"""
Test script to debug the authentication issue
"""
import streamlit as st
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
from config.auth_config import VALID_PASSWORDS, HINT_MESSAGE, MAX_LOGIN_ATTEMPTS

st.set_page_config(
    page_title="Debug Test",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Debug Test")

# Test authentication display
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.login_attempts = 0

if not st.session_state.authenticated:
    st.write("Authentication not active - showing login")
    
    st.markdown("""
    <div style="max-width: 400px; margin: 0 auto; padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="color: #DC2626; text-align: center;">🔧 Bosch Employee Verification</h2>
        <p style="text-align: center; color: #6B7280; margin-bottom: 2rem;">
            Prove that you are a Bosch employee.<br>
            Enter any Bosch Hashtags to login.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("test_login"):
        password = st.text_input("Enter Bosch Hashtag:", type="password", placeholder="#BeLikeBosch")
        login_button = st.form_submit_button("🚀 Login")
        
        if login_button:
            if password.lower() in [p.lower() for p in VALID_PASSWORDS]:
                st.session_state.authenticated = True
                st.session_state.login_attempts = 0
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                st.error(f"❌ Invalid hashtag! Attempts: {st.session_state.login_attempts}")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
        <p><strong>Valid Hashtags Include:</strong></p>
        <p>#BeLikeBosch | #BoschLife | #InventedForLife | #BoschInnovation | #BoschTech</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.success("✅ Successfully authenticated!")
    st.write("Main app content would go here...")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# Debug info
st.sidebar.write("**Debug Info:**")
st.sidebar.write(f"Authenticated: {st.session_state.get('authenticated', False)}")
st.sidebar.write(f"Login attempts: {st.session_state.get('login_attempts', 0)}")
st.sidebar.write(f"Valid passwords loaded: {len(VALID_PASSWORDS)}")
