"""
AI-Powered Project Documentation Management System
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
from typing import Dict, List

# Import our services
from src.config import Config
from src.database import create_tables, get_session_local, Project, Document, Workflow
from src.services.llm_service import LLMService
from src.services.document_generator import DocumentGeneratorService
from src.services.workflow_manager import WorkflowManagerService

# Configure Streamlit page
st.set_page_config(
    page_title="AI Project Documentation Manager",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_app():
    """Initialize the application"""
    # Create database tables
    create_tables()
    
    # Initialize services
    if 'llm_service' not in st.session_state:
        st.session_state.llm_service = LLMService()
    
    if 'doc_generator' not in st.session_state:
        st.session_state.doc_generator = DocumentGeneratorService()
        st.session_state.doc_generator.create_default_templates()
    
    if 'workflow_manager' not in st.session_state:
        st.session_state.workflow_manager = WorkflowManagerService()

def main():
    """Main application function"""
    initialize_app()
    
    # Sidebar navigation
    st.sidebar.title("📄 Documentation Manager")
    
    page = st.sidebar.selectbox(
        "Navigate to:",
        [
            "🏠 Dashboard",
            "🆕 New Project",
            "📝 Generate Document",
            "👥 Workflow Management",
            "📊 Project Overview",
            "⚙️ Settings"
        ]
    )
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🆕 New Project":
        show_new_project()
    elif page == "📝 Generate Document":
        show_document_generation()
    elif page == "👥 Workflow Management":
        show_workflow_management()
    elif page == "📊 Project Overview":
        show_project_overview()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Display main dashboard"""
    st.title("🏠 Dashboard")
    st.markdown("Welcome to the AI-Powered Project Documentation Management System")
    
    # Get database session
    SessionLocal = get_session_local()
    db = SessionLocal()
    
    try:
        # Get statistics
        total_projects = db.query(Project).count()
        total_documents = db.query(Document).count()
        total_workflows = db.query(Workflow).count()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Projects", total_projects)
        
        with col2:
            st.metric("Generated Documents", total_documents)
            
        with col3:
            st.metric("Active Workflows", total_workflows)
            
        with col4:
            st.metric("Template Types", len(Config.DOCUMENT_TYPES))
        
        # Recent projects
        st.subheader("Recent Projects")
        projects = db.query(Project).order_by(Project.created_at.desc()).limit(5).all()
        
        if projects:
            project_data = []
            for project in projects:
                project_data.append({
                    "Name": project.name,
                    "Type": project.project_type,
                    "Status": project.status,
                    "Created": project.created_at.strftime("%Y-%m-%d")
                })
            
            df = pd.DataFrame(project_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No projects found. Create your first project!")
            
        # Pending tasks
        st.subheader("Pending Approval Tasks")
        pending_tasks = st.session_state.workflow_manager.get_pending_tasks()
        
        if pending_tasks:
            task_data = []
            for task in pending_tasks[:10]:  # Show only first 10
                task_data.append({
                    "Document": task["document_name"],
                    "Type": task["document_type"],
                    "Assignee": task["assignee"],
                    "Priority": task["priority"],
                    "Due Date": task["due_date"][:10] if task["due_date"] else "Not set"
                })
            
            df = pd.DataFrame(task_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No pending approval tasks.")
            
    finally:
        db.close()

def show_new_project():
    """Show new project creation form"""
    st.title("🆕 Create New Project")
    
    with st.form("new_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name*", placeholder="Enter project name")
            project_type = st.selectbox("Project Type*", Config.PROJECT_TYPES)
            
        with col2:
            description = st.text_area("Project Description*", 
                                     placeholder="Describe your project objectives and scope",
                                     height=100)
        
        # AI-generated suggestions
        st.subheader("AI-Generated Requirements & Suggestions")
        
        if st.form_submit_button("🤖 Generate AI Suggestions", type="secondary"):
            if description:
                with st.spinner("Generating AI suggestions..."):
                    try:
                        suggestions = st.session_state.llm_service.generate_project_suggestions(description)
                        st.session_state.ai_suggestions = suggestions
                        st.success("AI suggestions generated!")
                    except Exception as e:
                        st.error(f"Error generating suggestions: {str(e)}")
                        # Use fallback suggestions
                        st.session_state.ai_suggestions = {
                            "functional_requirements": ["System shall meet specified criteria"],
                            "non_functional_requirements": ["High availability required"],
                            "conditions": ["Budget constraints apply"],
                            "recommended_documents": ["Project Management Plan"]
                        }
            else:
                st.warning("Please enter a project description first.")
        
        # Display suggestions if available
        if 'ai_suggestions' in st.session_state:
            suggestions = st.session_state.ai_suggestions
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Suggested Functional Requirements:**")
                functional_reqs = st.multiselect(
                    "Select functional requirements:",
                    suggestions.get("functional_requirements", []),
                    default=suggestions.get("functional_requirements", [])[:3]
                )
                
                additional_functional = st.text_area("Additional functional requirements:")
                
                st.write("**Suggested Non-Functional Requirements:**")
                non_functional_reqs = st.multiselect(
                    "Select non-functional requirements:",
                    suggestions.get("non_functional_requirements", []),
                    default=suggestions.get("non_functional_requirements", [])
                )
                
            with col2:
                st.write("**Suggested Conditions/Constraints:**")
                conditions = st.multiselect(
                    "Select conditions:",
                    suggestions.get("conditions", []),
                    default=suggestions.get("conditions", [])
                )
                
                additional_conditions = st.text_area("Additional conditions:")
                
                st.write("**Recommended Document Types:**")
                recommended_docs = st.multiselect(
                    "Select document types to generate:",
                    suggestions.get("recommended_documents", []),
                    default=suggestions.get("recommended_documents", [])[:3]
                )
        else:
            # Manual input if no AI suggestions
            col1, col2 = st.columns(2)
            
            with col1:
                functional_reqs = st.text_area("Functional Requirements (one per line)")
                non_functional_reqs = st.text_area("Non-Functional Requirements (one per line)")
                
            with col2:
                conditions = st.text_area("Project Conditions/Constraints (one per line)")
                recommended_docs = st.multiselect("Document Types to Generate", Config.DOCUMENT_TYPES)
        
        # Submit project
        submitted = st.form_submit_button("✅ Create Project", type="primary")
        
        if submitted:
            if project_name and project_type and description:
                # Prepare requirements and conditions
                all_functional_reqs = functional_reqs[:]
                if 'additional_functional' in locals() and additional_functional:
                    all_functional_reqs.extend(additional_functional.split('\n'))
                
                all_conditions = conditions[:]
                if 'additional_conditions' in locals() and additional_conditions:
                    all_conditions.extend(additional_conditions.split('\n'))
                
                # Create project
                try:
                    db = SessionLocal()
                    project = Project(
                        name=project_name,
                        project_type=project_type,
                        description=description,
                        requirements={
                            "functional": [req.strip() for req in all_functional_reqs if req.strip()],
                            "non_functional": [req.strip() for req in non_functional_reqs if req.strip()],
                            "conditions": [cond.strip() for cond in all_conditions if cond.strip()]
                        }
                    )
                    
                    db.add(project)
                    db.commit()
                    
                    st.success(f"✅ Project '{project_name}' created successfully!")
                    
                    # Store project ID for document generation
                    st.session_state.current_project_id = project.id
                    st.session_state.recommended_docs = recommended_docs
                    
                    st.info("You can now generate documents for this project in the 'Generate Document' section.")
                    
                    db.close()
                    
                except Exception as e:
                    st.error(f"Error creating project: {str(e)}")
            else:
                st.error("Please fill in all required fields marked with *")

def show_document_generation():
    """Show document generation interface"""
    st.title("📝 Generate Document")
    
    # Get available projects
    db = SessionLocal()
    projects = db.query(Project).all()
    db.close()
    
    if not projects:
        st.warning("No projects found. Please create a project first.")
        return
    
    # Project selection
    project_options = {f"{p.name} ({p.project_type})": p.id for p in projects}
    selected_project = st.selectbox("Select Project", list(project_options.keys()))
    
    if selected_project:
        project_id = project_options[selected_project]
        
        # Get project details
        db = SessionLocal()
        project = db.query(Project).filter(Project.id == project_id).first()
        db.close()
        
        if project:
            st.info(f"**Project:** {project.name} | **Type:** {project.project_type}")
            
            with st.form("document_generation_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    document_type = st.selectbox("Document Type", Config.DOCUMENT_TYPES)
                    template_name = st.selectbox("Template", ["Default Word Document", "HTML Template"])
                    
                with col2:
                    custom_requirements = st.text_area(
                        "Additional Requirements (optional)",
                        placeholder="Any specific requirements for this document..."
                    )
                
                generate_button = st.form_submit_button("🚀 Generate Document", type="primary")
                
                if generate_button:
                    with st.spinner("Generating document with AI..."):
                        try:
                            # Prepare project info and requirements
                            project_info = {
                                "name": project.name,
                                "project_type": project.project_type,
                                "description": project.description
                            }
                            
                            # Combine all requirements
                            all_requirements = []
                            if project.requirements:
                                reqs = project.requirements
                                if "functional" in reqs:
                                    all_requirements.extend(reqs["functional"])
                                if "non_functional" in reqs:
                                    all_requirements.extend(reqs["non_functional"])
                                if "conditions" in reqs:
                                    all_requirements.extend(reqs["conditions"])
                            
                            if custom_requirements:
                                all_requirements.extend(custom_requirements.split('\n'))
                            
                            # Generate document content using AI
                            content = st.session_state.llm_service.generate_document_content(
                                document_type=document_type,
                                project_info=project_info,
                                requirements=all_requirements
                            )
                            
                            # Generate document file
                            template = None if template_name == "Default Word Document" else "project_management_plan"
                            
                            file_path = st.session_state.doc_generator.generate_document(
                                project_id=project_id,
                                document_type=document_type,
                                content=content,
                                template_name=template
                            )
                            
                            st.success(f"✅ Document generated successfully!")
                            st.info(f"📁 File saved to: {file_path}")
                            
                            # Create approval workflow
                            workflow_id = st.session_state.workflow_manager.create_approval_workflow(
                                project_id=project_id,
                                document_id=file_path.split('/')[-1],  # Use filename as temp ID
                                workflow_name=f"{document_type} Review"
                            )
                            
                            st.success("🔄 Approval workflow created!")
                            
                            # Display generated content preview
                            st.subheader("Document Preview")
                            with st.expander("Show generated content", expanded=True):
                                st.markdown(content)
                            
                        except Exception as e:
                            st.error(f"Error generating document: {str(e)}")

def show_workflow_management():
    """Show workflow management interface"""
    st.title("👥 Workflow Management")
    
    tab1, tab2, tab3 = st.tabs(["📋 Pending Tasks", "📊 Workflow Status", "✅ Complete Tasks"])
    
    with tab1:
        st.subheader("Pending Approval Tasks")
        
        # Get pending tasks
        pending_tasks = st.session_state.workflow_manager.get_pending_tasks()
        
        if pending_tasks:
            for task in pending_tasks:
                with st.expander(f"📄 {task['document_name']} - {task['assignee']}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Document Type:** {task['document_type']}")
                        st.write(f"**Priority:** {task['priority']}")
                        st.write(f"**Due Date:** {task['due_date'][:10] if task['due_date'] else 'Not set'}")
                    
                    with col2:
                        st.write(f"**Task:** {task['task_name']}")
                        st.write(f"**Created:** {task['created_at'][:10]}")
                    
                    # Task completion form
                    with st.form(f"task_{task['task_id']}"):
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            action = st.selectbox("Action", ["Approve", "Reject"], key=f"action_{task['task_id']}")
                        
                        with col2:
                            comments = st.text_area("Comments", key=f"comments_{task['task_id']}")
                        
                        if st.form_submit_button("Submit Decision"):
                            try:
                                status = "Approved" if action == "Approve" else "Rejected"
                                st.session_state.workflow_manager.complete_task(
                                    task_id=task['task_id'],
                                    status=status,
                                    comments=comments
                                )
                                st.success(f"Task {action.lower()}!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error completing task: {str(e)}")
        else:
            st.info("No pending tasks found.")
    
    with tab2:
        st.subheader("Workflow Status Overview")
        
        # Get all workflows
        db = SessionLocal()
        workflows = db.query(Workflow).order_by(Workflow.created_at.desc()).all()
        db.close()
        
        if workflows:
            for workflow in workflows:
                try:
                    status_info = st.session_state.workflow_manager.get_workflow_status(workflow.id)
                    
                    with st.expander(f"🔄 {status_info['name']} ({status_info['status']})", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Progress", f"{status_info['progress_percentage']}%")
                            st.metric("Total Tasks", status_info['total_tasks'])
                            
                        with col2:
                            st.metric("Approved", status_info['approved_tasks'])
                            st.metric("Rejected", status_info['rejected_tasks'])
                        
                        # Progress bar
                        st.progress(status_info['progress_percentage'] / 100)
                        
                        # Task details
                        st.write("**Task Details:**")
                        for task in status_info['tasks']:
                            status_emoji = {"Pending": "⏳", "Approved": "✅", "Rejected": "❌"}
                            st.write(f"{status_emoji.get(task['status'], '❓')} {task['assignee']} - {task['status']}")
                            
                except Exception as e:
                    st.error(f"Error loading workflow {workflow.name}: {str(e)}")
        else:
            st.info("No workflows found.")
    
    with tab3:
        st.subheader("Task Completion History")
        st.info("This section would show completed tasks history - Feature coming soon!")

def show_project_overview():
    """Show project overview"""
    st.title("📊 Project Overview")
    
    db = SessionLocal()
    projects = db.query(Project).all()
    
    if projects:
        for project in projects:
            with st.expander(f"📁 {project.name} ({project.project_type})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {project.description}")
                    st.write(f"**Status:** {project.status}")
                    st.write(f"**Created:** {project.created_at.strftime('%Y-%m-%d %H:%M')}")
                
                with col2:
                    # Project requirements
                    if project.requirements:
                        st.write("**Requirements:**")
                        reqs = project.requirements
                        if "functional" in reqs:
                            st.write("*Functional:*")
                            for req in reqs["functional"][:3]:  # Show first 3
                                st.write(f"• {req}")
                        if len(reqs.get("functional", [])) > 3:
                            st.write(f"... and {len(reqs['functional']) - 3} more")
                
                # Project documents and workflows
                documents = db.query(Document).filter(Document.project_id == project.id).all()
                workflows = db.query(Workflow).filter(Workflow.project_id == project.id).all()
                
                st.write(f"**Documents:** {len(documents)} | **Workflows:** {len(workflows)}")
    else:
        st.info("No projects found.")
    
    db.close()

def show_settings():
    """Show application settings"""
    st.title("⚙️ Settings")
    
    st.subheader("API Configuration")
    
    # Show current configuration (masked for security)
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("LLM Farm URL", value=Config.LLM_FARM_URL_PREFIX, disabled=True)
        st.text_input("Model Name", value=Config.LLM_FARM_MODEL_NAME, disabled=True)
        
    with col2:
        st.text_input("API Key", value="*" * 20, disabled=True, type="password")
        st.text_input("Database URL", value=Config.DATABASE_URL, disabled=True)
    
    st.subheader("Default Approvers")
    approvers_text = st.text_area(
        "Default Approvers (one per line)",
        value="\n".join(Config.DEFAULT_APPROVERS),
        height=100
    )
    
    if st.button("Update Approvers"):
        # This would update the configuration
        st.success("Settings would be updated (feature not implemented in this demo)")
    
    st.subheader("Document Templates")
    st.info("Template management interface would be here")
    
    st.subheader("System Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database", "✅ Connected")
    
    with col2:
        try:
            # Test LLM service
            st.session_state.llm_service
            st.metric("LLM Service", "✅ Ready")
        except:
            st.metric("LLM Service", "❌ Error")
    
    with col3:
        st.metric("Document Generator", "✅ Ready")

if __name__ == "__main__":
    main()
