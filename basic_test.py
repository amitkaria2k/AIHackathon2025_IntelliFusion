import streamlit as st
import os
import sys

# Add config directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

st.set_page_config(page_title="Test App")

st.title("Basic Test")
st.write("If you can see this, Streamlit is working")

try:
    from config.auth_config import VALID_PASSWORDS
    st.success(f"Config loaded! Found {len(VALID_PASSWORDS)} passwords")
    st.write("First password:", VALID_PASSWORDS[0])
except Exception as e:
    st.error(f"Config error: {e}")

password = st.text_input("Test input")
if password:
    st.write(f"You typed: {password}")

if st.button("Test button"):
    st.balloons()
    st.success("Button works!")
