"""
Enhanced AI-Powered Project Documentation Management System
With Bosch Branding, Authentication, Database Persistence, and Chatbot
"""

import streamlit as st
import pandas as pd
import base64
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import sys

# Add config directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from config.auth_config import VALID_PASSWORDS, HINT_MESSAGE, MAX_LOGIN_ATTEMPTS
from config.database import DatabaseManager
from services.llm_service import llm_service

# Configure Streamlit page with Bosch branding
st.set_page_config(
    page_title="Bosch AI Document Manager",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for tab navigation
)

# Bosch Corporate Colors (from brand guidelines)
BOSCH_COLORS = {
    'primary_red': '#DC2626',      # Bosch Red
    'primary_blue': '#1E40AF',     # Bosch Blue  
    'dark_blue': '#1E3A8A',       # Dark Blue
    'gray_dark': '#374151',        # Dark Gray
    'gray_medium': '#6B7280',      # Medium Gray
    'gray_light': '#F3F4F6',      # Light Gray
    'white': '#FFFFFF',
    'success_green': '#059669',
    'warning_orange': '#D97706',
    'error_red': '#DC2626'
}

def load_bosch_logo():
    """Load and encode Bosch logo"""
    logo_path = "data/images/Bosch-Logo.png"
    try:
        with open(logo_path, "rb") as f:
            logo_data = f.read()
        return base64.b64encode(logo_data).decode()
    except FileNotFoundError:
        return None

def apply_bosch_styling():
    """Apply Bosch corporate styling"""
    logo_base64 = load_bosch_logo()
    
    bosch_css = f"""
    <style>
    /* Import Bosch fonts */
    @import url('https://fonts.googleapis.com/css2?family=Arial:wght@400;600;700&display=swap');
    
    /* Main app styling */
    .main .block-container {{
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    
    /* Header styling */
    .bosch-header {{
        background: linear-gradient(135deg, {BOSCH_COLORS['primary_red']} 0%, {BOSCH_COLORS['primary_blue']} 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    .bosch-logo {{
        width: 120px;
        height: auto;
        margin-right: 2rem;
        vertical-align: middle;
    }}
    
    .bosch-title {{
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        display: inline-block;
        vertical-align: middle;
    }}
    
    .bosch-subtitle {{
        font-family: 'Arial', sans-serif;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        background-color: {BOSCH_COLORS['gray_light']};
        border-radius: 10px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 3rem;
        padding: 0 1.5rem;
        background-color: transparent;
        border-radius: 8px;
        color: {BOSCH_COLORS['gray_dark']};
        font-weight: 600;
        font-family: 'Arial', sans-serif;
        border: none;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {BOSCH_COLORS['primary_red']} 0%, {BOSCH_COLORS['primary_blue']} 100%);
        color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {BOSCH_COLORS['primary_blue']};
        color: white;
    }}
    
    /* Button styling */
    .stButton button {{
        background: linear-gradient(135deg, {BOSCH_COLORS['primary_red']} 0%, {BOSCH_COLORS['primary_blue']} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Arial', sans-serif;
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    
    /* Metric styling */
    [data-testid="metric-container"] {{
        background: white;
        border: 1px solid {BOSCH_COLORS['gray_light']};
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    /* Login form styling */
    .login-container {{
        background: white;
        border-radius: 15px;
        padding: 3rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        border: 2px solid {BOSCH_COLORS['primary_blue']};
        max-width: 500px;
        margin: 2rem auto;
    }}
    
    .login-title {{
        color: {BOSCH_COLORS['primary_blue']};
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* Chat interface styling */
    .chat-container {{
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid {BOSCH_COLORS['gray_light']};
        margin-bottom: 1rem;
    }}
    
    .chat-message {{
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-family: 'Arial', sans-serif;
    }}
    
    .chat-user {{
        background: {BOSCH_COLORS['primary_blue']};
        color: white;
        text-align: right;
    }}
    
    .chat-assistant {{
        background: {BOSCH_COLORS['gray_light']};
        color: {BOSCH_COLORS['gray_dark']};
    }}
    
    /* Success/Error messages */
    .stSuccess {{
        background-color: {BOSCH_COLORS['success_green']};
        color: white;
        border-radius: 8px;
    }}
    
    .stError {{
        background-color: {BOSCH_COLORS['error_red']};
        color: white;
        border-radius: 8px;
    }}
    
    .stWarning {{
        background-color: {BOSCH_COLORS['warning_orange']};
        color: white;
        border-radius: 8px;
    }}
    
    /* Hide Streamlit menu and footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """
    
    # Add logo to CSS if available
    if logo_base64:
        bosch_css = bosch_css.replace(
            ".bosch-logo {", 
            f'.bosch-logo {{ content: url("data:image/png;base64,{logo_base64}");'
        )
    
    st.markdown(bosch_css, unsafe_allow_html=True)

def show_bosch_header():
    """Display Bosch branded header"""
    logo_base64 = load_bosch_logo()
    
    if logo_base64:
        header_html = f"""
        <div class="bosch-header">
            <img src="data:image/png;base64,{logo_base64}" class="bosch-logo">
            <div style="display: inline-block; vertical-align: middle;">
                <h1 class="bosch-title">AI Document Manager</h1>
                <p class="bosch-subtitle">Intelligent Project Documentation System</p>
            </div>
        </div>
        """
    else:
        header_html = f"""
        <div class="bosch-header">
            <div>
                <h1 class="bosch-title">🔧 Bosch AI Document Manager</h1>
                <p class="bosch-subtitle">Intelligent Project Documentation System</p>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)

def authenticate_user():
    """Handle user authentication"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.login_attempts = 0
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="login-container">
            <h2 class="login-title">🔧 Bosch Employee Verification</h2>
            <p style="text-align: center; color: #6B7280; margin-bottom: 2rem;">
                Prove that you are a Bosch employee.<br>
                Enter any Bosch Hashtags to login.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            password = st.text_input("Enter Bosch Hashtag:", type="password", placeholder="#BeLikeBosch")
            login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_button:
                if password.lower() in [p.lower() for p in VALID_PASSWORDS]:
                    st.session_state.authenticated = True
                    st.session_state.login_attempts = 0
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    
                    if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
                        st.error(f"❌ Invalid hashtag! {HINT_MESSAGE}")
                    else:
                        remaining = MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts
                        st.error(f"❌ Invalid hashtag! {remaining} attempts remaining.")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
            <p><strong>Valid Hashtags Include:</strong></p>
            <p>#BeLikeBosch | #BoschLife | #InventedForLife | #BoschInnovation | #BoschTech</p>
        </div>
        """, unsafe_allow_html=True)
        
        return False
    
    return True

def initialize_app():
    """Initialize the application"""
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseManager()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'llm_settings' not in st.session_state:
        st.session_state.llm_settings = {
            'temperature': 0.7,
            'max_tokens': 2000,
            'model': 'gpt-4o-mini',
            'use_project_context': True
        }

def load_project_template(uploaded_files):
    """Load project template from uploaded file(s)"""
    if uploaded_files is not None and len(uploaded_files) > 0:
        combined_template = {
            'name': '',
            'type': '',
            'description': '',
            'functional_reqs': [],
            'non_functional_reqs': [],
            'conditions': [],
            'recommended_docs': [],
            'template_content': []
        }
        
        # Import required libraries for file parsing
        try:
            import PyPDF2
            import docx
            from pptx import Presentation
            import pandas as pd
        except ImportError as e:
            st.error(f"Missing required libraries for file parsing: {e}")
            return None
        
        for uploaded_file in uploaded_files:
            try:
                file_extension = uploaded_file.name.lower().split('.')[-1]
                
                if file_extension == 'json':
                    content = json.loads(uploaded_file.read().decode('utf-8'))
                    # Merge JSON content with existing template
                    for key in ['name', 'type', 'description']:
                        if content.get(key) and not combined_template.get(key):
                            combined_template[key] = content[key]
                    
                    for key in ['functional_reqs', 'non_functional_reqs', 'conditions', 'recommended_docs']:
                        if content.get(key):
                            combined_template[key].extend(content[key])
                    
                    st.success(f"✅ JSON template loaded from {uploaded_file.name}")
                    
                elif file_extension in ['txt', 'md']:
                    content = uploaded_file.read().decode('utf-8')
                    combined_template['template_content'].append({
                        'filename': uploaded_file.name,
                        'content': content
                    })
                    st.success(f"✅ Text content loaded from {uploaded_file.name}")
                    
                elif file_extension in ['xlsx', 'xls']:
                    # Extract content from Excel files
                    try:
                        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
                        excel_content = ""
                        for sheet_name, df in excel_data.items():
                            excel_content += f"\n--- Sheet: {sheet_name} ---\n"
                            excel_content += df.to_string(index=False)
                            excel_content += "\n"
                        
                        combined_template['template_content'].append({
                            'filename': uploaded_file.name,
                            'content': excel_content
                        })
                        st.success(f"✅ Excel content extracted from {uploaded_file.name}")
                        
                    except Exception as e:
                        st.warning(f"⚠️ Could not fully parse Excel file {uploaded_file.name}: {str(e)}")
                        combined_template['template_content'].append({
                            'filename': uploaded_file.name,
                            'content': f"Excel file: {uploaded_file.name} (partial parsing error)"
                        })
                    
                elif file_extension in ['docx', 'doc']:
                    # Extract content from Word documents
                    try:
                        if file_extension == 'docx':
                            doc = docx.Document(uploaded_file)
                            word_content = ""
                            for paragraph in doc.paragraphs:
                                word_content += paragraph.text + "\n"
                            
                            # Extract tables
                            for table in doc.tables:
                                word_content += "\n--- Table ---\n"
                                for row in table.rows:
                                    row_text = " | ".join([cell.text for cell in row.cells])
                                    word_content += row_text + "\n"
                            
                            combined_template['template_content'].append({
                                'filename': uploaded_file.name,
                                'content': word_content
                            })
                            st.success(f"✅ Word content extracted from {uploaded_file.name}")
                        else:
                            # .doc files need different handling
                            st.warning(f"⚠️ .doc files require conversion to .docx for full support: {uploaded_file.name}")
                            combined_template['template_content'].append({
                                'filename': uploaded_file.name,
                                'content': f"Word document (.doc): {uploaded_file.name} - Please convert to .docx for full text extraction"
                            })
                            
                    except Exception as e:
                        st.warning(f"⚠️ Could not fully parse Word file {uploaded_file.name}: {str(e)}")
                        combined_template['template_content'].append({
                            'filename': uploaded_file.name,
                            'content': f"Word document: {uploaded_file.name} (parsing error: {str(e)})"
                        })
                    
                elif file_extension in ['pptx', 'ppt']:
                    # Extract content from PowerPoint presentations
                    try:
                        if file_extension == 'pptx':
                            prs = Presentation(uploaded_file)
                            ppt_content = ""
                            for slide_num, slide in enumerate(prs.slides, 1):
                                ppt_content += f"\n--- Slide {slide_num} ---\n"
                                for shape in slide.shapes:
                                    if hasattr(shape, "text"):
                                        ppt_content += shape.text + "\n"
                            
                            combined_template['template_content'].append({
                                'filename': uploaded_file.name,
                                'content': ppt_content
                            })
                            st.success(f"✅ PowerPoint content extracted from {uploaded_file.name}")
                        else:
                            # .ppt files need different handling
                            st.warning(f"⚠️ .ppt files require conversion to .pptx for full support: {uploaded_file.name}")
                            combined_template['template_content'].append({
                                'filename': uploaded_file.name,
                                'content': f"PowerPoint presentation (.ppt): {uploaded_file.name} - Please convert to .pptx for full text extraction"
                            })
                            
                    except Exception as e:
                        st.warning(f"⚠️ Could not fully parse PowerPoint file {uploaded_file.name}: {str(e)}")
                        combined_template['template_content'].append({
                            'filename': uploaded_file.name,
                            'content': f"PowerPoint presentation: {uploaded_file.name} (parsing error: {str(e)})"
                        })
                    
                elif file_extension == 'pdf':
                    # Extract content from PDF files
                    try:
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        pdf_content = ""
                        for page_num, page in enumerate(pdf_reader.pages, 1):
                            pdf_content += f"\n--- Page {page_num} ---\n"
                            pdf_content += page.extract_text() + "\n"
                        
                        combined_template['template_content'].append({
                            'filename': uploaded_file.name,
                            'content': pdf_content
                        })
                        st.success(f"✅ PDF content extracted from {uploaded_file.name} ({len(pdf_reader.pages)} pages)")
                        
                    except Exception as e:
                        st.warning(f"⚠️ Could not fully parse PDF file {uploaded_file.name}: {str(e)}")
                        combined_template['template_content'].append({
                            'filename': uploaded_file.name,
                            'content': f"PDF document: {uploaded_file.name} (parsing error: {str(e)})"
                        })
                    
                else:
                    st.error(f"❌ Unsupported file format: {uploaded_file.name}. Please upload JSON, TXT, MD, Excel, Word, PowerPoint, or PDF files.")
                    
            except Exception as e:
                st.error(f"❌ Error reading file {uploaded_file.name}: {str(e)}")
        
        return combined_template if any([combined_template['name'], combined_template['functional_reqs'], combined_template['template_content']]) else None
    return None

def generate_ai_content(prompt: str, project_context: Optional[Dict] = None) -> str:
    """Generate content using LLM"""
    # Use the new LLM service
    messages = [{"role": "user", "content": prompt}]
    
    result = llm_service.generate_response(
        messages=messages,
        temperature=st.session_state.llm_settings['temperature'],
        max_tokens=st.session_state.llm_settings['max_tokens'],
        use_project_context=st.session_state.llm_settings['use_project_context'],
        project_context=project_context
    )
    
    return result['response']

def main():
    """Main application function"""
    apply_bosch_styling()
    
    # Authentication check
    if not authenticate_user():
        return
    
    show_bosch_header()
    initialize_app()
    
    # Tab navigation instead of sidebar
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🏠 Dashboard", 
        "🆕 New Project", 
        "✏️ Edit Projects",
        "📝 Generate Document", 
        "👥 Workflow Management", 
        "📊 Project Overview",
        "💬 AI Assistant",
        "⚙️ Settings"
    ])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_new_project()
    
    with tab3:
        show_edit_projects()
    
    with tab4:
        show_document_generation()
    
    with tab5:
        show_workflow_management()
    
    with tab6:
        show_project_overview()
    
    with tab7:
        show_ai_assistant()
    
    with tab8:
        show_settings()

def show_dashboard():
    """Display main dashboard with persistent data"""
    st.title("🏠 Dashboard")
    st.markdown("Welcome to the Bosch AI-Powered Project Documentation Management System")
    
    # Force refresh data from database
    if st.button("🔄 Refresh Data", type="secondary"):
        st.rerun()
    
    # Load data from database
    projects = st.session_state.db.get_projects()
    documents = st.session_state.db.get_documents()
    workflows = st.session_state.db.get_workflows()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", len(projects))
    
    with col2:
        st.metric("Generated Documents", len(documents))
        
    with col3:
        active_workflows = len([w for w in workflows if w['status'] == 'Active'])
        st.metric("Active Workflows", active_workflows)
        
    with col4:
        st.metric("Template Types", 12)
    
    # Recent projects
    st.subheader("📊 Recent Projects")
    if projects:
        project_data = []
        for project in projects[:5]:  # Last 5 projects
            project_docs = len([d for d in documents if d['project_id'] == project['id']])
            project_data.append({
                "Name": project["name"],
                "Type": project["type"],
                "Documents": project_docs,
                "Created": project["created_at"][:10] if project["created_at"] else "Today"
            })
        
        df = pd.DataFrame(project_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No projects found. Create your first project!")
    
    # Recent documents
    st.subheader("📄 Recent Documents")
    if documents:
        doc_data = []
        for doc in documents[:5]:
            project = next((p for p in projects if p['id'] == doc['project_id']), None)
            doc_data.append({
                "Document": doc["name"],
                "Project": project["name"] if project else "Unknown",
                "Type": doc["type"],
                "Status": doc["status"],
                "Created": doc["created_at"][:10] if doc["created_at"] else "Today"
            })
        
        df = pd.DataFrame(doc_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No documents generated yet.")
    
    # System status
    st.subheader("🔧 System Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("✅ Application Running")
    
    with col2:
        st.success("✅ Database Connected")
    
    with col3:
        if os.getenv('LLM_FARM_API_KEY'):
            st.success("✅ AI Service Ready")
        else:
            st.warning("⚠️ AI Service (Demo Mode)")

def show_new_project():
    """Show new project creation form with template upload"""
    st.title("🆕 Create New Project")
    
    # Project template upload section
    st.subheader("📁 Project Template(s) (Optional)")
    uploaded_files = st.file_uploader(
        "Upload project template file(s)", 
        type=['json', 'txt', 'md', 'xlsx', 'xls', 'docx', 'doc', 'pptx', 'ppt', 'pdf'],
        help="Upload one or more template files to pre-fill project requirements. Supports: JSON, TXT, Markdown, Excel, Word, PowerPoint, PDF",
        accept_multiple_files=True
    )
    
    template_data = None
    if uploaded_files:
        template_data = load_project_template(uploaded_files)
        if template_data:
            st.success(f"✅ Loaded {len(uploaded_files)} template file(s) successfully!")
            
            with st.expander("📋 Preview combined template content", expanded=False):
                if template_data.get('name'):
                    st.write(f"**Project Name:** {template_data['name']}")
                if template_data.get('type'):
                    st.write(f"**Project Type:** {template_data['type']}")
                if template_data.get('description'):
                    st.write(f"**Description:** {template_data['description']}")
                if template_data.get('functional_reqs'):
                    st.write(f"**Functional Requirements:** {len(template_data['functional_reqs'])} items")
                if template_data.get('non_functional_reqs'):
                    st.write(f"**Non-Functional Requirements:** {len(template_data['non_functional_reqs'])} items")
                if template_data.get('conditions'):
                    st.write(f"**Conditions:** {len(template_data['conditions'])} items")
                if template_data.get('template_content'):
                    st.write(f"**Additional Files:** {len(template_data['template_content'])} files")
                    for file_info in template_data['template_content']:
                        st.write(f"• {file_info['filename']}")
                
                # Show detailed content in JSON format for debugging
                with st.expander("🔍 Detailed Template Data (Debug)", expanded=False):
                    st.json({k: v for k, v in template_data.items() if k != 'template_content'})
    
    st.subheader("📋 Project Information")
    
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
            project_name = st.text_input(
                "Project Name*", 
                value=template_data.get('name', '') if template_data else '',
                placeholder="Enter project name"
            )
            project_type = st.selectbox(
                "Project Type*", 
                project_types,
                index=project_types.index(template_data.get('type', project_types[0])) if template_data and template_data.get('type') in project_types else 0
            )
            
        with col2:
            description = st.text_area(
                "Project Description*", 
                value=template_data.get('description', '') if template_data else '',
                placeholder="Describe your project objectives and scope",
                height=100
            )
        
        # Requirements section
        st.subheader("📝 Requirements & Constraints")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Functional Requirements:**")
            functional_reqs_default = '\n'.join(template_data.get('functional_reqs', [])) if template_data else ""
            functional_reqs = st.text_area(
                "Functional requirements (one per line)",
                value=functional_reqs_default,
                placeholder="System shall meet performance criteria\nSolution shall integrate with existing systems"
            )
            
            st.write("**Non-Functional Requirements:**")
            non_functional_reqs_default = '\n'.join(template_data.get('non_functional_reqs', [])) if template_data else ""
            non_functional_reqs = st.text_area(
                "Non-functional requirements (one per line)",
                value=non_functional_reqs_default,
                placeholder="System shall be available 99.9% of the time\nResponse time shall not exceed 2 seconds"
            )
            
        with col2:
            st.write("**Conditions/Constraints:**")
            conditions_default = '\n'.join(template_data.get('conditions', [])) if template_data else ""
            conditions = st.text_area(
                "Project conditions (one per line)",
                value=conditions_default,
                placeholder="Budget constraints must be observed\nCompliance with company standards required"
            )
            
            st.write("**Document Types to Generate:**")
            document_types = [
                "Project Management Plan (PMP)",
                "Technical Concept Document (TCD)",
                "Configuration Management Plan",
                "Communication Management Plan",
                "Risk Management Plan",
                "Quality Plan"
            ]
            default_docs = template_data.get('recommended_docs', document_types[:3]) if template_data else document_types[:3]
            recommended_docs = st.multiselect(
                "Select document types", 
                document_types, 
                default=default_docs
            )
        
        # Submit project
        submitted = st.form_submit_button("✅ Create Project", type="primary")
        
        if submitted:
            if project_name and project_type and description:
                # Create project
                project = {
                    "name": project_name,
                    "type": project_type,
                    "description": description,
                    "functional_reqs": [req.strip() for req in functional_reqs.split('\n') if req.strip()],
                    "non_functional_reqs": [req.strip() for req in non_functional_reqs.split('\n') if req.strip()],
                    "conditions": [cond.strip() for cond in conditions.split('\n') if cond.strip()],
                    "recommended_docs": recommended_docs
                }
                
                # Save to database
                project_id = st.session_state.db.save_project(project)
                project['id'] = project_id
                
                st.success(f"✅ Project '{project_name}' created successfully!")
                st.info("You can now generate documents for this project in the 'Generate Document' tab.")
                
                # Force refresh to update other tabs
                time.sleep(1)  # Brief pause
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")

def show_edit_projects():
    """Show project editing and deletion interface"""
    st.title("✏️ Edit Projects")
    
    projects = st.session_state.db.get_projects()
    
    if not projects:
        st.warning("No projects found. Create a project first.")
        return
    
    # Create tabs for Edit and Delete
    edit_tab, delete_tab = st.tabs(["✏️ Edit Project", "🗑️ Delete Projects"])
    
    with edit_tab:
        st.subheader("Edit Existing Project")
        
        # Project selection
        project_options = {f"{p['name']} ({p['type']}) - ID: {p['id']}": p for p in projects}
        selected_project_name = st.selectbox(
            "Select Project to Edit:", 
            list(project_options.keys()),
            key="edit_project_select"
        )
        selected_project = project_options[selected_project_name]
        
        if selected_project:
            st.info(f"**Editing Project:** {selected_project['name']} | **Created:** {selected_project.get('created_at', 'Unknown')[:10]}")
            
            # Project template upload section for editing
            st.subheader("📁 Update from Template(s) (Optional)")
            uploaded_files_edit = st.file_uploader(
                "Upload template file(s) to update project", 
                type=['json', 'txt', 'md', 'xlsx', 'xls', 'docx', 'doc', 'pptx', 'ppt', 'pdf'],
                help="Upload one or more template files to update/merge with existing project data. Supports: JSON, TXT, Markdown, Excel, Word, PowerPoint, PDF",
                accept_multiple_files=True,
                key="edit_template_upload"
            )
            
            template_data_edit = None
            if uploaded_files_edit:
                template_data_edit = load_project_template(uploaded_files_edit)
                if template_data_edit:
                    st.success(f"✅ Loaded {len(uploaded_files_edit)} template file(s) for merging!")
                    
                    with st.expander("📋 Preview template updates", expanded=True):
                        st.warning("⚠️ Template data will be merged with existing project data. Existing data will be preserved unless explicitly replaced.")
                        
                        if template_data_edit.get('name'):
                            st.write(f"**New Project Name:** {template_data_edit['name']}")
                        if template_data_edit.get('type'):
                            st.write(f"**New Project Type:** {template_data_edit['type']}")
                        if template_data_edit.get('description'):
                            st.write(f"**New Description:** {template_data_edit['description']}")
                        if template_data_edit.get('functional_reqs'):
                            st.write(f"**Additional Functional Requirements:** {len(template_data_edit['functional_reqs'])} items")
                        if template_data_edit.get('non_functional_reqs'):
                            st.write(f"**Additional Non-Functional Requirements:** {len(template_data_edit['non_functional_reqs'])} items")
                        if template_data_edit.get('conditions'):
                            st.write(f"**Additional Conditions:** {len(template_data_edit['conditions'])} items")
                        if template_data_edit.get('template_content'):
                            st.write(f"**Additional Reference Files:** {len(template_data_edit['template_content'])} files")
            
            with st.form("edit_project_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Merge template name with existing project name
                    merged_name = template_data_edit.get('name', selected_project.get('name', '')) if template_data_edit else selected_project.get('name', '')
                    project_name = st.text_input(
                        "Project Name*", 
                        value=merged_name,
                        placeholder="Enter project name"
                    )
                    
                    project_types = [
                        "Software Development",
                        "Hardware Development", 
                        "Research Project",
                        "Process Improvement",
                        "Product Development",
                        "Custom"
                    ]
                    
                    # Merge template type with existing project type
                    merged_type = template_data_edit.get('type', selected_project.get('type', project_types[0])) if template_data_edit else selected_project.get('type', project_types[0])
                    current_type_index = project_types.index(merged_type) if merged_type in project_types else 0
                    project_type = st.selectbox(
                        "Project Type*", 
                        project_types,
                        index=current_type_index
                    )
                    
                with col2:
                    # Merge template description with existing project description
                    merged_desc = template_data_edit.get('description', selected_project.get('description', '')) if template_data_edit else selected_project.get('description', '')
                    description = st.text_area(
                        "Project Description*", 
                        value=merged_desc,
                        placeholder="Describe your project objectives and scope",
                        height=100
                    )
                
                # Requirements section
                st.subheader("📝 Requirements & Constraints")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Functional Requirements:**")
                    # Merge template functional requirements with existing ones
                    existing_func_reqs = selected_project.get('functional_reqs', [])
                    template_func_reqs = template_data_edit.get('functional_reqs', []) if template_data_edit else []
                    merged_func_reqs = existing_func_reqs + [req for req in template_func_reqs if req not in existing_func_reqs]
                    functional_reqs_text = '\n'.join(merged_func_reqs)
                    functional_reqs = st.text_area(
                        "Functional requirements (one per line)",
                        value=functional_reqs_text,
                        placeholder="System shall meet performance criteria\nSolution shall integrate with existing systems",
                        key="edit_func_reqs"
                    )
                    
                    st.write("**Non-Functional Requirements:**")
                    # Merge template non-functional requirements with existing ones
                    existing_nonfunc_reqs = selected_project.get('non_functional_reqs', [])
                    template_nonfunc_reqs = template_data_edit.get('non_functional_reqs', []) if template_data_edit else []
                    merged_nonfunc_reqs = existing_nonfunc_reqs + [req for req in template_nonfunc_reqs if req not in existing_nonfunc_reqs]
                    non_functional_reqs_text = '\n'.join(merged_nonfunc_reqs)
                    non_functional_reqs = st.text_area(
                        "Non-functional requirements (one per line)",
                        value=non_functional_reqs_text,
                        placeholder="System shall be available 99.9% of the time\nResponse time shall not exceed 2 seconds",
                        key="edit_nonfunc_reqs"
                    )
                    
                with col2:
                    st.write("**Conditions/Constraints:**")
                    # Merge template conditions with existing ones
                    existing_conditions = selected_project.get('conditions', [])
                    template_conditions = template_data_edit.get('conditions', []) if template_data_edit else []
                    merged_conditions = existing_conditions + [cond for cond in template_conditions if cond not in existing_conditions]
                    conditions_text = '\n'.join(merged_conditions)
                    conditions = st.text_area(
                        "Project conditions (one per line)",
                        value=conditions_text,
                        placeholder="Budget constraints must be observed\nCompliance with company standards required",
                        key="edit_conditions"
                    )
                    
                    st.write("**Document Types to Generate:**")
                    document_types = [
                        "Project Management Plan (PMP)",
                        "Technical Concept Document (TCD)",
                        "Configuration Management Plan",
                        "Communication Management Plan",
                        "Risk Management Plan",
                        "Quality Plan"
                    ]
                    recommended_docs = st.multiselect(
                        "Select document types", 
                        document_types, 
                        default=selected_project.get('recommended_docs', []),
                        key="edit_recommended_docs"
                    )
                
                # Submit buttons
                col1, col2 = st.columns(2)
                with col1:
                    update_button = st.form_submit_button("💾 Update Project", type="primary")
                with col2:
                    cancel_button = st.form_submit_button("❌ Cancel Changes")
                
                if update_button:
                    if project_name and project_type and description:
                        # Prepare updates
                        updates = {
                            "name": project_name,
                            "type": project_type,
                            "description": description,
                            "functional_reqs": [req.strip() for req in functional_reqs.split('\n') if req.strip()],
                            "non_functional_reqs": [req.strip() for req in non_functional_reqs.split('\n') if req.strip()],
                            "conditions": [cond.strip() for cond in conditions.split('\n') if cond.strip()],
                            "recommended_docs": recommended_docs
                        }
                        
                        # Update in database
                        st.session_state.db.update_project(selected_project['id'], updates)
                        
                        st.success(f"✅ Project '{project_name}' updated successfully!")
                        st.info("Changes have been saved. Other tabs will reflect the updated information.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields marked with *")
                
                if cancel_button:
                    st.info("Changes cancelled.")
                    st.rerun()
    
    with delete_tab:
        st.subheader("🗑️ Delete Projects")
        st.warning("⚠️ **Warning:** Deleting projects will also remove all associated documents and workflows. This action cannot be undone.")
        
        # Selection mode
        selection_mode = st.radio(
            "Selection Mode:",
            ["Single Project", "Multiple Projects"],
            key="delete_mode"
        )
        
        if selection_mode == "Single Project":
            # Single project deletion
            project_options = {f"{p['name']} ({p['type']}) - ID: {p['id']}": p for p in projects}
            selected_project_name = st.selectbox(
                "Select Project to Delete:", 
                list(project_options.keys()),
                key="single_delete_select"
            )
            selected_project = project_options[selected_project_name]
            
            if selected_project:
                # Show project details
                with st.expander("📋 Project Details", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name:** {selected_project['name']}")
                        st.write(f"**Type:** {selected_project['type']}")
                        st.write(f"**Created:** {selected_project.get('created_at', 'Unknown')[:10]}")
                    with col2:
                        # Count related items
                        documents = st.session_state.db.get_documents(selected_project['id'])
                        workflows = st.session_state.db.get_workflows(selected_project['id'])
                        st.write(f"**Documents:** {len(documents)}")
                        st.write(f"**Workflows:** {len(workflows)}")
                
                # Confirmation
                confirm_delete = st.checkbox(
                    f"I understand that deleting '{selected_project['name']}' will permanently remove all data",
                    key="single_confirm_delete"
                )
                
                if st.button("🗑️ Delete Project", type="secondary", disabled=not confirm_delete):
                    st.session_state.db.delete_project(selected_project['id'])
                    st.success(f"✅ Project '{selected_project['name']}' deleted successfully!")
                    time.sleep(1)
                    st.rerun()
        
        else:
            # Multiple project deletion
            st.write("**Select Multiple Projects to Delete:**")
            
            # Create checkboxes for each project
            selected_projects = []
            for project in projects:
                # Count related items
                documents = st.session_state.db.get_documents(project['id'])
                workflows = st.session_state.db.get_workflows(project['id'])
                
                checkbox_label = f"{project['name']} ({project['type']}) - {len(documents)} docs, {len(workflows)} workflows"
                
                if st.checkbox(checkbox_label, key=f"multi_delete_{project['id']}"):
                    selected_projects.append(project)
            
            if selected_projects:
                st.write(f"**Selected {len(selected_projects)} project(s) for deletion:**")
                for project in selected_projects:
                    st.write(f"• {project['name']} ({project['type']})")
                
                # Confirmation
                confirm_multiple_delete = st.checkbox(
                    f"I understand that deleting these {len(selected_projects)} project(s) will permanently remove all associated data",
                    key="multi_confirm_delete"
                )
                
                if st.button("🗑️ Delete Selected Projects", type="secondary", disabled=not confirm_multiple_delete):
                    project_ids = [p['id'] for p in selected_projects]
                    project_names = [p['name'] for p in selected_projects]
                    
                    st.session_state.db.delete_multiple_projects(project_ids)
                    st.success(f"✅ Deleted {len(selected_projects)} project(s): {', '.join(project_names)}")
                    time.sleep(1)
                    st.rerun()
            else:
                st.info("Select projects using the checkboxes above to enable deletion.")

def show_document_generation():
    """Show document generation interface"""
    st.title("📝 Generate Document")
    
    projects = st.session_state.db.get_projects()
    
    if not projects:
        st.warning("No projects found. Please create a project first.")
        return
    
    # Project selection
    project_options = {f"{p['name']} ({p['type']})": p for p in projects}
    selected_project_name = st.selectbox("Select Project", list(project_options.keys()))
    selected_project = project_options[selected_project_name]
    
    if selected_project:
        st.info(f"**Project:** {selected_project['name']} | **Type:** {selected_project['type']}")
        
        # Template upload section for document generation
        st.subheader("📁 Additional Template Files (Optional)")
        uploaded_template_files = st.file_uploader(
            "Upload additional template files to enhance document generation", 
            type=['json', 'txt', 'md', 'xlsx', 'xls', 'docx', 'doc', 'pptx', 'ppt', 'pdf'],
            help="Upload template files that contain relevant information for document generation. Supports: JSON, TXT, Markdown, Excel, Word, PowerPoint, PDF",
            accept_multiple_files=True,
            key="doc_gen_template_upload"
        )
        
        template_data_doc_gen = None
        if uploaded_template_files:
            template_data_doc_gen = load_project_template(uploaded_template_files)
            if template_data_doc_gen:
                st.success(f"✅ Loaded {len(uploaded_template_files)} template file(s) for document enhancement!")
                
                with st.expander("📋 Preview template content", expanded=False):
                    if template_data_doc_gen.get('template_content'):
                        st.write(f"**Reference Files:** {len(template_data_doc_gen['template_content'])} files loaded")
                        for file_info in template_data_doc_gen['template_content']:
                            filename = file_info.get('filename', 'Unknown')
                            content_preview = file_info.get('content', '')[:200] + "..." if len(file_info.get('content', '')) > 200 else file_info.get('content', '')
                            st.write(f"**{filename}:** {content_preview}")
        
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
                template_name = st.selectbox("Template", ["Default Document", "Bosch Template"])
                
            with col2:
                custom_requirements = st.text_area(
                    "Additional Requirements (optional)",
                    placeholder="Any specific requirements for this document..."
                )
                
                use_ai = st.checkbox("Use AI Generation", value=True, help="Generate content using AI")
            
            generate_button = st.form_submit_button("🚀 Generate Document", type="primary")
            
            if generate_button:
                with st.spinner("Generating document..."):
                    if use_ai:
                        # AI-generated content with template context
                        prompt = f"Generate a {document_type} for a {selected_project['type']} project named '{selected_project['name']}'. {custom_requirements}"
                        
                        # Add template content to AI prompt if available
                        if template_data_doc_gen and template_data_doc_gen.get('template_content'):
                            prompt += "\n\nReference information from uploaded templates:\n"
                            for file_info in template_data_doc_gen['template_content']:
                                filename = file_info.get('filename', 'Unknown')
                                content = file_info.get('content', '')
                                if content and len(content) < 1500:  # Only add shorter content to prompt
                                    prompt += f"\n--- From {filename} ---\n{content}\n"
                        
                        content = generate_ai_content(prompt, selected_project)
                    else:
                        # Template-based content with uploaded template data
                        content = generate_template_content(document_type, selected_project, custom_requirements.split('\n') if custom_requirements else [], template_data_doc_gen)
                    
                    # Save document to database
                    document = {
                        "project_id": selected_project["id"],
                        "name": f"{document_type}_{selected_project['name']}",
                        "type": document_type,
                        "content": content,
                        "status": "Draft"
                    }
                    
                    document_id = st.session_state.db.save_document(document)
                    document["id"] = document_id
                    
                    # Create workflow
                    workflow = {
                        "project_id": selected_project["id"],
                        "document_id": document_id,
                        "name": f"{document_type} Review",
                        "status": "Active",
                        "approvers": ["Project Manager", "Technical Lead", "Quality Assurance"],
                        "current_step": 0
                    }
                    
                    workflow_id = st.session_state.db.save_workflow(workflow)
                    
                    st.success("✅ Document generated successfully!")
                    st.success("🔄 Approval workflow created!")
                    
                    # Display generated content preview
                    st.subheader("📄 Document Preview")
                    with st.expander("Show generated content", expanded=True):
                        st.markdown(content)

def generate_template_content(document_type: str, project: Dict, additional_reqs: List[str], template_data: Optional[Dict] = None) -> str:
    """Generate template-based content with optional template file content"""
    content = f"""# {document_type}

## Project Overview
**Project Name:** {project.get('name', 'Not specified')}
**Project Type:** {project.get('type', 'Not specified')}
**Description:** {project.get('description', 'Not specified')}

## Executive Summary
This document outlines the {document_type.lower()} for the {project.get('name', 'project')} project.
"""

    # Add template file content if available
    if template_data and template_data.get('template_content'):
        content += "\n## Reference Information from Template Files\n"
        for file_info in template_data['template_content']:
            filename = file_info.get('filename', 'Unknown file')
            file_content = file_info.get('content', '')
            
            # Only include meaningful content (not error messages)
            if file_content and not file_content.startswith(('Excel file:', 'Word document:', 'PowerPoint presentation:', 'PDF document:')):
                content += f"\n### Content from {filename}\n"
                # Limit content length for readability
                if len(file_content) > 2000:
                    content += file_content[:2000] + "\n... [Content truncated for brevity]\n"
                else:
                    content += file_content + "\n"

    content += "\n## Requirements\n\n### Functional Requirements\n"
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
    
    content += f"""
## Implementation Plan
- **Phase 1:** Planning and Design
- **Phase 2:** Development and Testing
- **Phase 3:** Deployment and Monitoring

## Risk Management
Identified risks and mitigation strategies will be documented as the project progresses.

## Timeline
Project timeline and milestones to be established based on requirements analysis.

## Quality Assurance
Quality gates and testing procedures will ensure deliverable meets Bosch standards.

## Approval
This document requires review and approval from designated stakeholders.

---
*Generated by Bosch AI Document Manager - {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    return content

def show_workflow_management():
    """Show workflow management interface"""
    st.title("👥 Workflow Management")
    
    workflows = st.session_state.db.get_workflows()
    documents = st.session_state.db.get_documents()
    
    tab1, tab2 = st.tabs(["📋 Pending Tasks", "📊 Workflow Status"])
    
    with tab1:
        st.subheader("Pending Approval Tasks")
        
        pending_workflows = [w for w in workflows if w["status"] == "Active"]
        
        if pending_workflows:
            for workflow in pending_workflows:
                document = next((d for d in documents if d["id"] == workflow["document_id"]), None)
                
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
                        
                        with st.form(f"task_{workflow['id']}"):
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                action = st.selectbox("Action", ["Approve", "Reject"], key=f"action_{workflow['id']}")
                            
                            with col2:
                                comments = st.text_area(
                                    "Comments", 
                                    key=f"comments_{workflow['id']}",
                                    placeholder="Add your comments about this decision..."
                                )
                            
                            if st.form_submit_button("Submit Decision"):
                                current_approver = workflow["approvers"][workflow["current_step"]]
                                
                                # Add comment to workflow history
                                st.session_state.db.add_workflow_comment(
                                    workflow['id'], 
                                    current_approver, 
                                    action, 
                                    comments
                                )
                                
                                if action == "Approve":
                                    new_step = workflow["current_step"] + 1
                                    if new_step >= len(workflow["approvers"]):
                                        # Workflow complete
                                        st.session_state.db.update_workflow(
                                            workflow['id'], 
                                            {'status': 'Completed', 'current_step': new_step}
                                        )
                                        st.session_state.db.update_document(
                                            document['id'], 
                                            {'status': 'Approved'}
                                        )
                                        st.success("✅ Document fully approved!")
                                    else:
                                        # Move to next step
                                        st.session_state.db.update_workflow(
                                            workflow['id'], 
                                            {'current_step': new_step}
                                        )
                                        next_approver = workflow['approvers'][new_step]
                                        st.success(f"✅ Approved! Moving to next approver: {next_approver}")
                                else:
                                    # Reject workflow
                                    st.session_state.db.update_workflow(
                                        workflow['id'], 
                                        {'status': 'Rejected'}
                                    )
                                    st.session_state.db.update_document(
                                        document['id'], 
                                        {'status': 'Rejected'}
                                    )
                                    st.error("❌ Document rejected!")
                                
                                st.rerun()
        else:
            st.info("No pending approval tasks found.")
    
    with tab2:
        st.subheader("Workflow Status Overview")
        
        if workflows:
            for workflow in workflows:
                document = next((d for d in documents if d["id"] == workflow["document_id"]), None)
                
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
                        
                        st.progress(progress / 100)
                        
                        st.write("**Approval Chain:**")
                        for i, approver in enumerate(workflow["approvers"]):
                            if i < workflow["current_step"]:
                                st.write(f"✅ {approver}")
                            elif i == workflow["current_step"] and workflow["status"] == "Active":
                                st.write(f"⏳ {approver} (Current)")
                            else:
                                st.write(f"⏸️ {approver}")
                        
                        # Workflow comments
                        workflow_comments = st.session_state.db.get_workflow_comments(workflow['id'])
                        if workflow_comments:
                            st.write("**📝 Comments History:**")
                            for comment in workflow_comments:
                                action_emoji = "✅" if comment['action'] == "Approve" else "❌"
                                comment_date = comment['created_at'][:16] if comment['created_at'] else "Unknown"
                                
                                with st.expander(f"{action_emoji} {comment['approver']} - {comment['action']} ({comment_date})", expanded=False):
                                    if comment['comment']:
                                        st.write(f"**Comment:** {comment['comment']}")
                                    else:
                                        st.write("*No comment provided*")
                        else:
                            st.write("**📝 Comments:** No comments yet")
        else:
            st.info("No workflows found.")

def show_project_overview():
    """Show project overview"""
    st.title("📊 Project Overview")
    
    projects = st.session_state.db.get_projects()
    documents = st.session_state.db.get_documents()
    workflows = st.session_state.db.get_workflows()
    
    if projects:
        for project in projects:
            project_documents = [d for d in documents if d["project_id"] == project["id"]]
            project_workflows = [w for w in workflows if w["project_id"] == project["id"]]
            
            with st.expander(f"📁 {project['name']} ({project['type']})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {project['description']}")
                    st.write(f"**Created:** {project['created_at'][:10] if project['created_at'] else 'Unknown'}")
                
                with col2:
                    if project.get('functional_reqs'):
                        st.write("**Functional Requirements:**")
                        for req in project['functional_reqs'][:3]:
                            st.write(f"• {req}")
                        if len(project['functional_reqs']) > 3:
                            st.write(f"... and {len(project['functional_reqs']) - 3} more")
                
                st.write(f"**Documents:** {len(project_documents)} | **Workflows:** {len(project_workflows)}")
                
                if project_documents:
                    st.write("**Recent Documents:**")
                    for doc in project_documents[-3:]:
                        status_emoji = {"Draft": "📄", "Under Review": "🔍", "Approved": "✅", "Rejected": "❌"}
                        st.write(f"{status_emoji.get(doc['status'], '📄')} {doc['name']} - {doc['status']}")
    else:
        st.info("No projects found.")

def show_ai_assistant():
    """Show AI chatbot interface with configuration"""
    st.title("💬 AI Assistant")
    
    # Create three columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("🤖 AI Configuration")
        
        # Test API connection
        with st.expander("🔧 Connection Status", expanded=True):
            if st.button("🧪 Test Connection"):
                with st.spinner("Testing connection to Bosch LLM Farm..."):
                    connection_result = llm_service.test_connection()
                    
                    if connection_result['success']:
                        st.success(f"✅ {connection_result['message']}")
                        st.info(f"**Model:** {connection_result['model']}")
                        st.info(f"**Endpoint:** {connection_result['endpoint']}")
                    else:
                        st.error(f"❌ {connection_result['error']}")
                        st.warning(connection_result['details'])
        
        # LLM Configuration
        with st.form("llm_config_form"):
            st.write("**Model Settings:**")
            
            temperature = st.slider(
                "Temperature", 
                min_value=0.0, 
                max_value=2.0, 
                value=st.session_state.llm_settings['temperature'],
                step=0.1,
                help="Higher values make output more creative"
            )
            
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=100,
                max_value=4000,
                value=st.session_state.llm_settings['max_tokens'],
                step=100,
                help="Maximum response length"
            )
            
            model = st.selectbox(
                "Model",
                ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
                index=["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"].index(st.session_state.llm_settings['model'])
            )
            
            st.write("**Context Options:**")
            use_project_context = st.radio(
                "Response Mode:",
                ["Use Project Context (Augmented)", "LLM Response As-Is"],
                index=0 if st.session_state.llm_settings['use_project_context'] else 1,
                help="Choose whether to include project information in responses"
            )
            
            if st.form_submit_button("💾 Save Settings"):
                st.session_state.llm_settings = {
                    'temperature': temperature,
                    'max_tokens': max_tokens,
                    'model': model,
                    'use_project_context': use_project_context == "Use Project Context (Augmented)"
                }
                st.success("✅ Settings saved!")
                st.rerun()
    
    with col1:
        st.markdown("Chat with the AI assistant about your projects and documentation needs.")
        
        # Project context selection
        projects = st.session_state.db.get_projects()
        
        col_a, col_b = st.columns([3, 1])
        with col_a:
            if projects:
                project_options = {f"{p['name']} ({p['type']})": p for p in projects}
                project_options["None (General Chat)"] = None
                selected_context = st.selectbox(
                    "Select Project Context:", 
                    list(project_options.keys()),
                    help="Choose a project to provide context (only works in 'Use Project Context' mode)"
                )
                current_project = project_options[selected_context]
            else:
                current_project = None
                st.info("No projects available for context.")
        
        with col_b:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        
        # Display current settings status
        context_mode = "🔗 Project Context" if st.session_state.llm_settings['use_project_context'] else "🤖 LLM As-Is"
        st.info(f"**Mode:** {context_mode} | **Model:** {st.session_state.llm_settings['model']} | **Temp:** {st.session_state.llm_settings['temperature']}")
        
        # Display chat history
        st.subheader("💭 Conversation")
        
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message chat-user">
                        <strong>You:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Show if response was from API or fallback
                    api_indicator = ""
                    if message.get("is_fallback", False):
                        api_indicator = " <span style='color: orange;'>(Demo Mode)</span>"
                    elif message.get("from_api", False):
                        api_indicator = " <span style='color: green;'>(Bosch LLM)</span>"
                    
                    st.markdown(f"""
                    <div class="chat-message chat-assistant">
                        <strong>AI Assistant{api_indicator}:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Ask me anything about your projects or documentation:",
                placeholder="e.g., 'Help me create a risk management plan for my software project'",
                height=100
            )
            
            col_x, col_y = st.columns([3, 1])
            with col_x:
                send_button = st.form_submit_button("📤 Send", type="primary")
            with col_y:
                test_button = st.form_submit_button("🧪 Test API")
            
            if send_button and user_input.strip():
                # Add user message to history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Generate AI response
                with st.spinner("AI is thinking..."):
                    messages = [{"role": "user", "content": user_input}]
                    
                    result = llm_service.generate_response(
                        messages=messages,
                        temperature=st.session_state.llm_settings['temperature'],
                        max_tokens=st.session_state.llm_settings['max_tokens'],
                        use_project_context=st.session_state.llm_settings['use_project_context'],
                        project_context=current_project
                    )
                    
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": result['response'],
                        "is_fallback": result.get('is_fallback', False),
                        "from_api": result.get('success', False)
                    })
                
                st.rerun()
            
            if test_button:
                with st.spinner("Testing API connection..."):
                    test_result = llm_service.test_connection()
                    if test_result['success']:
                        st.success("✅ API connection successful!")
                    else:
                        st.error(f"❌ API test failed: {test_result['error']}")
                st.rerun()

def show_settings():
    """Show application settings"""
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["🔧 System Settings", "📊 Data Management", "🚪 Session"])
    
    with tab1:
        st.subheader("System Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Database", "SQLite")
        
        with col2:
            st.metric("Storage", "Persistent")
        
        with col3:
            if os.getenv('LLM_FARM_API_KEY'):
                st.metric("AI Service", "Connected")
            else:
                st.metric("AI Service", "Demo Mode")
        
        st.subheader("API Configuration")
        
        api_status = "✅ Configured" if os.getenv('LLM_FARM_API_KEY') else "❌ Not Configured"
        st.write(f"**Bosch LLM Farm API:** {api_status}")
        
        if not os.getenv('LLM_FARM_API_KEY'):
            st.warning("Configure your .env file to enable full AI features:")
            st.code("""
# Add to .env file:
LLM_FARM_URL_PREFIX = "https://aoai-farm.bosch-temp.com/api/"
LLM_FARM_API_KEY = "your-api-key-here"
            """)
    
    with tab3:
        st.subheader("Data Management")
        
        # Database statistics
        projects = st.session_state.db.get_projects()
        documents = st.session_state.db.get_documents()
        workflows = st.session_state.db.get_workflows()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Projects", len(projects))
        
        with col2:
            st.metric("Documents", len(documents))
        
        with col3:
            st.metric("Workflows", len(workflows))
        
        st.subheader("Database Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Data", type="secondary"):
                export_data = {
                    'projects': projects,
                    'documents': documents,
                    'workflows': workflows,
                    'exported_at': datetime.now().isoformat()
                }
                
                st.download_button(
                    label="⬇️ Download Export",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"bosch_projects_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Load Sample Data", type="secondary"):
                # Add sample data
                sample_project = {
                    "name": "Bosch IoT Platform",
                    "type": "Software Development",
                    "description": "Next-generation IoT platform for connected devices",
                    "functional_reqs": ["System shall handle 1M+ concurrent connections", "Real-time data processing"],
                    "non_functional_reqs": ["99.9% uptime", "Sub-100ms response time"],
                    "conditions": ["GDPR compliance required", "Bosch security standards"],
                    "recommended_docs": ["Project Management Plan (PMP)", "Technical Concept Document (TCD)"]
                }
                
                project_id = st.session_state.db.save_project(sample_project)
                st.success("Sample data loaded!")
                st.rerun()
    
    with tab3:
        st.subheader("Session Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚪 Logout", type="secondary"):
                st.session_state.authenticated = False
                st.session_state.login_attempts = 0
                st.rerun()
        
        with col2:
            if st.button("🔄 Restart App", type="secondary"):
                st.rerun()
        
        st.subheader("Session Information")
        st.write(f"**Authenticated:** {st.session_state.get('authenticated', False)}")
        st.write(f"**Chat Messages:** {len(st.session_state.get('chat_history', []))}")
        st.write(f"**Current Model:** {st.session_state.llm_settings['model']}")

if __name__ == "__main__":
    main()
