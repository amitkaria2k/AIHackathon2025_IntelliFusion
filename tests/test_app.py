import streamlit as st

def main():
    """Test main function"""
    st.title("Test App - Debugging Blank Page")
    st.write("If you see this, the basic app is working!")
    
    # Simple authentication test
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        st.subheader("Login Test")
        role = st.selectbox("Select Role", ["PM", "Project team", "Quality team"])
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if (role == "PM" and password == "pm123") or \
               (role == "Project team" and password == "project") or \
               (role == "Quality team" and password == "quality"):
                st.session_state['authenticated'] = True
                st.session_state['user_role'] = role
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        st.success(f"Logged in as: {st.session_state['user_role']}")
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            del st.session_state['user_role']
            st.rerun()

if __name__ == "__main__":
    main()
