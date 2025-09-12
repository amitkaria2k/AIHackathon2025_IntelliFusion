"""
Configuration module for AI-Powered Project Documentation Management System
Loads environment variables and application settings
"""
import os
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Bosch LLM Farm API Configuration
    LLM_FARM_URL_PREFIX: str = os.getenv("LLM_FARM_URL_PREFIX", "https://aoai-farm.bosch-temp.com/api/")
    LLM_FARM_API_KEY: str = os.getenv("LLM_FARM_API_KEY", "")
    LLM_FARM_API_VERSION: str = os.getenv("LLM_FARM_API_VERSION", "2024-08-01-preview")
    LLM_FARM_MODEL_NAME: str = os.getenv("LLM_FARM_MODEL_NAME", "gpt-4o-mini")
    LLM_FARM_DEPLOYMENT_NAME: str = os.getenv("LLM_FARM_DEPLOYMENT_NAME", "askbosch-prod-farm-openai-gpt-4o-mini-2024-07-18")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///project_docs.db")
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Document Storage
    DOCUMENTS_DIR: Path = Path(os.getenv("DOCUMENTS_DIR", "generated_documents"))
    TEMPLATES_DIR: Path = Path(os.getenv("TEMPLATES_DIR", "templates/document_templates"))
    
    # Workflow Configuration
    DEFAULT_APPROVERS: List[str] = os.getenv("DEFAULT_APPROVERS", "Project Manager,Technical Lead,Quality Assurance").split(",")
    
    # Docupedia Configuration
    DOCUPEDIA_PAT: str = os.getenv("DOCUPEDIA_PAT", "")
    DOCUPEDIA_EMAIL: str = os.getenv("DOCUPEDIA_EMAIL", "")
    DOCUPEDIA_USER_AGENT: str = os.getenv("DOCUPEDIA_USER_AGENT", "BoschAI-DocumentAssistant/1.0")
    
    # Project Types
    PROJECT_TYPES = [
        "Software Development",
        "Hardware Development", 
        "Research Project",
        "Process Improvement",
        "Product Development",
        "Custom"
    ]
    
    # Document Types
    DOCUMENT_TYPES = [
        "Project Management Plan (PMP)",
        "Technical Concept Document (TCD)",
        "Configuration Management Plan",
        "Communication Management Plan",
        "Time Plan",
        "PM Baseline",
        "Picaso Document",
        "Risk Management Plan",
        "Quality Plan",
        "Requirements Document",
        "Architecture Document",
        "Test Plan"
    ]
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DOCUMENTS_DIR.mkdir(exist_ok=True)
        cls.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# Create directories on import
Config.create_directories()
