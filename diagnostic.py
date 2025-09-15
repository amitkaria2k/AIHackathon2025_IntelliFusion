import streamlit as st
import sys
import os
from datetime import datetime

st.set_page_config(page_title="Diagnostic Test")

st.markdown("# 🔧 DIAGNOSTIC TEST")
st.markdown(f"**Time:** {datetime.now()}")
st.markdown(f"**Python Version:** {sys.version}")

st.markdown("## Test 1: Basic Streamlit")
st.success("✅ Streamlit is working!")

st.markdown("## Test 2: User Input")
name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello {name}!")

st.markdown("## Test 3: Button")
if st.button("Click me!"):
    st.balloons()
    st.success("Button works!")

st.markdown("## Test 4: Config Import")
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
    from config.auth_config import VALID_PASSWORDS
    st.success(f"✅ Config loaded! {len(VALID_PASSWORDS)} passwords found")
except Exception as e:
    st.error(f"❌ Config error: {e}")

st.markdown("## Test 5: Session State")
if "test_counter" not in st.session_state:
    st.session_state.test_counter = 0

if st.button("Count +1"):
    st.session_state.test_counter += 1

st.write(f"Counter: {st.session_state.test_counter}")

st.markdown("## Test 6: Styling")
st.markdown("""
<style>
.test-box {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
<div class="test-box">
    <h3>Custom CSS Test</h3>
    <p>If you can see this styled box, CSS is working!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.info("If you can see all tests above, Streamlit is working correctly!")
