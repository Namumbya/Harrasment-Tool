import streamlit as st
import bcrypt
from utils.database import execute_query

def login_user(email, password):
    """Authenticate user and return user data"""
    query = "SELECT id, name, email, password_hash FROM users WHERE email = ?"
    user = execute_query(query, (email,), fetchone=True)
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return {
            'id': user[0],
            'name': user[1],
            'email': user[2]
        }
    return None

def register_user(name, email, password):
    """Register a new user"""
    # Checking if email exists
    existing = execute_query("SELECT id FROM users WHERE email = ?", (email,), fetchone=True)
    if existing:
        return None
        
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert user
    query = "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)"
    user_id = execute_query(query, (name, email, password_hash.decode('utf-8')))
    
    return user_id

def show():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_email = None

    st.title("Welcome to HerVoice ")

    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if not all([email, password]):
                    st.error("Please fill in all fields")
                else:
                    user = login_user(email, password)
                    if user:
                        st.session_state.user_id = user['id']
                        st.session_state.user_name = user['name']
                        st.session_state.user_email = user['email']
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Register")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            password_confirm = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if not all([name, email, password, password_confirm]):
                    st.error("Please fill in all fields")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                else:
                    user_id = register_user(name, email, password)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.user_name = name
                        st.session_state.user_email = email
                        st.success("Registration successful!")
                        st.rerun()
                    else:
                        st.error("Email already registered")