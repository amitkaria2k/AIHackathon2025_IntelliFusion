"""
Database models for the Project Documentation Management System
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from .config import Config

Base = declarative_base()

class Project(Base):
    """Project model for storing project information"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    project_type = Column(String(100), nullable=False)
    description = Column(Text)
    requirements = Column(JSON)  # Store project requirements as JSON
    conditions = Column(JSON)    # Store project conditions as JSON
    status = Column(String(50), default="Active")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    documents = relationship("Document", back_populates="project")
    workflows = relationship("Workflow", back_populates="project")

class Document(Base):
    """Document model for storing generated documents"""
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    document_type = Column(String(100), nullable=False)
    template_name = Column(String(100))
    file_path = Column(String(500))
    version = Column(String(20), default="1.0")
    status = Column(String(50), default="Draft")  # Draft, Under Review, Approved, Obsolete
    content_hash = Column(String(64))  # For change detection
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="documents")
    workflow_tasks = relationship("WorkflowTask", back_populates="document")
    document_revisions = relationship("DocumentRevision", back_populates="document")

class DocumentRevision(Base):
    """Document revision model for version control"""
    __tablename__ = "document_revisions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    version = Column(String(20), nullable=False)
    changes_description = Column(Text)
    file_path = Column(String(500))
    created_by = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="document_revisions")

class Workflow(Base):
    """Workflow model for approval processes"""
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="Active")  # Active, Completed, Cancelled
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="workflows")
    tasks = relationship("WorkflowTask", back_populates="workflow")

class WorkflowTask(Base):
    """Workflow task model for individual approval tasks"""
    __tablename__ = "workflow_tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"))
    task_name = Column(String(200), nullable=False)
    assignee = Column(String(100), nullable=False)
    status = Column(String(50), default="Pending")  # Pending, In Progress, Approved, Rejected
    priority = Column(String(20), default="Medium")  # Low, Medium, High, Critical
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    comments = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    workflow = relationship("Workflow", back_populates="tasks")
    document = relationship("Document", back_populates="workflow_tasks")

class DocumentTemplate(Base):
    """Document template model"""
    __tablename__ = "document_templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    document_type = Column(String(100), nullable=False)
    template_path = Column(String(500), nullable=False)
    description = Column(Text)
    variables = Column(JSON)  # Template variables schema
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Database setup
def get_engine():
    """Get database engine, creating it if necessary"""
    return create_engine(Config.DATABASE_URL, echo=Config.DEBUG)

def get_session_local():
    """Get SessionLocal class"""
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
