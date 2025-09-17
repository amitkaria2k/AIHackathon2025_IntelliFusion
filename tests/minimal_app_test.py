import streamlit as st
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

st.set_page_config(page_title="Minimal App Test", page_icon="🔧")

def test_authentication():
    try:
        from config.auth_config import VALID_PASSWORDS, HINT_MESSAGE, MAX_LOGIN_ATTEMPTS
        
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
            st.session_state.login_attempts = 0
        
        if not st.session_state.authenticated:
            st.title("🔧 Bosch Employee Verification")
            st.write("Please enter a Bosch hashtag to continue")
            
            with st.form("login_form"):
                password = st.text_input("Enter Bosch Hashtag:", type="password", placeholder="#BeLikeBosch")
                login_button = st.form_submit_button("🚀 Login")
                
                if login_button:
                    if password.lower() in [p.lower() for p in VALID_PASSWORDS]:
                        st.session_state.authenticated = True
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid hashtag")
        else:
            return True
        
        return False
        
    except Exception as e:
        st.error(f"Authentication Error: {str(e)}")
        st.exception(e)
        return False

def test_database():
    try:
        from config.database import DatabaseManager
        if 'db' not in st.session_state:
            st.session_state.db = DatabaseManager()
        st.success("✅ Database initialized successfully")
        return True
    except Exception as e:
        st.error(f"Database Error: {str(e)}")
        st.exception(e)
        return False

def test_rag():
    try:
        from services.rag_service import RAGService
        if 'rag_service' not in st.session_state:
            st.session_state.rag_service = RAGService(st.session_state.db)
        st.success("✅ RAG service initialized successfully")
        return True
    except Exception as e:
        st.error(f"RAG Service Error: {str(e)}")
        st.exception(e)
        return False

def main():
    st.title("🔧 Minimal App Test")
    
    # Test authentication
    if not test_authentication():
        return
    
    st.success("✅ Authentication passed!")
    
    # Test database
    if not test_database():
        return
        
    # Test RAG
    if not test_rag():
        return
    
    st.success("🎉 All systems working! Main app should work now.")
    
    # Simple interface
    st.write("Welcome to the Bosch AI Document Assistant!")
    
    if st.button("Test Complete - Logout"):
        st.session_state.authenticated = False
        st.rerun()

if __name__ == "__main__":
    main()
