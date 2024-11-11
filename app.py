import streamlit as st
from streamlit.components.v1 import html
import os
from utils.database import init_db

# Hide default Streamlit pages from sidebar
def hide_pages():
    # CSS to hide the default pages
    st.markdown("""
        <style>
        /* Hide hamburger menu */
        #MainMenu {
            visibility: hidden;
        }
        
        /* Hide default pages in navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Hide Streamlit footer */
        footer {
            visibility: hidden;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding-top: 0;
        }
        </style>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="HerVoice",
    page_icon="🛡️",
    layout="wide"
)

# Hide default pages
hide_pages()

def sidebar():
    with st.sidebar:
        st.title("HerVoice")
        
        # Custom navigation with radio buttons
        selected = st.radio(
            label="Navigation Menu",
            options=[
                "🏠 Home",
                "💬 24/7 Support Chat",
                "📝 Report Incident",
                "🔍 Find Help",
                "📚 Resources",
                "📊 Statistics"
            ],
            label_visibility="collapsed",
            key="nav"
        )
        
        # User info and logout
        if st.session_state.get('user_id'):
            st.divider()
            st.markdown(f"👤 **{st.session_state.get('user_name', 'User')}**")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        
        # Sidebar footer
        st.sidebar.markdown("<br>" * 5, unsafe_allow_html=True)
        st.sidebar.markdown("""
            <div style='position: fixed; bottom: 0; padding: 1rem; font-size: 0.8rem; opacity: 0.7;'>
                © 2024 HerVoice Africa
            </div>
        """, unsafe_allow_html=True)
        
        return selected

def main():
    try:
        # Initialize database
        init_db()
        
        # Show navigation
        page = sidebar()
        
        # Route to appropriate page based on selection
        if page == "🏠 Home":
            from pages import home
            home.show()
        elif page == "💬 24/7 Support Chat":
            from pages import chat_support
            chat_support.show()
        elif page == "📝 Report Incident":
            if not st.session_state.get('user_id'):
                from pages import auth
                auth.show()
            else:
                from pages import report_incident
                report_incident.show()
        elif page == "🔍 Find Help":
            from pages import find_help
            find_help.show()
        elif page == "📚 Resources":
            from pages import resources
            resources.show()
        elif page == "📊 Statistics":
            from pages import statistics
            statistics.show()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please try refreshing the page or contact support if the problem persists.")

if __name__ == "__main__":
    main()
