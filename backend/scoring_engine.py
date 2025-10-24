from typing import Dict, List
import logging
from regulatory_kb import RESOURCE_MAPPING

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Calculate weighted readiness score"""
    
    # Category weights
    WEIGHTS = {
        'Capital': 0.25,
        'Governance': 0.25,
        'AML': 0.30,
        'Data Protection': 0.20
    }
    
    # Severity impact on score
    SEVERITY_IMPACT = {
        'HIGH': 0.0,      # High severity = 0% compliance
        'MEDIUM': 0.5,    # Medium severity = 50% compliance
        'LOW': 0.7        # Low severity = 70% compliance
    }
    
    @staticmethod
    def calculate_category_scores(gaps: List[Dict]) -> Dict:
        """Calculate compliance score for each category"""
        category_scores = {
            'Capital': 1.0,
            'Governance': 1.0,
            'AML': 1.0,
            'Data Protection': 1.0
        }
        
        category_gap_counts = {
            'Capital': 0,
            'Governance': 0,
            'AML': 0,
            'Data Protection': 0
        }
        
        # Calculate impact of gaps on each category
        for gap in gaps:
            category = gap['category']
            severity = gap['severity']
            
            if category in category_scores:
                category_gap_counts[category] += 1
                # Each gap reduces the category score based on severity
                impact = ScoringEngine.SEVERITY_IMPACT.get(severity, 0.5)
                category_scores[category] = min(category_scores[category], impact)
        
        return category_scores, category_gap_counts
    
    @staticmethod
    def calculate_overall_score(gaps: List[Dict]) -> Dict:
        """Calculate overall readiness score"""
        category_scores, category_gap_counts = ScoringEngine.calculate_category_scores(gaps)
        
        # Calculate weighted overall score
        overall_score = 0.0
        for category, weight in ScoringEngine.WEIGHTS.items():
            overall_score += category_scores[category] * weight
        
        # Convert to percentage
        overall_percentage = overall_score * 100
        
        # Determine readiness level
        if overall_percentage >= 90:
            readiness_level = 'EXCELLENT'
            readiness_color = 'green'
        elif overall_percentage >= 75:
            readiness_level = 'GOOD'
            readiness_color = 'blue'
        elif overall_percentage >= 50:
            readiness_level = 'MODERATE'
            readiness_color = 'yellow'
        elif overall_percentage >= 25:
            readiness_level = 'POOR'
            readiness_color = 'orange'
        else:
            readiness_level = 'CRITICAL'
            readiness_color = 'red'
        
        return {
            'overall_score': round(overall_percentage, 2),
            'readiness_level': readiness_level,
            'readiness_color': readiness_color,
            'category_scores': {k: round(v * 100, 2) for k, v in category_scores.items()},
            'category_gap_counts': category_gap_counts,
            'total_gaps': len(gaps),
            'high_severity_gaps': len([g for g in gaps if g['severity'] == 'HIGH']),
            'medium_severity_gaps': len([g for g in gaps if g['severity'] == 'MEDIUM']),
            'low_severity_gaps': len([g for g in gaps if g['severity'] == 'LOW'])
        }


class RecommendationEngine:
    """Generate expert and program recommendations based on gaps"""
    
    @staticmethod
    def get_expert_recommendations(gaps: List[Dict]) -> List[Dict]:
        """Map gaps to expert recommendations"""
        recommendations = []
        expert_ids = set()
        
        for gap in gaps:
            expert_id = gap.get('expert_recommendation')
            if expert_id and expert_id not in expert_ids:
                expert_data = RESOURCE_MAPPING['experts'].get(expert_id)
                if expert_data:
                    recommendations.append({
                        'type': 'expert',
                        'expert_id': expert_id,
                        'name': expert_data['name'],
                        'specialization': expert_data['specialization'],
                        'contact': expert_data.get('contact', 'N/A'),
                        'relevant_articles': expert_data['article_mapping'],
                        'relevant_gaps': [g['gap_id'] for g in gaps if g.get('expert_recommendation') == expert_id]
                    })
                    expert_ids.add(expert_id)
        
        return recommendations
    
    @staticmethod
    def get_program_recommendations(gaps: List[Dict]) -> List[Dict]:
        """Map gaps to program recommendations"""
        recommendations = []
        program_ids = set()
        
        for gap in gaps:
            program_id = gap.get('program_recommendation')
            if program_id and program_id not in program_ids:
                program_data = RESOURCE_MAPPING['programs'].get(program_id)
                if program_data:
                    recommendations.append({
                        'type': 'program',
                        'program_id': program_id,
                        'name': program_data['name'],
                        'focus_areas': program_data['focus_areas'],
                        'description': program_data['description'],
                        'duration': program_data['duration'],
                        'website': program_data.get('website', 'N/A'),
                        'relevant_gaps': [g['gap_id'] for g in gaps if g.get('program_recommendation') == program_id]
                    })
                    program_ids.add(program_id)
        
        # Always add general accelerator program
        if 'QDB_INCUBATOR_001' not in program_ids:
            program_data = RESOURCE_MAPPING['programs']['QDB_INCUBATOR_001']
            recommendations.append({
                'type': 'program',
                'program_id': 'QDB_INCUBATOR_001',
                'name': program_data['name'],
                'focus_areas': program_data['focus_areas'],
                'description': program_data['description'],
                'duration': program_data['duration'],
                'website': program_data.get('website', 'N/A'),
                'relevant_gaps': []
            })
        
        return recommendations
    
    @staticmethod
    def get_all_recommendations(gaps: List[Dict]) -> Dict:
        """Get all recommendations (experts + programs)"""
        return {
            'experts': RecommendationEngine.get_expert_recommendations(gaps),
            'programs': RecommendationEngine.get_program_recommendations(gaps)
        }
