import streamlit as st
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

st.set_page_config(page_title="Debug Test", page_icon="🔧")

st.title("🔧 Debug Test")
st.write("Basic Streamlit working...")

try:
    from config.auth_config import VALID_PASSWORDS, HINT_MESSAGE, MAX_LOGIN_ATTEMPTS
    st.success("✅ Auth config imported successfully")
    st.write(f"Found {len(VALID_PASSWORDS)} valid passwords")
except Exception as e:
    st.error(f"❌ Auth config error: {e}")

try:
    from config.database import DatabaseManager
    st.success("✅ Database manager imported successfully")
    db = DatabaseManager()
    st.write("Database manager initialized")
except Exception as e:
    st.error(f"❌ Database error: {e}")

try:
    from services.rag_service import RAGService
    st.success("✅ RAG service imported successfully")
except Exception as e:
    st.error(f"❌ RAG service error: {e}")

st.write("Debug test completed!")
