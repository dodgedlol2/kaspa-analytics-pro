"""
Enhanced UI utilities with sac.menu navigation for Kaspa Analytics Pro
"""

import streamlit as st
import streamlit_antd_components as sac
from utils.auth import get_current_user, logout_user, check_feature_access

def render_sidebar_navigation(user):
    """Render enhanced sidebar navigation with sac.menu"""
    with st.sidebar:
        # Logo and title
        st.markdown("# 💎 Kaspa Analytics")
        st.markdown("*Professional Analysis Platform*")
        
        # User info
        if user['username'] != 'public':
            st.markdown(f"**👤 {user['name']}**")
            st.markdown(f'<span class="subscription-badge badge-{user["subscription"]}">{user["subscription"].upper()}</span>', unsafe_allow_html=True)
        else:
            st.markdown("**👤 Public Access**")
            st.markdown('<span class="subscription-badge badge-public">PUBLIC</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Build menu items based on user subscription
        menu_items = build_menu_items(user)
        
        # Render the menu
        selected_page = sac.menu(
            items=menu_items,
            open_all=False,
            format_func='title',
            key='sidebar_menu'
        )
        
        # Handle menu selection
        handle_menu_selection(selected_page, user)
        
        # Authentication section
        render_auth_section(user)
        
        # Quick stats
        render_sidebar_stats()

def build_menu_items(user):
    """Build menu items based on user subscription level"""
    subscription = user['subscription']
    
    menu_items = [
        # Dashboard
        sac.MenuItem(
            'dashboard', 
            icon='house-fill',
            description='Main dashboard and overview'
        ),
        
        # Analytics section
        sac.MenuItem(
            'analytics', 
            icon='graph-up', 
            description='Price analysis and charts',
            children=[
                sac.MenuItem(
                    'price_charts', 
                    icon='bar-chart-line-fill',
                    description='Advanced price charts'
                ),
                # Power Law - subscription gated
                sac.MenuItem(
                    'power_law', 
                    icon='bezier2',
                    description='Power law analysis',
                    disabled=(subscription == 'public'),
                    tag=[] if subscription != 'public' else [sac.Tag('Login Required', color='orange')]
                ),
            ]
        ),
        
        # Data section - Premium+ features
        sac.MenuItem(
            'data', 
            icon='database-fill',
            description='Data access and export',
            children=[
                sac.MenuItem(
                    'network_metrics', 
                    icon='globe',
                    description='Network and blockchain metrics',
                    disabled=not check_feature_access('network_metrics', subscription),
                    tag=[] if check_feature_access('network_metrics', subscription) else [sac.Tag('Premium+', color='gold')]
                ),
                sac.MenuItem(
                    'data_export', 
                    icon='download',
                    description='Export data and reports',
                    disabled=not check_feature_access('data_export', subscription),
                    tag=[] if check_feature_access('data_export', subscription) else [sac.Tag('Premium+', color='gold')]
                ),
            ]
        ),
        
        # Divider
        sac.MenuItem(type='divider'),
        
        # Account section
        sac.MenuItem(
            'account', 
            icon='person-circle', 
            description='Account management',
            children=[
                sac.MenuItem(
                    'authentication', 
                    icon='key-fill',
                    description='Login, profile & settings'
                ),
            ]
        ),
    ]
    
    # Add admin panel for admin users
    if user['username'] == 'admin':
        menu_items.append(
            sac.MenuItem(
                'admin_panel', 
                icon='shield-fill-check',
                description='Administrator panel',
                tag=[sac.Tag('Admin', color='red')]
            )
        )
    
    # Add external links section
    menu_items.extend([
        sac.MenuItem(type='divider'),
        sac.MenuItem(
            'external', 
            type='group',
            children=[
                sac.MenuItem(
                    'kaspa_org', 
                    icon='globe',
                    href='https://kaspa.org',
                    description='Official Kaspa website'
                ),
                sac.MenuItem(
                    'github', 
                    icon='github',
                    href='https://github.com/kaspanet',
                    description='Kaspa on GitHub'
                ),
                sac.MenuItem(
                    'discord', 
                    icon='discord',
                    href='https://discord.gg/kaspa',
                    description='Join Kaspa Discord'
                ),
            ]
        ),
    ])
    
    return menu_items

def handle_menu_selection(selected_page, user):
    """Handle menu item selection and navigation"""
    if not selected_page:
        return
    
    # Navigation mapping
    page_mapping = {
        'dashboard': 'streamlit_app.py',
        'price_charts': 'pages/1_📈_Price_Charts.py',
        'power_law': 'pages/2_📊_Power_Law.py',
        'network_metrics': 'pages/3_🌐_Network_Metrics.py',
        'data_export': 'pages/4_📋_Data_Export.py',
        'authentication': 'pages/5_⚙️_Authentication.py',
        'admin_panel': 'pages/6_👑_Admin_Panel.py'
    }
    
    # Check if the selected page exists in mapping
    if selected_page in page_mapping:
        target_page = page_mapping[selected_page]
        
        # Check access permissions
        if selected_page in ['power_law'] and user['subscription'] == 'public':
            st.error("🔐 Please log in to access this feature")
            st.info("Redirecting to authentication...")
            st.switch_page('pages/5_⚙️_Authentication.py')
            return
        
        if selected_page in ['network_metrics', 'data_export']:
            if not check_feature_access('network_metrics' if selected_page == 'network_metrics' else 'data_export', user['subscription']):
                st.error("🔒 This feature requires Premium+ subscription")
                st.info("Redirecting to upgrade page...")
                st.switch_page('pages/5_⚙️_Authentication.py')
                return
        
        if selected_page == 'admin_panel' and user['username'] != 'admin':
            st.error("🚫 Admin access required")
            return
        
        # Navigate to the selected page
        st.switch_page(target_page)

def render_auth_section(user):
    """Render authentication section with improved styling"""
    st.markdown("---")
    
    if user['username'] == 'public':
        st.markdown("### 🔐 Get Started")
        
        # Login button
        if st.button("🔑 Login", use_container_width=True, key="sidebar_login", type="primary"):
            st.switch_page("pages/5_⚙️_Authentication.py")
        
        # Sign up button
        if st.button("🚀 Create Free Account", use_container_width=True, key="sidebar_signup"):
            st.switch_page("pages/5_⚙️_Authentication.py")
        
        # Quick benefits
        st.markdown("**🆓 Free Account Benefits:**")
        st.markdown("- 30-day price history")
        st.markdown("- Basic power law analysis")
        st.markdown("- Technical indicators")
    
    else:
        st.markdown("### ⚙️ Account")
        
        # Account info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{user['subscription'].title()} Plan**")
        with col2:
            # Plan status indicator
            plan_colors = {
                'free': '🟢',
                'premium': '🟡', 
                'pro': '🔴'
            }
            st.markdown(plan_colors.get(user['subscription'], '⚪'))
        
        # Quick actions
        if st.button("👤 Profile & Settings", use_container_width=True, key="sidebar_profile"):
            st.switch_page("pages/5_⚙️_Authentication.py")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout", type="secondary"):
            logout_user()
            st.rerun()
        
        # Upgrade prompt for free users
        if user['subscription'] == 'free':
            st.markdown("---")
            st.markdown("### ⬆️ Upgrade")
            st.info("Unlock premium features!")
            if st.button("⭐ Upgrade to Premium", key="sidebar_upgrade", use_container_width=True):
                st.switch_page("pages/5_⚙️_Authentication.py")

def render_sidebar_stats():
    """Render quick stats in sidebar"""
    from utils.data import get_market_stats, fetch_kaspa_price_data
    
    st.markdown("---")
    st.markdown("### ⚡ Market Stats")
    
    try:
        df = fetch_kaspa_price_data(7)  # Last 7 days for sidebar
        if not df.empty:
            stats = get_market_stats(df)
            
            # Current price with change
            price_change = stats.get('price_change_24h', 0)
            price_color = "green" if price_change >= 0 else "red"
            
            st.metric(
                "KAS Price", 
                f"${stats.get('current_price', 0):.4f}",
                delta=f"{price_change:+.2f}%"
            )
            
            # Volume
            st.metric(
                "24h Volume", 
                f"${stats.get('volume_24h', 0)/1000000:.1f}M"
            )
            
            # Quick trend indicator
            if price_change > 2:
                st.success("🚀 Strong Rally")
            elif price_change > 0:
                st.info("📈 Bullish")
            elif price_change < -2:
                st.error("📉 Decline")
            else:
                st.warning("📊 Sideways")
    
    except Exception as e:
        st.error("Unable to load market data")

def get_current_page():
    """Get the current page name for menu highlighting"""
    # This would be implemented to return the current page
    # for proper menu item highlighting
    return st.session_state.get('current_page', 'dashboard')

def set_current_page(page_name):
    """Set the current page for menu highlighting"""
    st.session_state.current_page = page_name
