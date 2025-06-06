"""
Kaspa Analytics Pro - Main Homepage
Updated with sac.menu navigation integration
"""

# Add this at the very top of streamlit_app.py, right after the imports
import streamlit as st

# Clear any cached page information to prevent old file references
if 'pages_cleared' not in st.session_state:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.pages_cleared = True
    
import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime
import pandas as pd
import numpy as np

# Try to import Plotly, fallback gracefully
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Import utilities
from utils.auth import get_current_user, is_authenticated
from utils.data import fetch_kaspa_price_data, get_market_stats
from utils.ui import (
    render_page_header, 
    render_sidebar_navigation,  # This now uses sac.menu
    show_login_prompt,
    apply_custom_css,
    render_footer,
    set_current_page  # New function for page tracking
)
from utils.config import get_app_config

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro - Professional Blockchain Analysis",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://kaspa-analytics.com/help',
        'Report a bug': 'https://kaspa-analytics.com/bug-report',
        'About': "# Kaspa Analytics Pro\nProfessional blockchain analysis platform"
    }
)

# Set current page for menu highlighting
set_current_page('dashboard')

# Apply custom CSS
apply_custom_css()

def main():
    """Main homepage function with sac.menu integration"""
    
    # Get current user and app config
    user = get_current_user()
    config = get_app_config()
    is_auth = is_authenticated()
    
    # Render sidebar navigation with sac.menu
    render_sidebar_navigation(user)
    
    # Main content
    if is_auth:
        render_authenticated_homepage(user)
    else:
        render_public_homepage()
    
    # Footer
    render_footer()

def render_public_homepage():
    """Public homepage with call-to-action for sac.menu navigation"""
    
    # Hero section
    render_page_header(
        "💎 Kaspa Analytics Pro",
        "Professional blockchain analysis platform for Kaspa (KAS)",
        show_auth_buttons=True
    )
    
    # Feature highlight with navigation preview
    st.subheader("🗺️ Platform Navigation")
    st.info("👈 Check out our new navigation menu in the sidebar! Create an account to unlock all features.")
    
    # Quick overview of navigation structure
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Analytics Section")
        st.markdown("- **Price Charts**: Advanced technical analysis")
        st.markdown("- **Power Law**: Mathematical price models")
        st.markdown("- *Login required for full access*")
        
        st.markdown("#### 💾 Data Section")
        st.markdown("- **Network Metrics**: Blockchain statistics")
        st.markdown("- **Data Export**: Download & API access") 
        st.markdown("- *Premium subscription required*")
    
    with col2:
        st.markdown("#### 👤 Account Section")
        st.markdown("- **Authentication**: Login & registration")
        st.markdown("- **Profile Management**: Settings & billing")
        st.markdown("- **Subscription Plans**: Free, Premium, Pro")
        
        st.markdown("#### 🔗 Quick Links")
        st.markdown("- **Kaspa.org**: Official website")
        st.markdown("- **GitHub**: Source code & development")
        st.markdown("- **Discord**: Community support")
    
    # Live Market Data (same as before)
    render_market_overview()
    
    # Navigation demo
    st.markdown("---")
    st.subheader("🎯 Try the Navigation")
    
    demo_cols = st.columns(3)
    
    with demo_cols[0]:
        if st.button("📈 View Price Charts", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📈_Price_Charts.py")
    
    with demo_cols[1]:
        if st.button("🔑 Create Account", use_container_width=True):
            st.switch_page("pages/5_⚙️_Authentication.py")
    
    with demo_cols[2]:
        if st.button("📊 Power Law Demo", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")
    
    # Feature showcase (same as before but with navigation context)
    render_feature_showcase_with_navigation()

def render_authenticated_homepage(user):
    """Authenticated dashboard with navigation integration"""
    
    subscription = user['subscription']
    
    # Welcome header
    render_page_header(
        f"👋 Welcome back, {user['name']}!",
        f"Your {subscription.title()} Dashboard - Use the sidebar menu to navigate",
        show_auth_buttons=False
    )
    
    # Navigation guide for new users
    if st.session_state.get('show_navigation_guide', True):
        with st.expander("🗺️ Navigation Guide", expanded=False):
            st.markdown("""
            **New sidebar navigation features:**
            - 📊 **Analytics**: Access all your analysis tools
            - 💾 **Data**: Network metrics and export features
            - 👤 **Account**: Manage your profile and subscription
            - 🔗 **Quick Links**: External Kaspa resources
            
            Your current plan unlocks specific features - look for the tags next to menu items!
            """)
            
            if st.button("Got it! Hide this guide", key="hide_nav_guide"):
                st.session_state.show_navigation_guide = False
                st.rerun()
    
    # Quick stats dashboard
    render_dashboard_stats(user)
    
    # Quick actions with navigation context
    st.subheader("⚡ Quick Actions")
    st.markdown("*Use the sidebar menu for full navigation, or try these shortcuts:*")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("📈 Price Charts", key="dash_charts", use_container_width=True):
            st.switch_page("pages/1_📈_Price_Charts.py")
    
    with action_cols[1]:
        if st.button("📊 Power Law", key="dash_powerlaw", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")
    
    with action_cols[2]:
        if subscription in ['premium', 'pro']:
            if st.button("🌐 Network Metrics", key="dash_network", use_container_width=True):
                st.switch_page("pages/3_🌐_Network_Metrics.py")
        else:
            st.button("🔒 Network Metrics", disabled=True, use_container_width=True, help="Premium+ required")
    
    with action_cols[3]:
        if subscription in ['premium', 'pro']:
            if st.button("📋 Data Export", key="dash_export", use_container_width=True):
                st.switch_page("pages/4_📋_Data_Export.py")
        else:
            st.button("🔒 Data Export", disabled=True, use_container_width=True, help="Premium+ required")
    
    # Recent activity and chart preview (same as before)
    render_user_dashboard_content(user)

def render_market_overview():
    """Market overview section"""
    st.subheader("📊 Live Market Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get market data
    df = fetch_kaspa_price_data()
    stats = get_market_stats(df) if not df.empty else {}
    
    with col1:
        st.metric(
            "KAS Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_7d', 0):+.2f}%"
        )
    
    with col2:
        st.metric(
            "24h Volume", 
            f"${stats.get('volume_24h', 0):,.0f}"
        )
    
    with col3:
        st.metric(
            "Market Cap", 
            f"${stats.get('market_cap', 0):.1f}B"
        )
    
    with col4:
        st.metric(
            "Network Hash Rate", 
            f"{stats.get('hash_rate', 0):.2f} EH/s"
        )

def render_feature_showcase_with_navigation():
    """Feature showcase highlighting navigation"""
    st.subheader("🚀 Platform Features")
    
    # Use sac.tabs for consistency with the menu component
    feature_tabs = sac.tabs([
        sac.TabsItem(label='Navigation', icon='map'),
        sac.TabsItem(label='Analytics', icon='graph-up'),
        sac.TabsItem(label='Data Access', icon='database'),
        sac.TabsItem(label='Tools', icon='tools'),
    ], key='feature_showcase')
    
    if feature_tabs == 'Navigation':
        render_navigation_showcase()
    elif feature_tabs == 'Analytics':
        render_analytics_showcase()
    elif feature_tabs == 'Data Access':
        render_data_showcase()
    else:
        render_tools_showcase()

def render_navigation_showcase():
    """Showcase the new navigation system"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗺️ Smart Navigation")
        st.write("• **Organized Structure**: Analytics, Data, Account sections")
        st.write("• **Access Control**: Features unlock based on your plan")
        st.write("• **Visual Indicators**: Tags show required subscription levels")
        st.write("• **External Links**: Quick access to Kaspa resources")
        
        st.markdown("#### 🎯 Subscription Gating")
        st.write("• **Public**: Basic preview access")
        st.write("• **Free**: Full navigation, basic features")
        st.write("• **Premium+**: All features unlocked")
    
    with col2:
        st.markdown("#### 🚀 Navigation Benefits")
        st.write("• **Faster Access**: Find features quickly")
        st.write("• **Clear Hierarchy**: Logical organization")
        st.write("• **Status Awareness**: Know what you can access")
        st.write("• **Seamless Upgrades**: Easy subscription management")
        
        if st.button("🎯 Try Navigation Now", key="try_navigation", use_container_width=True, type="primary"):
            st.info("👈 Check out the new sidebar menu!")

def render_dashboard_stats(user):
    """Dashboard statistics for authenticated users"""
    col1, col2, col3, col4 = st.columns(4)
    
    df = fetch_kaspa_price_data()
    stats = get_market_stats(df) if not df.empty else {}
    
    with col1:
        st.metric(
            "KAS Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_24h', 0):+.2f}%"
        )
    
    with col2:
        st.metric("Your Plan", user['subscription'].title())
    
    with col3:
        if user['subscription'] in ['premium', 'pro']:
            st.metric("Features Unlocked", "All", "100%")
        elif user['subscription'] == 'free':
            st.metric("Features Unlocked", "Basic", "60%")
        else:
            st.metric("Features Available", "Preview", "20%")
    
    with col4:
        st.metric("Navigation Items", "8+", "New!")

def render_user_dashboard_content(user):
    """User-specific dashboard content"""
    # Enhanced chart for authenticated users
    df = fetch_kaspa_price_data()
    if not df.empty:
        st.subheader("📈 Price Analysis Dashboard")
        
        subscription = user['subscription']
        
        if subscription == 'free':
            chart_data = df.tail(30)
            st.info("📊 Free account: 30-day data. Use sidebar navigation to explore features!")
        else:
            chart_data = df.tail(365)
            st.success(f"📊 {subscription.title()} account: Full access via sidebar navigation")
        
        # Simple chart for dashboard
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=chart_data['timestamp'], 
                y=chart_data['price'],
                mode='lines',
                name='KAS Price',
                line=dict(color='#70C7BA', width=2)
            ))
            
            fig.update_layout(
                title="Recent Price Movement",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart(chart_data.set_index('timestamp')['price'])
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    activity_data = [
        {"time": "2 hours ago", "action": "Used new sidebar navigation", "status": "✅"},
        {"time": "1 day ago", "action": "Viewed price charts", "status": "✅"},
        {"time": "3 days ago", "action": "Updated profile settings", "status": "✅"},
    ]
    
    for activity in activity_data:
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 1])
            with col1:
                st.write(activity["time"])
            with col2:
                st.write(activity["action"])
            with col3:
                st.write(activity["status"])

def render_analytics_showcase():
    """Analytics features showcase"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Advanced Analytics")
        st.write("• **Power Law Models**: Mathematical price predictions")
        st.write("• **Technical Indicators**: RSI, MACD, Moving averages")
        st.write("• **Trend Analysis**: Support/resistance levels")
        st.write("• **Volatility Metrics**: Price volatility tracking")
        
        if st.button("🔍 Explore Analytics", key="explore_analytics", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")
    
    with col2:
        st.markdown("#### 🌐 Network Insights")
        st.write("• **Hash Rate Tracking**: Network security metrics")
        st.write("• **Address Analysis**: Active wallet tracking")
        st.write("• **Transaction Metrics**: Network usage stats")
        st.write("• **Mining Analytics**: Difficulty and rewards")
        
        if st.button("📊 View Network Data", key="explore_network", use_container_width=True):
            st.switch_page("pages/3_🌐_Network_Metrics.py")

def render_data_showcase():
    """Data access showcase"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Real-time Data")
        st.write("• **Live Price Feeds**: Real-time KAS pricing")
        st.write("• **Historical Data**: Complete price history")
        st.write("• **High Frequency**: Minute-by-minute updates")
        st.write("• **Multiple Exchanges**: Aggregated pricing data")
    
    with col2:
        st.markdown("#### 📋 Export Options")
        st.write("• **CSV/JSON Export**: Download your data")
        st.write("• **API Access**: Programmatic data access")
        st.write("• **Custom Reports**: Automated reporting")
        st.write("• **Webhooks**: Real-time notifications")
        
        if st.button("📥 Export Data", key="explore_export", use_container_width=True):
            st.switch_page("pages/4_📋_Data_Export.py")

def render_tools_showcase():
    """Tools showcase"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛠️ Analysis Tools")
        st.write("• **Custom Dashboards**: Personalized views")
        st.write("• **Alert System**: Price and volume alerts")
        st.write("• **Portfolio Tracking**: Track your holdings")
        st.write("• **Comparison Tools**: Compare with other assets")
    
    with col2:
        st.markdown("#### ⚙️ Advanced Features")
        st.write("• **API Integration**: Connect your tools")
        st.write("• **White-label Reports**: Branded analysis")
        st.write("• **Team Collaboration**: Share insights")
        st.write("• **Mobile Access**: Use anywhere")

if __name__ == "__main__":
    main()
