"""
Advanced AI Features for Bosch Document Management System
Includes document intelligence, smart workflows, and enhanced assistance
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import hashlib

@dataclass
class DocumentAnalysis:
    """Structure for document analysis results"""
    document_type: str
    confidence: float
    key_entities: List[Dict[str, Any]]
    summary: str
    quality_score: float
    compliance_issues: List[str]
    action_items: List[str]
    risk_level: str

@dataclass
class WorkflowRecommendation:
    """Structure for workflow optimization recommendations"""
    recommended_approvers: List[str]
    estimated_duration: int
    risk_factors: List[str]
    optimization_suggestions: List[str]

class DocumentIntelligenceService:
    """Advanced AI service for document analysis and workflow optimization"""
    
    def __init__(self, llm_service, rag_service):
        self.llm_service = llm_service
        self.rag_service = rag_service
        
        # Document type patterns for classification
        self.document_patterns = {
            'Technical Specification': ['spec', 'requirement', 'technical', 'specification'],
            'Project Plan': ['plan', 'timeline', 'milestone', 'schedule', 'gantt'],
            'Risk Assessment': ['risk', 'assessment', 'mitigation', 'threat', 'vulnerability'],
            'Meeting Minutes': ['minutes', 'meeting', 'agenda', 'action items'],
            'Test Report': ['test', 'validation', 'verification', 'results'],
            'User Manual': ['manual', 'guide', 'instruction', 'how-to'],
            'Policy Document': ['policy', 'procedure', 'guideline', 'standard'],
            'Financial Report': ['budget', 'cost', 'financial', 'expense']
        }
        
        # Compliance keywords for different standards
        self.compliance_patterns = {
            'ISO 9001': ['quality management', 'process', 'improvement', 'customer satisfaction'],
            'ASPICE': ['automotive', 'software', 'process', 'assessment'],
            'ISO 27001': ['information security', 'risk management', 'security controls'],
            'GDPR': ['data protection', 'privacy', 'consent', 'personal data']
        }
    
    def analyze_document(self, content: str, filename: str) -> DocumentAnalysis:
        """Perform comprehensive document analysis"""
        
        # 1. Document Type Classification
        doc_type, confidence = self._classify_document_type(content, filename)
        
        # 2. Extract Key Entities
        entities = self._extract_key_entities(content)
        
        # 3. Generate Summary
        summary = self._generate_summary(content)
        
        # 4. Calculate Quality Score
        quality_score = self._assess_document_quality(content)
        
        # 5. Check Compliance
        compliance_issues = self._check_compliance(content)
        
        # 6. Extract Action Items
        action_items = self._extract_action_items(content)
        
        # 7. Assess Risk Level
        risk_level = self._assess_risk_level(content)
        
        return DocumentAnalysis(
            document_type=doc_type,
            confidence=confidence,
            key_entities=entities,
            summary=summary,
            quality_score=quality_score,
            compliance_issues=compliance_issues,
            action_items=action_items,
            risk_level=risk_level
        )
    
    def _classify_document_type(self, content: str, filename: str) -> Tuple[str, float]:
        """Classify document type using pattern matching and AI"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        scores = {}
        for doc_type, keywords in self.document_patterns.items():
            score = 0
            for keyword in keywords:
                # Check in filename (higher weight)
                if keyword in filename_lower:
                    score += 2
                # Check in content
                score += content_lower.count(keyword) * 0.5
            
            if score > 0:
                scores[doc_type] = score
        
        if scores:
            best_type = max(scores, key=scores.get)
            max_score = scores[best_type]
            confidence = min(max_score / 10.0, 1.0)  # Normalize to 0-1
            return best_type, confidence
        
        return 'General Document', 0.5
    
    def _extract_key_entities(self, content: str) -> List[Dict[str, Any]]:
        """Extract key entities like dates, names, numbers using pattern matching"""
        entities = []
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or DD/MM/YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY/MM/DD
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, content, re.IGNORECASE)
            for date in dates:
                entities.append({
                    'type': 'date',
                    'value': date,
                    'confidence': 0.9
                })
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        for email in emails:
            entities.append({
                'type': 'email',
                'value': email,
                'confidence': 0.95
            })
        
        # Extract numbers/measurements
        number_patterns = [
            r'\b\d+(?:\.\d+)?\s*(?:kg|g|m|cm|mm|l|ml|€|$|%)\b',  # Numbers with units
            r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:€|$|EUR|USD)\b'  # Currency
        ]
        
        for pattern in number_patterns:
            numbers = re.findall(pattern, content, re.IGNORECASE)
            for number in numbers:
                entities.append({
                    'type': 'measurement',
                    'value': number,
                    'confidence': 0.85
                })
        
        return entities[:20]  # Limit to top 20 entities
    
    def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """Generate document summary using LLM"""
        if not self.llm_service:
            # Fallback to extractive summary
            sentences = content.split('.')[:3]
            return '. '.join(sentences)[:max_length] + '...'
        
        try:
            prompt = f"""
            Please provide a concise summary of the following document content in 2-3 sentences.
            Focus on the main purpose, key points, and any important conclusions or decisions.
            
            Document content:
            {content[:2000]}...
            
            Summary:
            """
            
            response = self.llm_service.generate_response([
                {"role": "user", "content": prompt}
            ])
            
            if response.get('success'):
                return response['content'][:max_length]
            else:
                return "Summary generation failed. Please review document manually."
                
        except Exception as e:
            return f"Unable to generate summary: {str(e)}"
    
    def _assess_document_quality(self, content: str) -> float:
        """Assess document quality based on various metrics"""
        score = 1.0
        
        # Check document length (not too short or too long)
        word_count = len(content.split())
        if word_count < 50:
            score -= 0.3  # Too short
        elif word_count > 10000:
            score -= 0.1  # Very long
        
        # Check for spelling errors (basic)
        common_errors = ['teh', 'recieve', 'seperate', 'occured', 'neccessary']
        error_count = sum(content.lower().count(error) for error in common_errors)
        score -= min(error_count * 0.05, 0.2)
        
        # Check structure (headers, lists, etc.)
        if any(marker in content for marker in ['#', '1.', '2.', '•', '-']):
            score += 0.1  # Well-structured
        
        # Check for key sections
        key_sections = ['introduction', 'summary', 'conclusion', 'objective']
        section_count = sum(1 for section in key_sections if section.lower() in content.lower())
        score += min(section_count * 0.05, 0.15)
        
        return max(min(score, 1.0), 0.0)
    
    def _check_compliance(self, content: str) -> List[str]:
        """Check for compliance with various standards"""
        issues = []
        content_lower = content.lower()
        
        # Check for missing mandatory sections
        if 'risk' not in content_lower and len(content.split()) > 500:
            issues.append("Consider adding risk assessment section")
        
        if 'review' not in content_lower and 'approval' not in content_lower:
            issues.append("Document lacks review/approval information")
        
        # Check for data protection compliance
        if any(term in content_lower for term in ['personal data', 'customer data', 'employee data']):
            if 'gdpr' not in content_lower and 'data protection' not in content_lower:
                issues.append("Document may need GDPR compliance review")
        
        # Check for quality management
        quality_indicators = ['process', 'procedure', 'quality']
        if any(indicator in content_lower for indicator in quality_indicators):
            if 'iso 9001' not in content_lower and 'quality standard' not in content_lower:
                issues.append("Consider ISO 9001 compliance review")
        
        return issues
    
    def _extract_action_items(self, content: str) -> List[str]:
        """Extract action items from document content"""
        action_items = []
        
        # Look for action-oriented patterns
        action_patterns = [
            r'(?:action|todo|task|must|should|need to|required to)\s*:?\s*([^.!?\n]+)',
            r'(?:^|\n)\s*[-•*]\s*([^.\n]*(?:must|should|will|need)[^.\n]*)',
            r'(?:^|\n)\s*\d+\.\s*([^.\n]*(?:action|task|todo)[^.\n]*)'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 10:  # Filter out very short matches
                    action_items.append(match.strip())
        
        return list(set(action_items))[:10]  # Remove duplicates and limit to 10
    
    def _assess_risk_level(self, content: str) -> str:
        """Assess document risk level based on content analysis"""
        content_lower = content.lower()
        
        high_risk_terms = ['critical', 'urgent', 'failure', 'security', 'breach', 'error']
        medium_risk_terms = ['warning', 'caution', 'review', 'attention', 'issue']
        
        high_count = sum(content_lower.count(term) for term in high_risk_terms)
        medium_count = sum(content_lower.count(term) for term in medium_risk_terms)
        
        if high_count >= 3:
            return 'High'
        elif high_count >= 1 or medium_count >= 5:
            return 'Medium'
        else:
            return 'Low'
    
    def recommend_workflow(self, document_analysis: DocumentAnalysis, 
                          project_context: Optional[Dict] = None) -> WorkflowRecommendation:
        """Recommend optimal workflow based on document analysis"""
        
        # Default approvers based on document type
        type_approvers = {
            'Technical Specification': ['Technical Lead', 'Project Manager', 'Quality Assurance'],
            'Project Plan': ['Project Manager', 'Stakeholder', 'Finance'],
            'Risk Assessment': ['Risk Manager', 'Project Manager', 'Legal'],
            'Meeting Minutes': ['Project Manager'],
            'Test Report': ['Quality Assurance', 'Technical Lead'],
            'Policy Document': ['Legal', 'Compliance Officer', 'Management'],
            'Financial Report': ['Finance', 'Management']
        }
        
        recommended_approvers = type_approvers.get(
            document_analysis.document_type, 
            ['Project Manager', 'Technical Lead']
        )
        
        # Adjust based on risk level
        if document_analysis.risk_level == 'High':
            if 'Management' not in recommended_approvers:
                recommended_approvers.append('Management')
            estimated_duration = 5  # days
        elif document_analysis.risk_level == 'Medium':
            estimated_duration = 3
        else:
            estimated_duration = 2
        
        # Risk factors
        risk_factors = []
        if document_analysis.quality_score < 0.7:
            risk_factors.append("Low document quality score")
        if document_analysis.compliance_issues:
            risk_factors.append("Compliance issues detected")
        if document_analysis.risk_level == 'High':
            risk_factors.append("High-risk content identified")
        
        # Optimization suggestions
        suggestions = []
        if document_analysis.quality_score < 0.8:
            suggestions.append("Review document for completeness and clarity")
        if document_analysis.compliance_issues:
            suggestions.append("Address compliance issues before approval")
        if len(document_analysis.action_items) > 5:
            suggestions.append("Consider breaking down into smaller documents")
        
        return WorkflowRecommendation(
            recommended_approvers=recommended_approvers,
            estimated_duration=estimated_duration,
            risk_factors=risk_factors,
            optimization_suggestions=suggestions
        )
    
    def generate_compliance_report(self, documents: List[Dict]) -> Dict[str, Any]:
        """Generate compliance report for multiple documents"""
        report = {
            'total_documents': len(documents),
            'compliance_summary': {},
            'risk_distribution': {'High': 0, 'Medium': 0, 'Low': 0},
            'quality_stats': {
                'average_quality': 0.0,
                'low_quality_count': 0
            },
            'recommendations': []
        }
        
        total_quality = 0
        for doc in documents:
            # This would normally include actual analysis results
            # For now, simulating based on document properties
            mock_quality = 0.8  # Placeholder
            total_quality += mock_quality
            
            if mock_quality < 0.7:
                report['quality_stats']['low_quality_count'] += 1
        
        if documents:
            report['quality_stats']['average_quality'] = total_quality / len(documents)
        
        # Generate recommendations
        if report['quality_stats']['low_quality_count'] > 0:
            report['recommendations'].append(
                f"Review {report['quality_stats']['low_quality_count']} documents with low quality scores"
            )
        
        return report

# Initialize global service
ai_features_service = None

def get_ai_features_service(llm_service=None, rag_service=None):
    """Get or create AI features service instance"""
    global ai_features_service
    if ai_features_service is None and llm_service:
        ai_features_service = DocumentIntelligenceService(llm_service, rag_service)
    return ai_features_service
