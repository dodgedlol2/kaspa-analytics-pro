"""
Kaspa Analytics Pro - Simplified Main Homepage
Minimal version to eliminate performance issues
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple auth check
def get_current_user():
    """Get current user information"""
    if st.session_state.get('authentication_status') is True:
        username = st.session_state.get('username', 'unknown')
        name = st.session_state.get('name', 'User')
        
        # Simple subscription mapping
        subscription_map = {
            'admin': 'pro',
            'premium_user': 'premium',
            'free_user': 'free'
        }
        
        subscription = subscription_map.get(username, 'free')
        
        return {
            'name': name,
            'username': username,
            'subscription': subscription
        }
    else:
        return {
            'name': 'Public User',
            'username': 'public',
            'subscription': 'public'
        }

# Simple navigation
def render_simple_sidebar(user):
    """Simple sidebar without complex components"""
    with st.sidebar:
        st.markdown("# 💎 Kaspa Analytics")
        st.markdown("*Professional Analysis Platform*")
        
        if user['username'] != 'public':
            st.markdown(f"**👤 {user['name']}** ({user['subscription']})")
        else:
            st.markdown("**👤 Public Access**")
        
        st.markdown("---")
        
        # Simple navigation buttons
        if st.button("🏠 Dashboard"):
            st.switch_page("streamlit_app.py")
        
        if st.button("📈 Price Charts"):
            st.switch_page("pages/1_📈_Price_Charts.py")
        
        if user['username'] != 'public':
            if st.button("📊 Power Law"):
                st.switch_page("pages/2_📊_Power_Law.py")
        else:
            st.button("🔒 Power Law (Login Required)", disabled=True)
        
        if user['subscription'] in ['premium', 'pro']:
            if st.button("🌐 Network Metrics"):
                st.switch_page("pages/3_🌐_Network_Metrics.py")
        else:
            st.button("🔒 Network Metrics (Premium+)", disabled=True)
        
        if user['subscription'] in ['premium', 'pro']:
            if st.button("📋 Data Export"):
                st.switch_page("pages/4_📋_Data_Export.py")
        else:
            st.button("🔒 Data Export (Premium+)", disabled=True)
        
        st.markdown("---")
        
        if user['username'] == 'public':
            if st.button("🔑 Login"):
                st.switch_page("pages/5_⚙️_Authentication.py")
            if st.button("🚀 Sign Up", type="primary"):
                st.switch_page("pages/5_⚙️_Authentication.py")
        else:
            if st.button("⚙️ Profile"):
                st.switch_page("pages/5_⚙️_Authentication.py")
            if st.button("🚪 Logout"):
                # Simple logout
                for key in ['authentication_status', 'name', 'username']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        if user['username'] == 'admin':
            st.markdown("---")
            if st.button("👑 Admin Panel"):
                st.switch_page("pages/6_👑_Admin_Panel.py")

# Simple data generation
@st.cache_data
def get_simple_data():
    """Generate simple demo data"""
    dates = pd.date_range(start='2024-12-01', end=datetime.now(), freq='D')
    np.random.seed(42)
    
    base_price = 0.025
    prices = []
    current_price = base_price
    
    for i in range(len(dates)):
        change = np.random.normal(0, 0.02)
        current_price *= (1 + change)
        current_price = max(current_price, 0.001)
        prices.append(current_price)
    
    return pd.DataFrame({
        'date': dates,
        'price': prices
    })

def main():
    """Main application"""
    user = get_current_user()
    render_simple_sidebar(user)
    
    # Main content
    if user['username'] == 'public':
        render_public_page()
    else:
        render_dashboard(user)

def render_public_page():
    """Simple public homepage"""
    st.title("💎 Welcome to Kaspa Analytics Pro")
    st.markdown("*Professional Kaspa blockchain analysis platform*")
    
    # Simple metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("KAS Price", "$0.0250", "+2.1%")
    with col2:
        st.metric("24h Volume", "$1.2M")
    with col3:
        st.metric("Market Cap", "$2.1B")
    
    # Simple chart
    st.subheader("📈 7-Day Price Preview")
    data = get_simple_data().tail(7)
    st.line_chart(data.set_index('date')['price'])
    
    st.info("📊 Public users see 7-day preview. Create a free account for more data!")
    
    # Call to action
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started Free", type="primary", use_container_width=True):
            st.switch_page("pages/5_⚙️_Authentication.py")

def render_dashboard(user):
    """Simple authenticated dashboard"""
    st.title(f"👋 Welcome back, {user['name']}!")
    st.markdown(f"*Your {user['subscription'].title()} Dashboard*")
    
    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("KAS Price", "$0.0250", "+2.1%")
    with col2:
        st.metric("Your Plan", user['subscription'].title())
    with col3:
        if user['subscription'] in ['premium', 'pro']:
            st.metric("Power Law", "Above Trend", "+15%")
        else:
            st.metric("Power Law", "🔒 Premium")
    with col4:
        st.metric("Active Alerts", "3")
    
    # Simple chart based on subscription
    st.subheader("📈 Price Analysis")
    
    data = get_simple_data()
    if user['subscription'] == 'free':
        chart_data = data.tail(30)
        st.info("📊 Free account: 30-day data. Upgrade for full history!")
    else:
        chart_data = data
        st.success(f"📊 {user['subscription'].title()} account: Full data access")
    
    st.line_chart(chart_data.set_index('date')['price'])
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📈 View Charts", use_container_width=True):
            st.switch_page("pages/1_📈_Price_Charts.py")
    
    with col2:
        if st.button("📊 Power Law", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")
    
    with col3:
        if user['subscription'] in ['premium', 'pro']:
            if st.button("🌐 Network Data", use_container_width=True):
                st.switch_page("pages/3_🌐_Network_Metrics.py")
        else:
            st.button("🔒 Network Data", disabled=True, use_container_width=True)
    
    with col4:
        if user['subscription'] in ['premium', 'pro']:
            if st.button("📋 Export", use_container_width=True):
                st.switch_page("pages/4_📋_Data_Export.py")
        else:
            st.button("🔒 Export", disabled=True, use_container_width=True)

if __name__ == "__main__":
    main()
