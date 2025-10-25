from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
import uuid
from datetime import datetime, timezone
import shutil
import tempfile

# Import our custom modules
from document_parser import DocumentParser, EntityExtractor
from gap_analyzer import GapAnalyzer
from scoring_engine import ScoringEngine, RecommendationEngine
from semantic_mapper import SemanticMapper

# Initialize semantic mapper (lazy loading)
_semantic_mapper = None

def get_semantic_mapper():
    global _semantic_mapper
    if _semantic_mapper is None:
        logger.info("Initializing semantic mapper...")
        _semantic_mapper = SemanticMapper()
    return _semantic_mapper

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="FinRegX - Smart Regulatory Readiness Platform")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class AssessmentCreate(BaseModel):
    startup_name: str
    contact_email: Optional[str] = None

class AssessmentResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    startup_name: str
    contact_email: Optional[str] = None
    status: str = "processing"  # processing, completed, failed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    
class AssessmentResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    assessment_id: str
    startup_name: str
    entities: Dict
    gaps: List[Dict]
    score: Dict
    recommendations: Dict
    created_at: datetime
    
class UploadResponse(BaseModel):
    message: str
    assessment_id: str
    files_uploaded: int


# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {
        "message": "FinRegX API - Smart Regulatory Readiness Platform",
        "version": "1.0.0",
        "endpoints": {
            "create_assessment": "/api/assessments",
            "upload_documents": "/api/assessments/{assessment_id}/upload",
            "get_assessment": "/api/assessments/{assessment_id}",
            "list_assessments": "/api/assessments"
        }
    }

@api_router.post("/assessments", response_model=AssessmentResponse)
async def create_assessment(input: AssessmentCreate):
    """Create a new compliance assessment"""
    assessment = AssessmentResponse(
        startup_name=input.startup_name,
        contact_email=input.contact_email,
        status="created"
    )
    
    doc = assessment.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.assessments.insert_one(doc)
    return assessment

@api_router.post("/assessments/{assessment_id}/upload")
async def upload_documents(
    assessment_id: str,
    files: List[UploadFile] = File(...)
):
    """Upload startup documents for analysis"""
    try:
        # Check if assessment exists
        assessment = await db.assessments.find_one({"id": assessment_id}, {"_id": 0})
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Create temp directory for uploads
        temp_dir = tempfile.mkdtemp()
        uploaded_files = []
        parsed_documents = {}
        
        # Save and parse each file
        for file in files:
            if not file.filename.lower().endswith(('.pdf', '.docx')):
                continue
                
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)
            
            uploaded_files.append(file.filename)
            
            # Parse document
            try:
                text = DocumentParser.parse_document(file_path)
                parsed_documents[file.filename] = text
            except Exception as e:
                logger.error(f"Error parsing {file.filename}: {str(e)}")
        
        # Extract entities
        entities = EntityExtractor.extract_all_entities(parsed_documents)
        
        # Perform semantic analysis (RAG)
        logger.info("Performing semantic regulatory mapping...")
        semantic_mapper = get_semantic_mapper()
        combined_text = "\n\n".join(parsed_documents.values())
        semantic_analysis = semantic_mapper.analyze_document_semantically(combined_text)
        relevant_articles = semantic_mapper.get_relevant_articles_for_entities(entities)
        
        # Analyze gaps
        gaps = GapAnalyzer.analyze_all_gaps(entities)
        
        # Calculate score
        score = ScoringEngine.calculate_overall_score(gaps)
        
        # Hybrid vetting: Flag for expert review if score is critically low
        needs_expert_review = score['overall_score'] < 50 or score['high_severity_gaps'] >= 3
        expert_review_reason = None
        if needs_expert_review:
            if score['overall_score'] < 25:
                expert_review_reason = "Critical readiness score - comprehensive expert review required"
            elif score['high_severity_gaps'] >= 4:
                expert_review_reason = f"Multiple high-severity gaps detected ({score['high_severity_gaps']} gaps)"
            else:
                expert_review_reason = "Low readiness score - expert validation recommended"
        
        # Get recommendations
        recommendations = RecommendationEngine.get_all_recommendations(gaps)
        
        # Save results
        result = {
            "assessment_id": assessment_id,
            "startup_name": assessment['startup_name'],
            "entities": entities,
            "semantic_analysis": {
                "article_matches": semantic_analysis,
                "relevant_articles": relevant_articles
            },
            "gaps": gaps,
            "score": score,
            "recommendations": recommendations,
            "hybrid_vetting": {
                "needs_expert_review": needs_expert_review,
                "review_reason": expert_review_reason,
                "confidence_level": "HIGH" if score['overall_score'] > 70 else "MEDIUM" if score['overall_score'] > 40 else "LOW"
            },
            "documents_analyzed": uploaded_files,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.results.insert_one(result)
        
        # Update assessment status
        await db.assessments.update_one(
            {"id": assessment_id},
            {"$set": {
                "status": "completed",
                "completed_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        # Clean up temp files
        shutil.rmtree(temp_dir)
        
        return {
            "message": "Documents uploaded and analyzed successfully",
            "assessment_id": assessment_id,
            "files_uploaded": len(uploaded_files),
            "gaps_detected": len(gaps),
            "readiness_score": score['overall_score']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")

@api_router.get("/assessments/{assessment_id}")
async def get_assessment_result(assessment_id: str):
    """Get assessment results"""
    result = await db.results.find_one({"assessment_id": assessment_id}, {"_id": 0})
    
    if not result:
        # Check if assessment exists but not completed
        assessment = await db.assessments.find_one({"id": assessment_id}, {"_id": 0})
        if assessment:
            return {
                "message": "Assessment in progress",
                "status": assessment.get('status', 'processing'),
                "assessment_id": assessment_id
            }
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return result

@api_router.get("/assessments")
async def list_assessments(limit: int = 50):
    """List all assessments"""
    assessments = await db.assessments.find({}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    return {"assessments": assessments, "count": len(assessments)}

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()