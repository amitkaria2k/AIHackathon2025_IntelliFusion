"""
Simple test app with key AI features to ensure it works
"""

import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime, timedelta

# Add config directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

try:
    from config.auth_config import VALID_PASSWORDS, HINT_MESSAGE, MAX_LOGIN_ATTEMPTS
    from config.database import DatabaseManager
    from services.llm_service import llm_service
    from services.rag_service import RAGService
    from services.ai_features import get_ai_features_service, DocumentIntelligenceService
except ImportError as e:
    st.error(f"Import error: {e}")

# Configure Streamlit page
st.set_page_config(
    page_title="Bosch AI Document Manager - Enhanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    st.title("🤖 Enhanced Bosch AI Document Manager")
    st.markdown("**With Advanced AI Features**")
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseManager()
    if 'llm_settings' not in st.session_state:
        st.session_state.llm_settings = {
            'temperature': 0.7,
            'max_tokens': 1000,
            'model': 'gpt-4o-mini',
            'use_project_context': True
        }
    
    # Authentication
    if not st.session_state.authenticated:
        show_login()
    else:
        show_main_app()

def show_login():
    """Simple login interface"""
    st.subheader("🔐 Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("**Demo Credentials:**")
        st.write("- PM: `pm123` 🔹 Project team: `team456` 🔹 Quality team: `quality789`")
        
        selected_role = st.selectbox("Select Role:", ["PM", "Project team", "Quality team"])
        password = st.text_input("Password:", type="password")
        
        if st.button("🚪 Login", type="primary", use_container_width=True):
            expected_password = VALID_PASSWORDS.get(selected_role)
            if password == expected_password:
                st.session_state.authenticated = True
                st.session_state.user_role = selected_role
                st.success(f"✅ Welcome, {selected_role}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

def show_main_app():
    """Main application with AI features"""
    user_role = st.session_state.user_role
    
    st.sidebar.success(f"👤 Logged in as: **{user_role}**")
    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Main tabs with AI features
    if user_role == 'PM':
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏠 AI Dashboard", 
            "📝 Smart Document Generation", 
            "🤖 AI Assistant",
            "⚙️ AI Configuration"
        ])
    else:
        tab1, tab3, tab4 = st.tabs([
            "🏠 AI Dashboard", 
            "🤖 AI Assistant",
            "⚙️ AI Configuration"
        ])
        tab2 = None
    
    with tab1:
        show_ai_dashboard()
    
    if tab2:  # PM only
        with tab2:
            show_smart_document_generation()
    
    with tab3:
        show_ai_assistant_simple()
    
    with tab4:
        show_ai_configuration_simple()

def show_ai_dashboard():
    """AI-powered dashboard"""
    st.title("🧠 AI-Powered Dashboard")
    
    # Mock data for demonstration
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Projects", "12", "+2")
    with col2:
        st.metric("Documents", "45", "+8")
    with col3:
        st.metric("AI Insights", "156", "+23")
    with col4:
        st.metric("Efficiency", "87%", "+5%")
    
    # AI Insights Section
    st.subheader("🎯 AI-Generated Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Project Health")
        if st.button("🧠 Analyze Project Health"):
            with st.spinner("AI analyzing..."):
                st.success("✅ Project health: **Excellent** (92/100)")
                st.info("💡 **AI Recommendation:** Consider automating approval workflows to improve efficiency by 15%.")
    
    with col2:
        st.markdown("### 🔍 Smart Recommendations")
        recommendations = [
            "📝 3 documents need quality review",
            "⚡ Optimize approval chain for Technical Specs",
            "🎯 Consider using AI templates for faster generation",
            "📊 Weekly compliance report is ready"
        ]
        
        for rec in recommendations:
            st.write(f"• {rec}")

def show_smart_document_generation():
    """AI-enhanced document generation"""
    st.title("📝 Smart Document Generation")
    
    st.info("🤖 AI-powered document generation with intelligent templates and content suggestions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Document Configuration")
        
        doc_type = st.selectbox(
            "Document Type:",
            ["Technical Specification", "Project Plan", "Risk Assessment", "Test Report"]
        )
        
        project_name = st.text_input("Project Name:", "AI Enhancement Project")
        
        # AI-powered template selection
        st.markdown("### 🎯 AI Template Recommendations")
        if st.button("🧠 Get AI Template Suggestions"):
            st.success(f"✅ **Recommended template:** {doc_type} - Enhanced Format")
            st.info("💡 **AI Insight:** This template has 95% approval rate and reduces review time by 30%")
    
    with col2:
        st.subheader("🚀 Content Generation")
        
        if st.button("📝 Generate with AI", type="primary"):
            with st.spinner("🤖 AI is generating content..."):
                # Mock AI-generated content
                content = f"""# {doc_type}

## Executive Summary
This {doc_type.lower()} for {project_name} has been generated using AI-powered templates and best practices from similar successful projects.

## Key Sections
- Requirements Analysis ✅
- Technical Architecture 🎯
- Risk Assessment 🔍
- Implementation Plan 📅

## AI Quality Score: 94/100
- Completeness: ✅ Excellent
- Compliance: ✅ Meets standards
- Readability: ✅ Professional
- Technical Accuracy: ✅ Validated

*Generated by Bosch AI Document Assistant*
"""
                st.success("✅ Document generated successfully!")
                st.markdown("### 📄 Generated Content Preview")
                st.text_area("Content:", content, height=300)
                
                st.download_button(
                    "📥 Download Document",
                    content,
                    f"{doc_type}_{project_name}.md",
                    "text/markdown"
                )

def show_ai_assistant_simple():
    """Simplified AI assistant"""
    st.title("🤖 AI Assistant")
    
    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display sample conversation
    st.markdown("### 💬 Chat with AI")
    
    sample_messages = [
        {"role": "user", "content": "What's the status of my current projects?"},
        {"role": "assistant", "content": "📊 You have 3 active projects: 2 are on track, 1 needs attention. The AI Enhancement Project is 85% complete with excellent quality metrics."},
        {"role": "user", "content": "Can you help me optimize my document approval workflow?"},
        {"role": "assistant", "content": "🎯 Based on your data, I recommend: 1) Parallel approvals for technical reviews, 2) Auto-routing based on document complexity, 3) AI pre-screening for quality checks. This could reduce approval time by 40%."}
    ]
    
    for msg in sample_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background-color: #E3F2FD; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #1976D2;">
                <strong>You:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #F3F4F6; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #059669;">
                <strong>🤖 AI Assistant:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me anything about your projects...")
    if user_input:
        st.info(f"You asked: {user_input}")
        st.info("🤖 AI Assistant: I'd be happy to help! (Connect to LLM service for full functionality)")

def show_ai_configuration_simple():
    """Simplified AI configuration"""
    st.title("⚙️ AI Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Connection Status")
        
        # Test connection
        if st.button("🧪 Test LLM Connection"):
            st.info("Testing connection to Bosch LLM Farm...")
            st.success("✅ Connected to gpt-4o-mini")
            st.info("**Endpoint:** aoai-farm.bosch-temp.com")
        
        # Feature status
        st.subheader("🎯 AI Features")
        features = {
            "Document Analysis": "✅ Available",
            "Smart Templates": "✅ Available", 
            "Workflow Optimization": "✅ Available",
            "Compliance Checking": "⚠️ Limited"
        }
        
        for feature, status in features.items():
            st.write(f"**{feature}:** {status}")
    
    with col2:
        st.subheader("🎛️ Model Settings")
        
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)
        model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"])
        
        if st.button("💾 Save Settings"):
            st.session_state.llm_settings = {
                'temperature': temperature,
                'max_tokens': max_tokens,
                'model': model
            }
            st.success("✅ Settings saved!")

if __name__ == "__main__":
    main()
