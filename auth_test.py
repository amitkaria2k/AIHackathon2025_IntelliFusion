import streamlit as st
import os
import sys

# Add config directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

# Configure page
st.set_page_config(
    page_title="Bosch AI Document Assistant",
    page_icon="🔧",
    layout="wide"
)

def main():
    try:
        # Import auth config
        from config.auth_config import VALID_PASSWORDS, HINT_MESSAGE, MAX_LOGIN_ATTEMPTS
        
        st.title("🔧 Bosch AI Document Assistant")
        st.write("Auth Test Version")
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
            st.session_state.login_attempts = 0
        
        if not st.session_state.authenticated:
            st.markdown("### Authentication Required")
            
            with st.form("login_form"):
                password = st.text_input("Enter Bosch Hashtag:", type="password", placeholder="#BeLikeBosch")
                login_button = st.form_submit_button("🚀 Login")
                
                if login_button:
                    if password.lower() in [p.lower() for p in VALID_PASSWORDS]:
                        st.session_state.authenticated = True
                        st.session_state.login_attempts = 0
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.session_state.login_attempts += 1
                        if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
                            st.error(f"❌ Invalid hashtag! {HINT_MESSAGE}")
                        else:
                            remaining = MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts
                            st.error(f"❌ Invalid hashtag! {remaining} attempts remaining.")
            
            st.info("Valid hashtags include: #BeLikeBosch, #BoschLife, #InventedForLife")
        else:
            st.success("✅ Authenticated successfully!")
            st.write("Welcome to the Bosch AI Document Assistant!")
            
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()
                
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
