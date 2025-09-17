"""
AI-Powered Project Documentation Management System
Simplified Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from typing import Dict, List

# Configure Streamlit page
st.set_page_config(
    page_title="AI Project Documentation Manager",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_app():
    """Initialize the application"""
    # Initialize session state for data storage (in-memory)
    if 'projects' not in st.session_state:
        st.session_state.projects = []
    
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    
    if 'workflows' not in st.session_state:
        st.session_state.workflows = []

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
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", len(st.session_state.projects))
    
    with col2:
        st.metric("Generated Documents", len(st.session_state.documents))
        
    with col3:
        st.metric("Active Workflows", len(st.session_state.workflows))
        
    with col4:
        st.metric("Template Types", 12)
    
    # Recent projects
    st.subheader("Recent Projects")
    if st.session_state.projects:
        project_data = []
        for project in st.session_state.projects[-5:]:  # Last 5 projects
            project_data.append({
                "Name": project["name"],
                "Type": project["type"],
                "Status": "Active",
                "Created": "Today"
            })
        
        df = pd.DataFrame(project_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No projects found. Create your first project!")
    
    # Status info
    st.subheader("System Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("✅ Application Running")
    
    with col2:
        st.info("⚠️ Demo Mode (No Database)")
    
    with col3:
        st.warning("🔑 API Keys Not Configured")

def show_new_project():
    """Show new project creation form"""
    st.title("🆕 Create New Project")
    
    project_types = [
        "Software Development",
        "Hardware Development", 
        "Research Project",
        "Process Improvement",
        "Product Development",
        "Custom"
    ]
    
    with st.form("new_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name*", placeholder="Enter project name")
            project_type = st.selectbox("Project Type*", project_types)
            
        with col2:
            description = st.text_area("Project Description*", 
                                     placeholder="Describe your project objectives and scope",
                                     height=100)
        
        # AI-generated suggestions (simplified)
        st.subheader("Requirements & Suggestions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Functional Requirements:**")
            functional_reqs = st.text_area("Functional requirements (one per line)",
                                         placeholder="System shall meet performance criteria\nSolution shall integrate with existing systems")
            
            st.write("**Non-Functional Requirements:**")
            non_functional_reqs = st.text_area("Non-functional requirements (one per line)",
                                             placeholder="System shall be available 99.9% of the time\nResponse time shall not exceed 2 seconds")
            
        with col2:
            st.write("**Conditions/Constraints:**")
            conditions = st.text_area("Project conditions (one per line)",
                                    placeholder="Budget constraints must be observed\nCompliance with company standards required")
            
            st.write("**Document Types to Generate:**")
            document_types = [
                "Project Management Plan (PMP)",
                "Technical Concept Document (TCD)",
                "Configuration Management Plan",
                "Communication Management Plan",
                "Risk Management Plan",
                "Quality Plan"
            ]
            recommended_docs = st.multiselect("Select document types", document_types, default=document_types[:3])
        
        # Submit project
        submitted = st.form_submit_button("✅ Create Project", type="primary")
        
        if submitted:
            if project_name and project_type and description:
                # Create project (in-memory storage)
                project = {
                    "id": len(st.session_state.projects) + 1,
                    "name": project_name,
                    "type": project_type,
                    "description": description,
                    "functional_reqs": [req.strip() for req in functional_reqs.split('\n') if req.strip()],
                    "non_functional_reqs": [req.strip() for req in non_functional_reqs.split('\n') if req.strip()],
                    "conditions": [cond.strip() for cond in conditions.split('\n') if cond.strip()],
                    "recommended_docs": recommended_docs
                }
                
                st.session_state.projects.append(project)
                
                st.success(f"✅ Project '{project_name}' created successfully!")
                st.info("You can now generate documents for this project in the 'Generate Document' section.")
            else:
                st.error("Please fill in all required fields marked with *")

def show_document_generation():
    """Show document generation interface"""
    st.title("📝 Generate Document")
    
    if not st.session_state.projects:
        st.warning("No projects found. Please create a project first.")
        return
    
    # Project selection
    project_names = [f"{p['name']} ({p['type']})" for p in st.session_state.projects]
    selected_project_name = st.selectbox("Select Project", project_names)
    
    if selected_project_name:
        # Find selected project
        selected_project = None
        for project in st.session_state.projects:
            if f"{project['name']} ({project['type']})" == selected_project_name:
                selected_project = project
                break
        
        if selected_project:
            st.info(f"**Project:** {selected_project['name']} | **Type:** {selected_project['type']}")
            
            with st.form("document_generation_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    document_types = [
                        "Project Management Plan (PMP)",
                        "Technical Concept Document (TCD)",
                        "Configuration Management Plan",
                        "Communication Management Plan",
                        "Risk Management Plan",
                        "Quality Plan",
                        "Requirements Document",
                        "Architecture Document"
                    ]
                    document_type = st.selectbox("Document Type", document_types)
                    template_name = st.selectbox("Template", ["Default Word Document", "HTML Template"])
                    
                with col2:
                    custom_requirements = st.text_area(
                        "Additional Requirements (optional)",
                        placeholder="Any specific requirements for this document..."
                    )
                
                generate_button = st.form_submit_button("🚀 Generate Document", type="primary")
                
                if generate_button:
                    with st.spinner("Generating document..."):
                        # Generate document content (simplified)
                        content = generate_fallback_content(
                            document_type, 
                            selected_project, 
                            custom_requirements.split('\n') if custom_requirements else []
                        )
                        
                        # Store document
                        document = {
                            "id": len(st.session_state.documents) + 1,
                            "project_id": selected_project["id"],
                            "name": f"{document_type}_{selected_project['name']}",
                            "type": document_type,
                            "content": content,
                            "status": "Draft"
                        }
                        
                        st.session_state.documents.append(document)
                        
                        # Create workflow
                        workflow = {
                            "id": len(st.session_state.workflows) + 1,
                            "project_id": selected_project["id"],
                            "document_id": document["id"],
                            "name": f"{document_type} Review",
                            "status": "Active",
                            "approvers": ["Project Manager", "Technical Lead", "Quality Assurance"],
                            "current_step": 0
                        }
                        
                        st.session_state.workflows.append(workflow)
                        
                        st.success("✅ Document generated successfully!")
                        st.success("🔄 Approval workflow created!")
                        
                        # Display generated content preview
                        st.subheader("Document Preview")
                        with st.expander("Show generated content", expanded=True):
                            st.markdown(content)

def generate_fallback_content(document_type: str, project: Dict, additional_reqs: List[str]) -> str:
    """Generate fallback content when AI service is not available"""
    content = f"""# {document_type}

## Project Overview
**Project Name:** {project.get('name', 'Not specified')}
**Project Type:** {project.get('type', 'Not specified')}
**Description:** {project.get('description', 'Not specified')}

## Executive Summary
This document outlines the {document_type.lower()} for the {project.get('name', 'project')} project.

## Requirements

### Functional Requirements
"""
    if project.get('functional_reqs'):
        for i, req in enumerate(project['functional_reqs'], 1):
            content += f"{i}. {req}\n"
    else:
        content += "1. System shall meet specified performance criteria\n"
        content += "2. Solution shall integrate with existing systems\n"
    
    content += "\n### Non-Functional Requirements\n"
    if project.get('non_functional_reqs'):
        for i, req in enumerate(project['non_functional_reqs'], 1):
            content += f"{i}. {req}\n"
    else:
        content += "1. System shall be available 99.9% of the time\n"
        content += "2. Response time shall not exceed 2 seconds\n"
    
    if additional_reqs:
        content += "\n### Additional Requirements\n"
        for i, req in enumerate(additional_reqs, 1):
            if req.strip():
                content += f"{i}. {req.strip()}\n"
    
    content += """
## Implementation Plan
- **Phase 1:** Planning and Design
- **Phase 2:** Development and Testing
- **Phase 3:** Deployment and Monitoring

## Risk Management
Identified risks and mitigation strategies will be documented as the project progresses.

## Timeline
Project timeline and milestones to be established based on requirements analysis.

## Quality Assurance
Quality gates and testing procedures will ensure deliverable meets specifications.

## Approval
This document requires review and approval from designated stakeholders.

---
*This document was generated automatically. Please review and update as needed.*
"""
    return content

def show_workflow_management():
    """Show workflow management interface"""
    st.title("👥 Workflow Management")
    
    tab1, tab2 = st.tabs(["📋 Pending Tasks", "📊 Workflow Status"])
    
    with tab1:
        st.subheader("Pending Approval Tasks")
        
        # Get pending workflows
        pending_workflows = [w for w in st.session_state.workflows if w["status"] == "Active"]
        
        if pending_workflows:
            for workflow in pending_workflows:
                # Find document
                document = next((d for d in st.session_state.documents if d["id"] == workflow["document_id"]), None)
                
                if document:
                    current_approver = workflow["approvers"][workflow["current_step"]]
                    
                    with st.expander(f"📄 {document['name']} - {current_approver}", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Document Type:** {document['type']}")
                            st.write(f"**Current Approver:** {current_approver}")
                            st.write(f"**Step:** {workflow['current_step'] + 1} of {len(workflow['approvers'])}")
                        
                        with col2:
                            st.write(f"**Workflow:** {workflow['name']}")
                            st.write(f"**Status:** {workflow['status']}")
                        
                        # Task completion form
                        with st.form(f"task_{workflow['id']}"):
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                action = st.selectbox("Action", ["Approve", "Reject"], key=f"action_{workflow['id']}")
                            
                            with col2:
                                comments = st.text_area("Comments", key=f"comments_{workflow['id']}")
                            
                            if st.form_submit_button("Submit Decision"):
                                if action == "Approve":
                                    workflow["current_step"] += 1
                                    if workflow["current_step"] >= len(workflow["approvers"]):
                                        workflow["status"] = "Completed"
                                        document["status"] = "Approved"
                                        st.success("Document fully approved!")
                                    else:
                                        st.success(f"Approved! Moving to next approver: {workflow['approvers'][workflow['current_step']]}")
                                else:
                                    workflow["status"] = "Rejected"
                                    document["status"] = "Rejected"
                                    st.error("Document rejected!")
                                
                                st.rerun()
        else:
            st.info("No pending approval tasks found.")
    
    with tab2:
        st.subheader("Workflow Status Overview")
        
        if st.session_state.workflows:
            for workflow in st.session_state.workflows:
                document = next((d for d in st.session_state.documents if d["id"] == workflow["document_id"]), None)
                
                if document:
                    progress = (workflow["current_step"] / len(workflow["approvers"]) * 100) if workflow["status"] != "Completed" else 100
                    
                    with st.expander(f"🔄 {workflow['name']} ({workflow['status']})", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Progress", f"{progress:.0f}%")
                            st.metric("Current Step", f"{workflow['current_step'] + 1} of {len(workflow['approvers'])}")
                            
                        with col2:
                            st.metric("Document", document["name"])
                            st.metric("Status", document["status"])
                        
                        # Progress bar
                        st.progress(progress / 100)
                        
                        # Approver list
                        st.write("**Approval Chain:**")
                        for i, approver in enumerate(workflow["approvers"]):
                            if i < workflow["current_step"]:
                                st.write(f"✅ {approver}")
                            elif i == workflow["current_step"] and workflow["status"] == "Active":
                                st.write(f"⏳ {approver} (Current)")
                            else:
                                st.write(f"⏸️ {approver}")
        else:
            st.info("No workflows found.")

def show_project_overview():
    """Show project overview"""
    st.title("📊 Project Overview")
    
    if st.session_state.projects:
        for project in st.session_state.projects:
            with st.expander(f"📁 {project['name']} ({project['type']})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {project['description']}")
                    st.write(f"**Status:** Active")
                
                with col2:
                    # Project requirements
                    if project.get('functional_reqs'):
                        st.write("**Functional Requirements:**")
                        for req in project['functional_reqs'][:3]:  # Show first 3
                            st.write(f"• {req}")
                        if len(project['functional_reqs']) > 3:
                            st.write(f"... and {len(project['functional_reqs']) - 3} more")
                
                # Project documents and workflows
                project_documents = [d for d in st.session_state.documents if d["project_id"] == project["id"]]
                project_workflows = [w for w in st.session_state.workflows if w["project_id"] == project["id"]]
                
                st.write(f"**Documents:** {len(project_documents)} | **Workflows:** {len(project_workflows)}")
                
                if project_documents:
                    st.write("**Recent Documents:**")
                    for doc in project_documents[-3:]:  # Show last 3
                        status_emoji = {"Draft": "📄", "Under Review": "🔍", "Approved": "✅", "Rejected": "❌"}
                        st.write(f"{status_emoji.get(doc['status'], '📄')} {doc['name']} - {doc['status']}")
    else:
        st.info("No projects found.")

def show_settings():
    """Show application settings"""
    st.title("⚙️ Settings")
    
    st.subheader("Application Mode")
    st.info("Currently running in **Demo Mode** - all data is stored in memory and will be lost when the session ends.")
    
    st.subheader("API Configuration")
    st.warning("API integration is disabled in demo mode. Configure your .env file to enable AI features:")
    
    # Show configuration template
    st.code("""
# Add to .env file:
LLM_FARM_URL_PREFIX = "https://aoai-farm.bosch-temp.com/api/"
LLM_FARM_API_KEY = "your-api-key-here"
DATABASE_URL = "sqlite:///project_docs.db"
    """)
    
    st.subheader("Default Approvers")
    approvers_list = ["Project Manager", "Technical Lead", "Quality Assurance"]
    st.write("Current default approvers:")
    for approver in approvers_list:
        st.write(f"• {approver}")
    
    st.subheader("System Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mode", "Demo")
    
    with col2:
        st.metric("Storage", "In-Memory")
    
    with col3:
        st.metric("AI Features", "Disabled")
    
    # Data management
    st.subheader("Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear All Data", type="secondary"):
            st.session_state.projects = []
            st.session_state.documents = []
            st.session_state.workflows = []
            st.success("All data cleared!")
            st.rerun()
    
    with col2:
        if st.button("Load Sample Data", type="secondary"):
            # Add sample data
            sample_project = {
                "id": 1,
                "name": "Sample AI Project",
                "type": "Software Development",
                "description": "A sample project demonstrating the documentation system",
                "functional_reqs": ["System shall be user-friendly", "System shall be scalable"],
                "non_functional_reqs": ["High availability required"],
                "conditions": ["Budget constraints apply"],
                "recommended_docs": ["Project Management Plan (PMP)"]
            }
            st.session_state.projects = [sample_project]
            st.success("Sample data loaded!")
            st.rerun()

if __name__ == "__main__":
    main()
