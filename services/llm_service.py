"""
LLM Service for Bosch AI Document Assistant
Handles communication with Bosch LLM Farm API
"""

import os
import requests
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

class BoschLLMService:
    """Service class for interacting with Bosch LLM Farm"""
    
    def __init__(self):
        self.api_url = os.getenv('LLM_FARM_URL_PREFIX', '').rstrip('/')
        self.api_key = os.getenv('LLM_FARM_API_KEY', '')
        self.api_version = os.getenv('LLM_FARM_API_VERSION', '2024-08-01-preview')
        self.model_name = os.getenv('LLM_FARM_MODEL_NAME', 'gpt-4o-mini')
        self.deployment_name = os.getenv('LLM_FARM_DEPLOYMENT_NAME', 'askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18')
        
        # Build full endpoint URL
        if self.api_url and self.deployment_name:
            self.endpoint_url = f"{self.api_url}/openai/deployments/{self.deployment_name}/chat/completions"
        else:
            self.endpoint_url = None
        
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to LLM Farm API"""
        if not self.api_key:
            return {
                "success": False,
                "error": "API key not configured",
                "details": "Please set LLM_FARM_API_KEY in .env file"
            }
        
        if not self.endpoint_url:
            return {
                "success": False,
                "error": "API endpoint not configured",
                "details": "Please check LLM_FARM_URL_PREFIX and LLM_FARM_DEPLOYMENT_NAME in .env file"
            }
        
        try:
            # Simple test request
            test_payload = {
                "messages": [
                    {"role": "user", "content": "Hello, this is a connection test."}
                ],
                "max_tokens": 50,
                "temperature": 0.1
            }
            
            response = requests.post(
                f"{self.endpoint_url}?api-version={self.api_version}",
                headers=self.headers,
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Successfully connected to Bosch LLM Farm",
                    "model": self.model_name,
                    "endpoint": self.endpoint_url.split('/')[2]  # Just the domain
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status code {response.status_code}",
                    "details": response.text[:200] if response.text else "No response details"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out",
                "details": "The API request took too long to respond"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": "Connection failed",
                "details": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Unexpected error",
                "details": str(e)
            }
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000,
        use_project_context: bool = True,
        project_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generate response from LLM"""
        
        if not self.api_key or not self.endpoint_url:
            return {
                "success": False,
                "response": self._get_fallback_response(messages[-1]["content"] if messages else ""),
                "is_fallback": True,
                "error": "API not configured"
            }
        
        try:
            # Prepare messages with project context if requested
            prepared_messages = messages.copy()
            
            if use_project_context and project_context:
                # Build comprehensive context including template content
                context_content = f"""You are an AI assistant for Bosch project documentation. 
Current project context:
- Name: {project_context.get('name', 'N/A')}
- Type: {project_context.get('type', 'N/A')}
- Description: {project_context.get('description', 'N/A')}
- Functional Requirements: {', '.join(project_context.get('functional_reqs', [])[:3])}
- Non-functional Requirements: {', '.join(project_context.get('non_functional_reqs', [])[:3])}"""

                # Add template content if available
                if project_context.get('template_content'):
                    context_content += "\n\nReference materials from project templates:"
                    for file_info in project_context.get('template_content', []):
                        filename = file_info.get('filename', 'Unknown')
                        content = file_info.get('content', '')
                        # Only include meaningful, shorter content
                        if content and len(content) < 1000 and not content.startswith(('Excel file:', 'Word document:', 'PowerPoint presentation:', 'PDF document:')):
                            context_content += f"\n--- From {filename} ---\n{content[:800]}...\n"

                context_content += "\n\nProvide responses that are relevant to this project context while maintaining professional Bosch standards."
                
                context_message = {
                    "role": "system",
                    "content": context_content
                }
                prepared_messages.insert(0, context_message)
            
            payload = {
                "messages": prepared_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "stop": None
            }
            
            response = requests.post(
                f"{self.endpoint_url}?api-version={self.api_version}",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'choices' in data and len(data['choices']) > 0:
                    ai_response = data['choices'][0]['message']['content']
                    
                    return {
                        "success": True,
                        "response": ai_response,
                        "is_fallback": False,
                        "usage": data.get('usage', {}),
                        "model": self.model_name
                    }
                else:
                    return {
                        "success": False,
                        "response": self._get_fallback_response(messages[-1]["content"] if messages else ""),
                        "is_fallback": True,
                        "error": "No response choices returned"
                    }
            
            else:
                return {
                    "success": False,
                    "response": self._get_fallback_response(messages[-1]["content"] if messages else ""),
                    "is_fallback": True,
                    "error": f"API error: {response.status_code} - {response.text[:200]}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "response": self._get_fallback_response(messages[-1]["content"] if messages else ""),
                "is_fallback": True,
                "error": str(e)
            }
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Generate fallback response when API is not available"""
        fallback_responses = {
            "hello": "Hello! I'm the Bosch AI Assistant. I'm currently running in demo mode. Please configure the LLM_FARM_API_KEY in your .env file for full functionality.",
            "help": "I can help you with project documentation, requirements analysis, risk assessment, and technical writing. However, I'm currently in demo mode - please configure the API key for full AI capabilities.",
            "project": "I'd be happy to help with your project! In demo mode, I can provide template-based responses. Configure the API key to enable full AI project analysis and recommendations.",
            "document": "I can assist with document generation and review. Currently running in demo mode with template responses. Enable the API key for AI-powered document creation.",
            "risk": "Risk management is crucial for project success. In demo mode, I can provide general risk assessment templates. Enable API access for AI-powered risk analysis tailored to your specific project.",
        }
        
        # Simple keyword matching for fallback responses
        user_lower = user_message.lower()
        for keyword, response in fallback_responses.items():
            if keyword in user_lower:
                return response
        
        return f"""Thank you for your question: "{user_message}"

I'm currently running in demo mode. To enable full AI capabilities with the Bosch LLM Farm, please ensure your .env file contains:

```
LLM_FARM_API_KEY = "your-api-key-here"
LLM_FARM_URL_PREFIX = "https://aoai-farm.bosch-temp.com/api/"
```

In full mode, I can provide:
- Detailed project analysis and recommendations
- AI-generated documentation content
- Risk assessments tailored to your project
- Technical writing assistance
- Requirements analysis and validation

Would you like me to help you with any specific aspect of your project using template-based responses?"""

# Global instance
llm_service = BoschLLMService()
