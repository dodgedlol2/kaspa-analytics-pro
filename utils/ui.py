"""
UI utilities and components for Kaspa Analytics Pro
Handles styling, common components, and layout utilities
"""

import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime
from utils.auth import get_current_user, logout_user, check_feature_access

def apply_custom_css():
    """Apply custom CSS styling for the entire application"""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --kaspa-primary: #70C7BA;
        --kaspa-secondary: #49A097;
        --kaspa-accent: #667eea;
        --kaspa-gradient: linear-gradient(135deg, #70C7BA 0%, #49A097 100%);
        --kaspa-accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Page header styling */
    .page-header {
        background: var(--kaspa-gradient);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .page-header h1 {
        margin: 0 0 0.5rem 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .page-header p {
        margin: 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Authentication container */
    .auth-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    /* Subscription badges */
    .subscription-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.25rem 0;
    }
    
    .badge-public {
        background: #28a745;
        color: white;
    }
    
    .badge-free {
        background: #6c757d;
        color: white;
    }
    
    .badge-premium {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
    }
    
    .badge-pro {
        background: linear-gradient(45deg, #8A2BE2, #4B0082);
        color: white;
    }
    
    /* Login prompt styling */
    .login-prompt {
        background: var(--kaspa-accent-gradient);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .login-prompt h3 {
        margin: 0 0 1rem 0;
    }
    
    /* Feature highlight boxes */
    .feature-highlight {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid var(--kaspa-primary);
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Upgrade prompt */
    .upgrade-prompt {
        background: var(--kaspa-accent-gradient);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Stats cards */
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        text-align: center;
    }
    
    /* Navigation styling */
    .nav-section {
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Footer styling */
    .footer {
        background: #f8f9fa;
        padding: 2rem;
        margin-top: 3rem;
        border-radius: 8px;
        text-align: center;
        color: #6c757d;
    }
    
    .footer a {
        color: var(--kaspa-primary);
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Error and warning styling */
    .stAlert > div {
        border-radius: 8px;
    }
    
    /* Custom metric styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Sidebar styling */
    .sidebar .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .page-header h1 {
            font-size: 2rem;
        }
        
        .page-header {
            padding: 1.5rem;
        }
        
        .auth-container {
            padding: 1rem;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--kaspa-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--kaspa-secondary);
    }
    </style>
    """, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str = "", show_auth_buttons: bool = False):
    """Render a consistent page header"""
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
    
    if show_auth_buttons:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            auth_cols = st.columns(2)
            
            with auth_cols[0]:
                if st.button("🔑 Login", key="header_login_btn", use_container_width=True):
                    st.switch_page("pages/5_⚙️_Authentication.py")
            
            with auth_cols[1]:
                if st.button("🚀 Sign Up", key="header_signup_btn", use_container_width=True, type="primary"):
                    st.switch_page("pages/5_⚙️_Authentication.py")

def render_sidebar_navigation(user):
    """Render sidebar navigation for all pages"""
    with st.sidebar:
        # Logo and title
        st.markdown("# 💎 Kaspa Analytics")
        st.markdown(f"*Professional Analysis Platform*")
        
        # User info
        if user['username'] != 'public':
            st.markdown(f"**👤 {user['name']}**")
            st.markdown(f'<span class="subscription-badge badge-{user["subscription"]}">{user["subscription"].upper()}</span>', unsafe_allow_html=True)
        else:
            st.markdown("**👤 Public Access**")
            st.markdown('<span class="subscription-badge badge-public">PUBLIC</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### 📊 Navigation")
        
        # Home
        if st.button("🏠 Dashboard", use_container_width=True, key="nav_home"):
            st.switch_page("streamlit_app.py")
        
        # Price Charts
        if st.button("📈 Price Charts", use_container_width=True, key="nav_charts"):
            st.switch_page("pages/1_📈_Price_Charts.py")
        
        # Power Law
        if user['subscription'] == 'public':
            st.button("🔒 Power Law", disabled=True, use_container_width=True, help="Requires account")
        else:
            if st.button("📊 Power Law", use_container_width=True, key="nav_powerlaw"):
                st.switch_page("pages/2_📊_Power_Law.py")
        
        # Network Metrics (Premium+)
        if check_feature_access('network_metrics', user['subscription']):
            if st.button("🌐 Network Metrics", use_container_width=True, key="nav_network"):
                st.switch_page("pages/3_🌐_Network_Metrics.py")
        else:
            st.button("🔒 Network Metrics", disabled=True, use_container_width=True, help="Requires Premium+")
        
        # Data Export (Premium+)
        if check_feature_access('data_export', user['subscription']):
            if st.button("📋 Data Export", use_container_width=True, key="nav_export"):
                st.switch_page("pages/4_📋_Data_Export.py")
        else:
            st.button("🔒 Data Export", disabled=True, use_container_width=True, help="Requires Premium+")
        
        # Admin Panel (Admin only)
        if user['username'] == 'admin':
            if st.button("👑 Admin Panel", use_container_width=True, key="nav_admin"):
                st.switch_page("pages/6_👑_Admin_Panel.py")
        
        st.markdown("---")
        
        # Authentication section
        if user['username'] == 'public':
            st.markdown("### 🔐 Account")
            
            if st.button("🔑 Login", use_container_width=True, key="sidebar_login"):
                st.switch_page("pages/
