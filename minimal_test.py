import streamlit as st

st.title("Minimal Test")
st.write("This is a minimal Streamlit app to test basic functionality")

# Test session state
if "test_var" not in st.session_state:
    st.session_state.test_var = "Session state working"

st.write(f"Session state: {st.session_state.test_var}")

# Test authentication simulation
username = st.text_input("Username")
if username:
    st.write(f"Hello {username}!")

# Test button
if st.button("Test Button"):
    st.success("Button clicked successfully!")
