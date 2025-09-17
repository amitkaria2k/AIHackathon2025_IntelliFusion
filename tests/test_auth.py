import streamlit as st
import os
import sys

# Add the current directory to Python path
sys.path.append(os.getcwd())

from config.auth_config import VALID_PASSWORDS

def test_auth():
    st.title("Auth Test")
    st.write(f"Valid passwords loaded: {len(VALID_PASSWORDS)}")
    st.write(f"First valid password: {VALID_PASSWORDS[0]}")
    
    # Test basic authentication form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username == "bosch_user" and password in VALID_PASSWORDS:
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

if __name__ == "__main__":
    test_auth()
