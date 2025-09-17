import streamlit as st
import os
import sys

# Add config directory to path  
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

# Page config
st.set_page_config(
    page_title="Bosch AI Document Assistant",
    page_icon="🔧",
    layout="wide"
)

def main():
    st.write("Application starting...")
    
    try:
        st.write("Importing auth config...")
        from config.auth_config import VALID_PASSWORDS, HINT_MESSAGE, MAX_LOGIN_ATTEMPTS
        st.write(f"Auth config loaded. Found {len(VALID_PASSWORDS)} valid passwords")
        
        st.write("Setting up session state...")
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
            st.session_state.login_attempts = 0
        
        st.write(f"Current auth status: {st.session_state.authenticated}")
        
        if not st.session_state.authenticated:
            st.title("🔧 Bosch Employee Verification")
            st.write("Please enter a Bosch hashtag to continue")
            
            password = st.text_input("Enter Bosch Hashtag:", type="password")
            if st.button("Login"):
                if password.lower() in [p.lower() for p in VALID_PASSWORDS]:
                    st.session_state.authenticated = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid hashtag")
        else:
            st.success("Authenticated!")
            st.write("Welcome to the application")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
