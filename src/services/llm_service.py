"""
LLM Service for interfacing with Bosch LLM Farm API
"""
import openai
import os
from typing import List, Dict, Optional
from ..config import Config

class LLMService:
    """Service for interacting with Bosch LLM Farm API"""
    
    def __init__(self):
        """Initialize the LLM service with Bosch LLM Farm configuration"""
        # Check if API key is available
        if not Config.LLM_FARM_API_KEY or Config.LLM_FARM_API_KEY == "your-api-key-here":
            print("Warning: LLM Farm API key not configured. Some features may not work.")
            self.client = None
            self.model = Config.LLM_FARM_MODEL_NAME
            return
            
        # Configure OpenAI client for Bosch LLM Farm
        openai.api_base = Config.LLM_FARM_URL_PREFIX
        openai.api_key = Config.LLM_FARM_API_KEY
        openai.api_version = Config.LLM_FARM_API_VERSION
        
        self.client = openai.OpenAI(
            api_key=Config.LLM_FARM_API_KEY,
            base_url=Config.LLM_FARM_URL_PREFIX
        )
        self.model = Config.LLM_FARM_MODEL_NAME
    
    def generate_document_content(self, 
                                document_type: str, 
                                project_info: Dict, 
                                requirements: List[str],
                                template_variables: Optional[Dict] = None) -> str:
        """
        Generate document content using AI
        
        Args:
            document_type: Type of document to generate
            project_info: Project information dictionary
            requirements: List of project requirements
            template_variables: Optional template variables
            
        Returns:
            Generated document content as string
        """
        
        # Check if client is available
        if not self.client:
            return self._generate_fallback_content(document_type, project_info, requirements)
        
        prompt = self._build_document_prompt(
            document_type, project_info, requirements, template_variables
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert technical writer and project manager specializing in creating professional project documentation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            return content if content else self._generate_fallback_content(document_type, project_info, requirements)
            
        except Exception as e:
            print(f"Error generating document content: {str(e)}")
            return self._generate_fallback_content(document_type, project_info, requirements)
    
    def _build_document_prompt(self, 
                             document_type: str, 
                             project_info: Dict, 
                             requirements: List[str],
                             template_variables: Optional[Dict] = None) -> str:
        """Build the prompt for document generation"""
        
        prompt = f"""
Generate a comprehensive {document_type} document for the following project:

PROJECT INFORMATION:
- Name: {project_info.get('name', 'Not specified')}
- Type: {project_info.get('project_type', 'Not specified')}
- Description: {project_info.get('description', 'Not specified')}

PROJECT REQUIREMENTS:
{chr(10).join(f"- {req}" for req in requirements)}

DOCUMENT REQUIREMENTS:
Please create a professional {document_type} that includes:
1. Executive Summary
2. Project Overview
3. Scope and Objectives
4. Requirements Analysis
5. Implementation Plan
6. Risk Assessment
7. Timeline and Milestones
8. Resource Requirements
9. Quality Assurance
10. Approval and Sign-off

The document should be:
- Professional and comprehensive
- Suitable for stakeholder review
- Compliant with project management best practices
- Ready for approval workflow

Format the output as a structured document with clear headings and sections.
"""
        
        if template_variables:
            prompt += f"\n\nADDITIONAL TEMPLATE VARIABLES:\n"
            for key, value in template_variables.items():
                prompt += f"- {key}: {value}\n"
        
        return prompt
    
    def generate_project_suggestions(self, project_description: str) -> Dict[str, List[str]]:
        """Generate suggestions for project requirements and conditions"""
        
        prompt = f"""
Based on the following project description, suggest relevant requirements and conditions:

PROJECT DESCRIPTION: {project_description}

Please provide:
1. Functional Requirements (5-8 items)
2. Non-functional Requirements (3-5 items)  
3. Project Conditions/Constraints (3-5 items)
4. Recommended Document Types (5-7 items)

Format as JSON with keys: functional_requirements, non_functional_requirements, conditions, recommended_documents
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a project management expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.4
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            # Fallback suggestions if API fails
            return {
                "functional_requirements": [
                    "System shall meet specified performance criteria",
                    "Solution shall integrate with existing systems",
                    "User interface shall be intuitive and accessible"
                ],
                "non_functional_requirements": [
                    "System shall be available 99.9% of the time",
                    "Response time shall not exceed 2 seconds"
                ],
                "conditions": [
                    "Budget constraints must be observed",
                    "Compliance with company standards required"
                ],
                "recommended_documents": [
                    "Project Management Plan (PMP)",
                    "Technical Concept Document (TCD)",
                    "Risk Management Plan"
                ]
            }
    
    def _generate_fallback_content(self, document_type: str, project_info: Dict, requirements: List[str]) -> str:
        """Generate fallback content when AI service is not available"""
        content = f"""# {document_type}

## Project Overview
**Project Name:** {project_info.get('name', 'Not specified')}
**Project Type:** {project_info.get('project_type', 'Not specified')}
**Description:** {project_info.get('description', 'Not specified')}

## Executive Summary
This document outlines the {document_type.lower()} for the {project_info.get('name', 'project')} project.

## Requirements
"""
        if requirements:
            for i, req in enumerate(requirements, 1):
                content += f"{i}. {req}\n"
        else:
            content += "Requirements to be defined.\n"
        
        content += """
## Implementation Plan
- Phase 1: Planning and Design
- Phase 2: Development and Testing
- Phase 3: Deployment and Monitoring

## Risk Management
Identified risks and mitigation strategies will be documented as the project progresses.

## Timeline
Project timeline and milestones to be established based on requirements analysis.

## Approval
This document requires review and approval from designated stakeholders.

---
*This document was generated automatically. Please review and update as needed.*
"""
        return content
