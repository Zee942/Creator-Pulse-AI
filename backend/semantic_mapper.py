from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import logging
from regulatory_kb import REGULATORY_ARTICLES

logger = logging.getLogger(__name__)

class SemanticMapper:
    """Use semantic similarity to map document text to regulatory articles"""
    
    def __init__(self):
        # Load a lightweight semantic model
        logger.info("Loading semantic model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Pre-compute embeddings for all regulatory articles
        self.article_texts = []
        self.article_ids = []
        
        for article_id, article_data in REGULATORY_ARTICLES.items():
            # Combine article text with keywords for better matching
            text = f"{article_data['requirement']} {' '.join(article_data['keywords'])}"
            self.article_texts.append(text)
            self.article_ids.append(article_id)
        
        logger.info(f"Computing embeddings for {len(self.article_texts)} regulatory articles...")
        self.article_embeddings = self.model.encode(self.article_texts)
        logger.info("Semantic mapper initialized successfully")
    
    def map_text_to_articles(self, text: str, threshold: float = 0.3) -> List[Tuple[str, float]]:
        """
        Map document text to relevant regulatory articles using semantic similarity
        
        Args:
            text: Document text to analyze
            threshold: Minimum similarity score (0-1)
        
        Returns:
            List of (article_id, similarity_score) tuples
        """
        # Encode the input text
        text_embedding = self.model.encode([text])[0]
        
        # Calculate cosine similarity with all articles
        similarities = cosine_similarity([text_embedding], self.article_embeddings)[0]
        
        # Filter by threshold and sort by similarity
        results = []
        for article_id, similarity in zip(self.article_ids, similarities):
            if similarity >= threshold:
                results.append((article_id, float(similarity)))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def analyze_document_semantically(self, document_text: str) -> Dict[str, List[Tuple[str, float]]]:
        """
        Analyze entire document and map sections to regulatory articles
        
        Returns:
            Dict with categories as keys and matched articles with scores
        """
        # Split document into meaningful chunks (paragraphs)
        chunks = [p.strip() for p in document_text.split('\n\n') if len(p.strip()) > 50]
        
        category_matches = {
            'AML': [],
            'Data Protection': [],
            'Governance': [],
            'Capital': []
        }
        
        # Analyze each chunk
        for chunk in chunks:
            matches = self.map_text_to_articles(chunk, threshold=0.25)
            
            for article_id, score in matches:
                category = REGULATORY_ARTICLES[article_id]['category']
                if category in category_matches:
                    category_matches[category].append((article_id, score, chunk[:100]))
        
        return category_matches
    
    def get_relevant_articles_for_entities(self, entities: Dict) -> Dict[str, List[str]]:
        """
        Given extracted entities, suggest relevant regulatory articles
        """
        relevant_articles = {
            'data_residency': [],
            'capital': [],
            'governance': [],
            'aml': []
        }
        
        # Data location mentions -> Data Protection articles
        if entities.get('data_locations'):
            locations_text = ' '.join(entities['data_locations'])
            matches = self.map_text_to_articles(locations_text, threshold=0.2)
            for article_id, score in matches:
                if REGULATORY_ARTICLES[article_id]['category'] == 'Data Protection':
                    relevant_articles['data_residency'].append(article_id)
        
        # Capital mentions -> Capital articles
        if entities.get('capital'):
            capital_text = f"capital paid-up authorized {entities['capital']}"
            matches = self.map_text_to_articles(capital_text, threshold=0.2)
            relevant_articles['capital'] = [m[0] for m in matches[:3]]
        
        # Compliance officer -> Governance articles
        if entities.get('compliance_officer'):
            officer_text = "compliance officer governance board directors"
            matches = self.map_text_to_articles(officer_text, threshold=0.2)
            for article_id, score in matches:
                if REGULATORY_ARTICLES[article_id]['category'] == 'Governance':
                    relevant_articles['governance'].append(article_id)
        
        # AML policy -> AML articles
        if entities.get('aml_policy'):
            aml_text = "AML CFT anti-money laundering policy transaction monitoring suspicious"
            matches = self.map_text_to_articles(aml_text, threshold=0.2)
            for article_id, score in matches:
                if REGULATORY_ARTICLES[article_id]['category'] == 'AML':
                    relevant_articles['aml'].append(article_id)
        
        return relevant_articles
