"""
Authentication Page - Kaspa Analytics Pro
Handles login, registration, user profile, and account management
"""

import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime

# Import utilities
from utils.auth import (
    get_current_user, 
    get_authenticator, 
    is_authenticated,
    add_user,
    logout_user,
    get_user_stats,
    update_user_subscription
)
from utils.ui import (
    render_page_header, 
    render_sidebar_navigation,
    apply_custom_css,
    render_subscription_comparison,
    render_footer
)

# Configure page
st.set_page_config(
    page_title="Authentication - Kaspa Analytics Pro",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Login, register, or manage your Kaspa Analytics Pro account. Access premium features and manage your subscription.">
<meta name="keywords" content="Kaspa Analytics login, register account, user profile, subscription management">
<meta property="og:title" content="Account Management - Kaspa Analytics Pro">
<meta property="og:description" content="Manage your Kaspa Analytics Pro account and subscription">
""", unsafe_allow_html=True)

# Apply styling
apply_custom_css()

def main():
    """Main authentication page"""
    
    # Get current user
    user = get_current_user()
    
    # Render sidebar navigation
    render_sidebar_navigation(user)
    
    # Main content based on authentication status
    if user['username'] == 'public':
        render_public_auth_page()
    else:
        render_user_profile_page(user)
    
    # Footer
    render_footer()

def render_public_auth_page():
    """Authentication page for public users"""
    
    render_page_header(
        "🔐 Account Access",
        "Login to your account or create a new one to unlock premium features"
    )
    
    # Navigation breadcrumb
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Dashboard", key="auth_back_to_home"):
            st.switch_page("streamlit_app.py")
    
    # Authentication tabs
    auth_tabs = sac.tabs([
        sac.TabsItem(label='Login', icon='box-arrow-in-right'),
        sac.TabsItem(label='Register', icon='person-plus'),
        sac.TabsItem(label='Pricing', icon='currency-dollar'),
        sac.TabsItem(label='Features', icon='star'),
    ], key='main_auth_tabs')
    
    if auth_tabs == 'Login':
        render_login_tab()
    elif auth_tabs == 'Register':
        render_registration_tab()
    elif auth_tabs == 'Pricing':
        render_pricing_tab()
    else:
        render_features_tab()

def render_login_tab():
    """Login interface"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 🔑 Login to Your Account")
        
        # Get authenticator and handle login
        authenticator = get_authenticator()
        
        try:
            authenticator.login()
            
            # Check authentication status
            name = st.session_state.get('name')
            authentication_status = st.session_state.get('authentication_status')
            username = st.session_state.get('username')
            
            if authentication_status == False:
                st.error("❌
