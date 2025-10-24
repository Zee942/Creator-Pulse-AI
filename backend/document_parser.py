import docx
import PyPDF2
import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DocumentParser:
    """Parse DOCX and PDF documents to extract text content"""
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            return "\n".join(text)
        except Exception as e:
            logger.error(f"Error parsing DOCX: {str(e)}")
            raise
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return "\n".join(text)
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise
    
    @staticmethod
    def parse_document(file_path: str) -> str:
        """Parse document based on file extension"""
        if file_path.lower().endswith('.docx'):
            return DocumentParser.parse_docx(file_path)
        elif file_path.lower().endswith('.pdf'):
            return DocumentParser.parse_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")


class EntityExtractor:
    """Extract key entities from startup documents"""
    
    @staticmethod
    def extract_capital(text: str) -> Optional[Dict]:
        """Extract capital information"""
        capital_info = {
            'authorized_capital': None,
            'paid_up_capital': None
        }
        
        # More specific patterns for paid-up and authorized capital
        paid_up_pattern = r'paid[\s-]?up\s+capital[:\s]+(?:was\s+)?(?:QAR|qar)?\s*([\d,]+(?:\.\d+)?)'
        authorized_pattern = r'authorized\s+(?:share\s+)?capital[:\s]+(?:is\s+)?(?:QAR|qar)?\s*([\d,]+(?:\.\d+)?)'
        
        # Extract paid-up capital
        paid_matches = re.finditer(paid_up_pattern, text, re.IGNORECASE)
        for match in paid_matches:
            amount_str = match.group(1).replace(',', '')
            try:
                amount = float(amount_str)
                if amount >= 100000:  # Realistic minimum
                    capital_info['paid_up_capital'] = amount
                    break  # Take first match
            except ValueError:
                continue
        
        # Extract authorized capital
        auth_matches = re.finditer(authorized_pattern, text, re.IGNORECASE)
        for match in auth_matches:
            amount_str = match.group(1).replace(',', '')
                try:
                    amount = float(amount_str)
                    # Only accept amounts in realistic capital range (> 100,000 QAR)
                    if amount < 100000:
                        continue
                    if 'paid' in match.group(0).lower():
                        capital_info['paid_up_capital'] = amount
                    elif 'authorized' in match.group(0).lower():
                        capital_info['authorized_capital'] = amount
                    else:
                        # Default to paid-up capital if not specified
                        if not capital_info['paid_up_capital']:
                            capital_info['paid_up_capital'] = amount
                except ValueError:
                    continue
        
        return capital_info if any(capital_info.values()) else None
    
    @staticmethod
    def extract_data_location(text: str) -> Optional[List[str]]:
        """Extract data storage locations"""
        locations = []
        
        # Common cloud providers and locations
        location_patterns = [
            r'(?:AWS|Amazon|Azure|Google Cloud|GCP).*?(?:in|region[s]?)\s+([A-Za-z\s,]+)',
            r'server[s]?.*?(?:located|hosted|stored).*?(?:in|at)\s+([A-Za-z\s,]+)',
            r'data.*?(?:stored|hosted|processed).*?(?:in|at)\s+([A-Za-z\s,]+)',
            r'(?:Ireland|Singapore|Qatar|UAE|Dubai|USA|Europe|Asia)'
        ]
        
        for pattern in location_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                location = match.group(1) if match.lastindex else match.group(0)
                location = location.strip()
                if location and len(location) > 2:
                    locations.append(location)
        
        return list(set(locations)) if locations else None
    
    @staticmethod
    def extract_compliance_officer(text: str) -> Optional[Dict]:
        """Extract compliance officer information"""
        officer_info = {
            'has_officer': False,
            'details': None
        }
        
        # Patterns to detect compliance officer
        positive_patterns = [
            r'compliance\s+officer[:\s]+([\w\s\.]+)',
            r'(?:appointed|designated).*?compliance\s+officer',
            r'(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[\w\s]+.*?compliance\s+officer'
        ]
        
        negative_patterns = [
            r'no.*?compliance\s+officer',
            r'without.*?compliance\s+officer',
            r'compliance\s+officer.*?(?:pending|under review|not yet|will be)',
            r'interim.*?compliance'
        ]
        
        # Check negative patterns first
        for pattern in negative_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                officer_info['has_officer'] = False
                officer_info['details'] = 'No dedicated compliance officer found'
                return officer_info
        
        # Check positive patterns
        for pattern in positive_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                officer_info['has_officer'] = True
                officer_info['details'] = match.group(0)
                return officer_info
        
        return officer_info
    
    @staticmethod
    def extract_aml_policy(text: str) -> Optional[Dict]:
        """Extract AML policy information"""
        policy_info = {
            'has_policy': False,
            'is_approved': False,
            'has_monitoring': False,
            'details': None
        }
        
        # AML policy patterns
        if re.search(r'AML.*?(?:policy|policies)', text, re.IGNORECASE):
            policy_info['has_policy'] = True
            
            if re.search(r'board[\s-]?approved.*?AML|AML.*?board[\s-]?approved', text, re.IGNORECASE):
                policy_info['is_approved'] = True
            
            if re.search(r'under review|pending|draft', text, re.IGNORECASE):
                policy_info['is_approved'] = False
                policy_info['details'] = 'AML policy under review'
        
        # Transaction monitoring
        if re.search(r'(?:transaction|automated)\s+monitoring|monitoring\s+system', text, re.IGNORECASE):
            policy_info['has_monitoring'] = True
        
        return policy_info
    
    @staticmethod
    def extract_business_category(text: str) -> Optional[str]:
        """Determine business category based on services"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['p2p', 'peer-to-peer', 'lending', 'crowdfunding', 'marketplace lending']):
            return 'Category 2'
        elif any(keyword in text_lower for keyword in ['payment', 'psp', 'electronic money', 'payment service']):
            return 'Category 1'
        elif any(keyword in text_lower for keyword in ['wealth management', 'robo-advisor', 'investment advice', 'portfolio management']):
            return 'Category 3'
        
        return None
    
    @staticmethod
    def extract_all_entities(documents: Dict[str, str]) -> Dict:
        """Extract all entities from multiple documents"""
        combined_text = "\n\n".join(documents.values())
        
        entities = {
            'capital': EntityExtractor.extract_capital(combined_text),
            'data_locations': EntityExtractor.extract_data_location(combined_text),
            'compliance_officer': EntityExtractor.extract_compliance_officer(combined_text),
            'aml_policy': EntityExtractor.extract_aml_policy(combined_text),
            'business_category': EntityExtractor.extract_business_category(combined_text)
        }
        
        return entities
