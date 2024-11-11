import streamlit as st
from utils.database import execute_query

def show():
    # Custom CSS with updated colors
    st.markdown("""
        <style>
        :root {
            --primary-color: #7B2CBF;      /* Royal Purple - represents dignity */
            --secondary-color: #9D4EDD;    /* Lighter Purple - approachability */
            --accent-color: #FF6B6B;       /* Soft Red - urgency/importance */
            --safe-color: #4CAF50;         /* Green - safety/success */
            --text-dark: #2C3E50;          /* Dark Blue-Gray - trust */
            --text-light: #FFFFFF;         /* White - clarity */
            --bg-light: #F8F9FA;           /* Light Gray - neutrality */
            --bg-warm: #FFF5F5;            /* Warm White - comfort */
        }
        
        .main-header {
            text-align: center;
            padding: 2.5rem 0;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: var(--text-light);
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(123, 44, 191, 0.2);
        }
        .sub-header {
            font-size: 1.2rem;
            opacity: 0.95;
            color: var(--text-light);
            margin-top: 0.5rem;
        }
        .feature-card {
            padding: 1.8rem;
            background: var(--bg-light);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            transition: all 0.3s ease;
            border-left: 4px solid var(--primary-color);
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(123, 44, 191, 0.15);
        }
        .feature-card h3 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        .feature-card p {
            color: var(--text-dark);
            line-height: 1.6;
        }
        .stat-card {
            text-align: center;
            padding: 1.5rem;
            background: var(--text-light);
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin: 0.5rem;
            border-top: 4px solid var(--secondary-color);
        }
        .stat-card h3 {
            color: var(--primary-color);
            font-size: 2rem;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        .stat-card p {
            color: var(--text-dark);
            font-size: 1rem;
        }
        .welcome-message {
            background-color: var(--safe-color);
            color: var(--text-light);
            padding: 1.2rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
        }
        .emergency-resources {
            background-color: var(--bg-warm);
            padding: 2rem;
            border-radius: 12px;
            margin: 2rem 0;
            border-left: 4px solid var(--accent-color);
        }
        .emergency-resources h3 {
            color: var(--accent-color);
            margin-bottom: 1.5rem;
        }
        .emergency-resources p {
            color: var(--text-dark);
            margin-bottom: 0.8rem;
        }
        .footer {
            background-color: var(--bg-light);
            padding: 1.5rem;
            border-radius: 8px;
            color: var(--text-dark);
            margin-top: 3rem;
            border-top: 2px solid rgba(123, 44, 191, 0.1);
        }
        .footer a {
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .footer a:hover {
            color: var(--secondary-color);
        }
        .stButton>button {
            background-color: var(--primary-color) !important;
            color: var(--text-light) !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            background-color: var(--secondary-color) !important;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

    # Main Header Section
    st.markdown("""
        <div class="main-header">
            <h1>🛡️ HerVoice</h1>
            <p class="sub-header">Empowering Voices, Ensuring Safety</p>
        </div>
    """, unsafe_allow_html=True)

    # Quick Actions for logged-in users
    if st.session_state.get('user_id'):
        st.success(f"Welcome back, {st.session_state.get('user_name', 'User')}!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Submit Report", use_container_width=True, type="primary"):
                st.switch_page("pages/report_incident.py")
        with col2:
            if st.button("💬 24/7 Support Chat", use_container_width=True):
                st.switch_page("pages/chat_support.py")
        with col3:
            if st.button("🔍 Find Help", use_container_width=True):
                st.switch_page("pages/find_help.py")

        # Statistics Section
        st.divider()
        st.subheader("Platform Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="stat-card">
                    <h3>1,234</h3>
                    <p>Reports Filed</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="stat-card">
                    <h3>98%</h3>
                    <p>Response Rate</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="stat-card">
                    <h3>50+</h3>
                    <p>Support Teams</p>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
                <div class="stat-card">
                    <h3>24/7</h3>
                    <p>Support Available</p>
                </div>
            """, unsafe_allow_html=True)

    # Features Section
    st.divider()
    st.header("Why Choose Our Platform?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>🔒 Secure & Private</h3>
                <p>End-to-end encryption and anonymous reporting options to protect your identity.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>⚡ Quick Response</h3>
                <p>24/7 monitoring and rapid response system for urgent cases.</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3>📊 Detailed Analytics</h3>
                <p>Comprehensive reporting and tracking of your case progress.</p>
            </div>
        """, unsafe_allow_html=True)

    # Emergency Resources
    with st.expander("🆘 Emergency Resources"):
        st.markdown("""
        ### Immediate Help
        - **Emergency Services**: 112 (Police)
        - **Women's Helpline**: 0800-428-428
        - **Support Chat**: *120*7867#
        
        ### Legal Resources
        - Free Legal Consultation
        - Document Templates
        - Victim Support Services
        """)

    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("© 2024 HerVoice Africa")
    with col2:
        st.markdown("[Privacy Policy](/) • [Terms of Service](/) • [Contact Us](/)")
    with col3:
        st.markdown("Version 1.0.0")
