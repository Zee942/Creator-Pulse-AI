from typing import Dict, List, Optional
import logging
from regulatory_kb import REGULATORY_ARTICLES, CAPITAL_REQUIREMENTS, RESOURCE_MAPPING

logger = logging.getLogger(__name__)

class GapAnalyzer:
    """Analyze compliance gaps based on extracted entities and regulatory requirements"""
    
    @staticmethod
    def analyze_data_residency(entities: Dict) -> Optional[Dict]:
        """Check Article 2.1.1 - Data Residency"""
        data_locations = entities.get('data_locations', [])
        
        if not data_locations:
            return {
                'gap_id': 'GAP_DATA_001',
                'article': '2.1.1',
                'article_name': REGULATORY_ARTICLES['2.1.1']['article'],
                'category': 'Data Protection',
                'severity': 'HIGH',
                'status': 'MISSING_INFO',
                'description': 'No data storage location information found',
                'requirement': REGULATORY_ARTICLES['2.1.1']['requirement'],
                'recommendation': 'Specify data storage locations and ensure compliance with Qatar residency requirements'
            }
        
        # Check if data is stored outside Qatar
        # Any mention of non-Qatar locations is a violation
        non_qatar_locations = [loc for loc in data_locations if 'qatar' not in loc.lower()]
        
        if non_qatar_locations:
            return {
                'gap_id': 'GAP_DATA_001',
                'article': '2.1.1',
                'article_name': REGULATORY_ARTICLES['2.1.1']['article'],
                'category': 'Data Protection',
                'severity': 'HIGH',
                'status': 'VIOLATION',
                'description': f'Gap: High Risk. Data storage is outside the State of Qatar. Found locations: {", ".join(non_qatar_locations)}',
                'requirement': REGULATORY_ARTICLES['2.1.1']['requirement'],
                'recommendation': 'Migrate all customer PII and transactional data to servers physically located within Qatar',
                'expert_recommendation': 'EXPERT_C101'
            }
        
        return None
    
    @staticmethod
    def analyze_compliance_officer(entities: Dict) -> Optional[Dict]:
        """Check Article 2.2.1 - Compliance Officer"""
        officer_info = entities.get('compliance_officer', {})
        
        if not officer_info or not officer_info.get('has_officer'):
            return {
                'gap_id': 'GAP_GOV_001',
                'article': '2.2.1',
                'article_name': REGULATORY_ARTICLES['2.2.1']['article'],
                'category': 'Governance',
                'severity': 'HIGH',
                'status': 'MISSING_ROLE',
                'description': 'Gap: Missing Mandatory Document/Role. Requires appointment of dedicated compliance officer',
                'requirement': REGULATORY_ARTICLES['2.2.1']['requirement'],
                'recommendation': 'Appoint a designated, independent Compliance Officer and submit CV and credentials to QCB for approval'
            }
        
        return None
    
    @staticmethod
    def analyze_capital_requirement(entities: Dict) -> Optional[Dict]:
        """Check capital requirements based on business category"""
        capital_info = entities.get('capital', {})
        business_category = entities.get('business_category')
        
        if not business_category:
            return {
                'gap_id': 'GAP_CAP_001',
                'article': 'N/A',
                'article_name': 'Capital Requirements',
                'category': 'Capital',
                'severity': 'MEDIUM',
                'status': 'MISSING_INFO',
                'description': 'Unable to determine business category for capital requirement assessment',
                'requirement': 'Business category must be identified',
                'recommendation': 'Clearly specify business category (Category 1, 2, or 3)'
            }
        
        required_capital = CAPITAL_REQUIREMENTS.get(business_category, {}).get('minimum_capital')
        paid_up_capital = capital_info.get('paid_up_capital') if capital_info else None
        
        if not paid_up_capital:
            return {
                'gap_id': 'GAP_CAP_002',
                'article': 'Licensing Pathways',
                'article_name': f'{business_category} Capital Requirement',
                'category': 'Capital',
                'severity': 'HIGH',
                'status': 'MISSING_INFO',
                'description': 'No paid-up capital information found',
                'requirement': f'{business_category} requires minimum capital of QAR {required_capital:,.0f}',
                'recommendation': 'Provide capital structure documentation'
            }
        
        if required_capital and paid_up_capital < required_capital:
            shortfall = required_capital - paid_up_capital
            return {
                'gap_id': 'GAP_CAP_003',
                'article': 'Licensing Pathways',
                'article_name': f'{business_category} Capital Requirement',
                'category': 'Capital',
                'severity': 'HIGH',
                'status': 'DEFICIENCY',
                'description': f'Gap: Financial Deficiency. Capital is QAR {shortfall:,.0f} short of the required minimum',
                'requirement': f'{business_category} requires minimum capital of QAR {required_capital:,.0f}',
                'recommendation': f'Increase paid-up capital from QAR {paid_up_capital:,.0f} to QAR {required_capital:,.0f}',
                'current_capital': paid_up_capital,
                'required_capital': required_capital,
                'shortfall': shortfall
            }
        
        return None
    
    @staticmethod
    def analyze_aml_compliance(entities: Dict) -> List[Dict]:
        """Check AML/CFT compliance - Articles 1.1.4 and 1.2.1"""
        gaps = []
        aml_policy = entities.get('aml_policy', {})
        
        # Check for AML policy (Article 1.1.4)
        if not aml_policy or not aml_policy.get('has_policy'):
            gaps.append({
                'gap_id': 'GAP_AML_001',
                'article': '1.1.4',
                'article_name': REGULATORY_ARTICLES['1.1.4']['article'],
                'category': 'AML',
                'severity': 'HIGH',
                'status': 'MISSING_DOCUMENT',
                'description': 'No AML/CFT policy found',
                'requirement': REGULATORY_ARTICLES['1.1.4']['requirement'],
                'recommendation': 'Develop and submit Board-approved AML/CFT Policy',
                'expert_recommendation': 'EXPERT_C102',
                'program_recommendation': 'QDB_EXPERT_002'
            })
        elif not aml_policy.get('is_approved'):
            gaps.append({
                'gap_id': 'GAP_AML_002',
                'article': '1.1.4',
                'article_name': REGULATORY_ARTICLES['1.1.4']['article'],
                'category': 'AML',
                'severity': 'HIGH',
                'status': 'INCOMPLETE',
                'description': 'AML/CFT policy exists but not Board-approved or under review',
                'requirement': REGULATORY_ARTICLES['1.1.4']['requirement'],
                'recommendation': 'Obtain Board approval for AML/CFT Policy',
                'expert_recommendation': 'EXPERT_C102',
                'program_recommendation': 'QDB_EXPERT_002'
            })
        
        # Check for transaction monitoring (Article 1.2.1)
        if not aml_policy or not aml_policy.get('has_monitoring'):
            gaps.append({
                'gap_id': 'GAP_AML_003',
                'article': '1.2.1',
                'article_name': REGULATORY_ARTICLES['1.2.1']['article'],
                'category': 'AML',
                'severity': 'HIGH',
                'status': 'MISSING_SYSTEM',
                'description': 'No automated transaction monitoring system mentioned',
                'requirement': REGULATORY_ARTICLES['1.2.1']['requirement'],
                'recommendation': 'Implement automated transaction monitoring system for suspicious activity detection',
                'expert_recommendation': 'EXPERT_C102',
                'program_recommendation': 'QDB_EXPERT_002'
            })
        
        return gaps
    
    @staticmethod
    def analyze_all_gaps(entities: Dict) -> List[Dict]:
        """Analyze all compliance gaps"""
        all_gaps = []
        
        # Data Residency
        data_gap = GapAnalyzer.analyze_data_residency(entities)
        if data_gap:
            all_gaps.append(data_gap)
        
        # Compliance Officer
        officer_gap = GapAnalyzer.analyze_compliance_officer(entities)
        if officer_gap:
            all_gaps.append(officer_gap)
        
        # Capital Requirements
        capital_gap = GapAnalyzer.analyze_capital_requirement(entities)
        if capital_gap:
            all_gaps.append(capital_gap)
        
        # AML Compliance
        aml_gaps = GapAnalyzer.analyze_aml_compliance(entities)
        all_gaps.extend(aml_gaps)
        
        return all_gaps
