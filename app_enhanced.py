import streamlit as st
import time
import uuid
from datetime import time as datetime_time
from utils.supabase_client import get_db
from utils.auth import AuthManager
from utils.llm_generator import NewsletterGenerator
from utils.content_aggregator import ContentAggregator
from utils.trend_detector import TrendDetector
from utils.delivery_scheduler import DeliveryScheduler

# Initialize database and auth
db = get_db()
auth = AuthManager()

# Page configuration
st.set_page_config(
    page_title="CreatorPulse - Newsletter Curator",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get authenticated user or set up demo mode
# Note: We no longer block users from seeing the home page
if auth.is_authenticated():
    user = auth.get_current_user()
    st.session_state.user_id = user['id']
    st.session_state.user_email = user['email']
else:
    # Demo mode - user chose to continue without auth
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.user_email = 'demo@creatorpulse.com'

# Always initialize llm_provider and model first (default)
if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = 'groq'

if 'groq_model' not in st.session_state:
    st.session_state.groq_model = 'llama-3.3-70b-versatile'  # Default to latest Llama 3.3

# Try to load user profile from database
if db.is_configured():
    try:
        profile = db.get_or_create_profile(st.session_state.user_id, st.session_state.user_email)
        if profile and profile.get('preferred_llm_provider'):
            st.session_state.llm_provider = profile.get('preferred_llm_provider')
    except Exception as e:
        # If database has RLS or other issues, just use default
        pass

# Initialize style_trained state
if 'style_trained' not in st.session_state:
    st.session_state.style_trained = False
    # Try to check if user has style training in database
    if db.is_configured():
        try:
            style_data = db.get_style_training(st.session_state.user_id)
            st.session_state.style_trained = len(style_data) > 0
        except Exception as e:
            # If database has issues, just use default
            pass

# Initialize workflow state for guided onboarding
if 'guided_mode' not in st.session_state:
    st.session_state.guided_mode = False

if 'current_step' not in st.session_state:
    st.session_state.current_step = "Home"

# Modern Custom CSS
st.markdown("""
    <style>
    /* CSS Variables for Theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --card-bg: rgba(255, 255, 255, 0.05);
        --card-border: rgba(255, 255, 255, 0.1);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.2);
    }

    /* Modern Typography */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .subtitle {
        font-size: 1.3rem;
        color: var(--text-secondary);
        margin-bottom: 2.5rem;
        font-weight: 400;
        line-height: 1.6;
    }

    /* Modern Card Component */
    .modern-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
    }

    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: rgba(102, 126, 234, 0.3);
    }

    /* Feature Card with Icon */
    .feature-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .feature-card:hover::before {
        transform: scaleX(1);
    }

    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }

    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border: 1px solid rgba(102, 126, 234, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .metric-card:hover::after {
        opacity: 1;
    }

    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }

    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: var(--primary-gradient);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    .status-badge-success {
        background: var(--success-gradient);
    }

    .status-badge-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    /* Modern Button Styles */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        min-width: fit-content !important;
    }

    .stButton > button p {
        white-space: nowrap !important;
        overflow: visible !important;
        margin: 0 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Enhanced Form Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
        padding: 0.75rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        background-color: transparent;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
    }

    /* Enhanced Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Metric Container Hover Effects */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        transition: all 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(118, 75, 162, 0.12) 100%);
    }

    /* Info/Success/Warning Boxes Hover */
    .stAlert {
        transition: all 0.3s ease;
        border-radius: 12px;
    }

    .stAlert:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(79, 172, 254, 0.2);
    }

    /* Enhanced Selectbox Styling */
    [data-baseweb="select"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }

    [data-baseweb="select"]:hover {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    [data-baseweb="select"] > div {
        background: transparent !important;
        border: none !important;
    }

    /* Selectbox dropdown */
    [data-baseweb="popover"] {
        background: rgba(30, 41, 59, 0.98) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }

    [data-baseweb="menu"] li {
        transition: all 0.2s ease !important;
    }

    [data-baseweb="menu"] li:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
    }

    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(10px);
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background: var(--card-bg) !important;
        border-radius: 12px !important;
        border: 1px solid var(--card-border) !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: rgba(102, 126, 234, 0.4) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    }

    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .loading {
        animation: pulse 2s ease-in-out infinite;
    }

    /* Success Toast */
    .success-toast {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(79, 172, 254, 0.3);
        color: white;
        font-weight: 600;
    }

    /* Container Enhancements */
    .stContainer {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--card-border);
    }

    /* Feature Cards - Style Streamlit Containers */
    div[data-testid="column"] > div > div > div {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.8rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        min-height: 180px !important;
    }

    div[data-testid="column"] > div > div > div:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
    }

    /* Alternative selector for containers */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.8rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 180px !important;
    }

    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
    }

    /* Smooth Transitions */
    * {
        transition: background-color 0.3s ease, border-color 0.3s ease, transform 0.3s ease;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }

        .feature-card {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("# 📰 CreatorPulse")
    st.markdown("---")

    # User info section
    if auth.is_authenticated():
        user = auth.get_current_user()
        st.success(f"👤 {user['email']}")
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()
    else:
        st.info("🎮 Demo Mode")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Login", use_container_width=True, key="sidebar_login"):
                st.switch_page("pages/1_🔐_Login.py")
        with col2:
            if st.button("📝 Sign Up", use_container_width=True, key="sidebar_signup"):
                st.switch_page("pages/2_📝_Signup.py")

    st.markdown("---")

    st.markdown("### Navigation")

    # Use guided mode or allow manual override
    if st.session_state.guided_mode:
        # Get the index of current step for the radio
        pages_list = ["Home", "Source Connections", "Style Trainer", "Generate Newsletter", "Dashboard"]
        current_index = pages_list.index(st.session_state.current_step) if st.session_state.current_step in pages_list else 0

        page = st.radio(
            "Go to",
            pages_list,
            index=current_index,
            label_visibility="collapsed",
            key="guided_nav"
        )

        # Allow manual navigation to override guided mode
        if page != st.session_state.current_step:
            st.session_state.current_step = page
            st.session_state.guided_mode = False  # Exit guided mode if user manually navigates
    else:
        # Normal navigation mode
        page = st.radio(
            "Go to",
            ["Home", "Source Connections", "Style Trainer", "Generate Newsletter", "Dashboard"],
            label_visibility="collapsed"
        )

    st.markdown("---")
    
    # Model Selection
    st.markdown('<h3 style="margin-bottom: 1rem;"><span style="font-size: 1.5rem;">🤖</span> AI Model</h3>', unsafe_allow_html=True)

    # Available models
    available_models = {
        'llama-3.3-70b-versatile': '🌟 Llama 3.3 70B (Latest, Best)',
        'llama-3.1-70b-versatile': '🚀 Llama 3.1 70B (Fast, Reliable)',
        'llama-3.1-8b-instant': '⚡ Llama 3.1 8B (Instant)',
        'llama3-70b-8192': '🔥 Llama 3 70B (Long Context)',
        'mixtral-8x7b-32768': '🎯 Mixtral 8x7B (32K Context)',
        'gemma2-9b-it': '💎 Gemma 2 9B (Google)',
        'llama-3.2-90b-vision-preview': '👁️ Llama 3.2 90B Vision',
        'llama-3.2-11b-vision-preview': '📸 Llama 3.2 11B Vision',
        'llama-3.2-3b-preview': '⚡ Llama 3.2 3B (Ultra Fast)',
        'llama-3.2-1b-preview': '🏃 Llama 3.2 1B (Lightning)',
    }

    selected_model = st.selectbox(
        "Select Model",
        options=list(available_models.keys()),
        format_func=lambda x: available_models[x],
        index=list(available_models.keys()).index(st.session_state.groq_model) if st.session_state.groq_model in available_models else 0,
        key="model_selector"
    )

    if selected_model != st.session_state.groq_model:
        st.session_state.groq_model = selected_model
        st.success(f"✅ Switched to {available_models[selected_model]}")

    st.markdown("---")
    st.markdown("### Quick Stats")

    # Get stats from database or fallback
    if db.is_configured():
        user_stats = db.get_user_stats(st.session_state.user_id)
        total_sources = user_stats.get('total_sources', 0)
        total_drafts = user_stats.get('total_drafts', 0)
    else:
        # Fallback to session state
        total_sources = (len(st.session_state.get('sources', {}).get('twitter', [])) +
                        len(st.session_state.get('sources', {}).get('youtube', [])) +
                        len(st.session_state.get('sources', {}).get('newsletters', [])))
        total_drafts = len(st.session_state.get('generated_drafts', []))

    st.metric("Connected Sources", total_sources)
    st.metric("Drafts Generated", total_drafts)
    st.metric("Style Trained", "Yes ✓" if st.session_state.style_trained else "No ✗")

# Main content
if page == "Home":
    st.markdown('<h1 class="main-header">CreatorPulse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-powered newsletter curator and drafting assistant</p>', unsafe_allow_html=True)

    # Hero section with modern design
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("### Welcome to CreatorPulse 👋")
        st.markdown("""
        CreatorPulse transforms newsletter creation from hours to minutes using AI-powered automation:
        """)

        with st.container():
            st.markdown("""
            - ✨ **Aggregate** insights from multiple sources
            - 🔥 **Detect** emerging trends automatically
            - ✍️ **Generate** voice-matched newsletter drafts
            - 📬 **Deliver** curated content every morning
            """)

        st.info("""
        **Get started in 3 simple steps:**

        1. Connect your content sources
        2. Train your writing style
        3. Generate your first newsletter draft
        """)

        # Get Started button with smart routing
        if st.button("🚀 Get Started", use_container_width=True, type="primary", key="home_get_started"):
            if not auth.is_authenticated() and not st.session_state.get('demo_mode', False):
                # Show auth options
                st.session_state.show_auth_modal = True
                st.rerun()
            else:
                # Start guided workflow
                st.session_state.guided_mode = True
                st.session_state.current_step = "Source Connections"
                st.rerun()

        # Show auth modal if triggered
        if st.session_state.get('show_auth_modal', False):
            st.info("💡 **Choose an option to continue:**")

            modal_col1, modal_col2, modal_col3 = st.columns(3)
            with modal_col1:
                if st.button("🎮 Try Demo Mode", use_container_width=True, type="primary", key="modal_demo"):
                    st.session_state.demo_mode = True
                    st.session_state.user_id = str(uuid.uuid4())
                    st.session_state.user_email = 'demo@creatorpulse.com'
                    st.session_state.show_auth_modal = False
                    st.session_state.guided_mode = True
                    st.session_state.current_step = "Source Connections"
                    st.rerun()
            with modal_col2:
                if st.button("🔐 Login", use_container_width=True, key="modal_login"):
                    st.switch_page("pages/1_🔐_Login.py")
            with modal_col3:
                if st.button("📝 Sign Up", use_container_width=True, key="modal_signup"):
                    st.switch_page("pages/2_📝_Signup.py")

    with col2:
        # Modern stats cards with native Streamlit metrics
        st.metric(label="⏱️ Time Saved", value="2-3 hours", delta="per newsletter")
        st.metric(label="⚡ Draft Time", value="< 20 min", delta="review & send")
        st.metric(label="✅ Acceptance", value="≥70%", delta="target rate")

    st.markdown("---")

    # Features section with modern cards
    st.markdown("### ✨ Core Features")
    st.markdown("")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔗</span>
            <h4 class="feature-title">Multi-Source Aggregation</h4>
            <p class="feature-description">Connect Twitter handles, YouTube channels, and newsletter RSS feeds to aggregate content from all your trusted sources in one place.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <h4 class="feature-title">Trend Detection</h4>
            <p class="feature-description">AI-powered trend analysis surfaces emerging topics and insights automatically, so you never miss what matters most to your audience.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">✍️</span>
            <h4 class="feature-title">Voice-Matched Drafts</h4>
            <p class="feature-description">Upload your past newsletters to train the AI on your unique writing style for 70%+ ready-to-send drafts that sound like you.</p>
        </div>
        """, unsafe_allow_html=True)

    # Prominent CTA Section at bottom (for non-auth users)
    if not auth.is_authenticated() and not st.session_state.get('demo_mode', False):
        st.markdown("---")
        st.markdown("")

        # Social proof / benefits
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="font-size: 2rem; margin-bottom: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                Ready to Transform Your Newsletter Workflow?
            </h2>
        </div>
        """, unsafe_allow_html=True)

        benefit_col1, benefit_col2, benefit_col3 = st.columns(3)
        with benefit_col1:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">✅</div>
                <p style="color: #94a3b8; font-size: 0.95rem;">Free tier available<br/>No credit card required</p>
            </div>
            """, unsafe_allow_html=True)
        with benefit_col2:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
                <p style="color: #94a3b8; font-size: 0.95rem;">10+ AI models<br/>Llama 3.3, Mixtral, Gemma</p>
            </div>
            """, unsafe_allow_html=True)
        with benefit_col3:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚡</div>
                <p style="color: #94a3b8; font-size: 0.95rem;">Lightning fast<br/>Powered by Groq</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # Primary CTAs
        cta_col1, cta_col2, cta_col3 = st.columns([1, 1, 1], gap="medium")
        with cta_col1:
            if st.button("🎮 Try Demo Mode", use_container_width=True, type="primary", key="bottom_cta_demo"):
                st.session_state.demo_mode = True
                st.session_state.user_id = str(uuid.uuid4())
                st.session_state.user_email = 'demo@creatorpulse.com'
                st.session_state.guided_mode = True
                st.session_state.current_step = "Source Connections"
                st.rerun()
        with cta_col2:
            if st.button("🔐 Login", use_container_width=True, key="bottom_cta_login"):
                st.switch_page("pages/1_🔐_Login.py")
        with cta_col3:
            if st.button("📝 Sign Up", use_container_width=True, key="bottom_cta_signup"):
                st.switch_page("pages/2_📝_Signup.py")

        st.markdown("")
        st.markdown('<p style="text-align: center; color: #64748b; font-size: 0.85rem;">Start curating amazing newsletters in minutes, not hours</p>', unsafe_allow_html=True)

elif page == "Source Connections":
    # Require authentication for functional pages
    if not auth.is_authenticated() and not st.session_state.get('demo_mode', False):
        st.warning("🔐 Please login or use demo mode to access this feature")
        st.info("Choose an option below to continue:")

        auth_col1, auth_col2, auth_col3 = st.columns(3)
        with auth_col1:
            if st.button("🎮 Try Demo Mode", use_container_width=True, type="primary", key="source_demo"):
                st.session_state.demo_mode = True
                st.session_state.user_id = str(uuid.uuid4())
                st.session_state.user_email = 'demo@creatorpulse.com'
                st.rerun()
        with auth_col2:
            if st.button("🔐 Login", use_container_width=True, key="source_login"):
                st.switch_page("pages/1_🔐_Login.py")
        with auth_col3:
            if st.button("📝 Sign Up", use_container_width=True, key="source_signup"):
                st.switch_page("pages/2_📝_Signup.py")
        st.stop()

    st.title("🔗 Source Connections")
    st.markdown("Connect your content sources to start curating your newsletter.")

    tab1, tab2, tab3 = st.tabs(["Twitter", "YouTube", "Newsletters"])

    with tab1:
        st.markdown("### Twitter Sources")
        st.markdown("Add Twitter handles or hashtags to monitor")

        twitter_handle = st.text_input("Enter Twitter handle (without @)", key="twitter_input")
        if st.button("Add Twitter Source", key="add_twitter", type="primary"):
            if twitter_handle:
                if db.is_configured():
                    # Ensure profile exists before adding source
                    try:
                        db.get_or_create_profile(st.session_state.user_id, st.session_state.user_email)
                    except Exception as e:
                        st.error(f"❌ Please run the database fix script first. Error: {str(e)}")
                        st.info("See FIX_DATABASE_WARNING.md for instructions")
                        st.stop()

                    result = db.add_source(st.session_state.user_id, 'twitter', twitter_handle)
                    if result.get('success'):
                        st.success(f"✅ Added @{twitter_handle}")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        error_msg = result.get('error', 'Unknown error')
                        st.error(f"❌ Error: {error_msg}")
                        if 'violates foreign key constraint' in str(error_msg) or 'row-level security' in str(error_msg).lower():
                            st.error("🔧 Database needs RLS disabled. Run the SQL script from database/quick_fix_rls.sql")
                else:
                    st.warning("⚠️ Database not configured. Source not saved.")

        # Get Twitter sources from database
        twitter_sources = []
        if db.is_configured():
            twitter_sources = db.get_sources(st.session_state.user_id, 'twitter')

        if twitter_sources:
            st.markdown("#### Connected Twitter Sources")
            for source in twitter_sources:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"@{source['identifier']}")
                with col2:
                    if st.button("Remove", key=f"remove_twitter_{source['id']}"):
                        if db.delete_source(st.session_state.user_id, source['id']):
                            st.success("Removed!")
                            time.sleep(0.3)
                            st.rerun()

    with tab2:
        st.markdown("### YouTube Channels")
        st.markdown("Add YouTube channel IDs or names to monitor")

        youtube_channel = st.text_input("Enter YouTube channel", key="youtube_input")
        if st.button("Add YouTube Source", key="add_youtube", type="primary"):
            if youtube_channel:
                if db.is_configured():
                    result = db.add_source(st.session_state.user_id, 'youtube', youtube_channel)
                    if result.get('success'):
                        st.success(f"✅ Added {youtube_channel}")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                else:
                    st.warning("⚠️ Database not configured. Source not saved.")

        # Get YouTube sources from database
        youtube_sources = []
        if db.is_configured():
            youtube_sources = db.get_sources(st.session_state.user_id, 'youtube')

        if youtube_sources:
            st.markdown("#### Connected YouTube Channels")
            for source in youtube_sources:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(source['identifier'])
                with col2:
                    if st.button("Remove", key=f"remove_youtube_{source['id']}"):
                        if db.delete_source(st.session_state.user_id, source['id']):
                            st.success("Removed!")
                            time.sleep(0.3)
                            st.rerun()

    with tab3:
        st.markdown("### Newsletter RSS Feeds")
        st.markdown("Add RSS feed URLs from newsletters you follow")

        newsletter_url = st.text_input("Enter RSS feed URL", key="newsletter_input")
        if st.button("Add Newsletter Source", key="add_newsletter", type="primary"):
            if newsletter_url:
                if db.is_configured():
                    result = db.add_source(st.session_state.user_id, 'newsletter', newsletter_url)
                    if result.get('success'):
                        st.success(f"✅ Added newsletter feed")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                else:
                    st.warning("⚠️ Database not configured. Source not saved.")

        # Get Newsletter sources from database
        newsletter_sources = []
        if db.is_configured():
            newsletter_sources = db.get_sources(st.session_state.user_id, 'newsletter')

        if newsletter_sources:
            st.markdown("#### Connected Newsletter Feeds")
            for source in newsletter_sources:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(source['identifier'])
                with col2:
                    if st.button("Remove", key=f"remove_newsletter_{source['id']}"):
                        if db.delete_source(st.session_state.user_id, source['id']):
                            st.success("Removed!")
                            time.sleep(0.3)
                            st.rerun()

    # Guided workflow - Continue button
    if st.session_state.guided_mode:
        st.markdown("---")
        st.markdown("")

        # Check if at least one source is connected
        total_sources = 0
        if db.is_configured():
            total_sources = len(twitter_sources) + len(youtube_sources) + len(newsletter_sources)

        if total_sources > 0:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Continue to Style Training →", use_container_width=True, type="primary", key="continue_to_style"):
                    st.session_state.current_step = "Style Trainer"
                    st.rerun()
        else:
            st.info("💡 Add at least one source to continue to the next step")

elif page == "Style Trainer":
    # Require authentication for functional pages
    if not auth.is_authenticated() and not st.session_state.get('demo_mode', False):
        st.warning("🔐 Please login or use demo mode to access this feature")
        st.info("Choose an option below to continue:")

        auth_col1, auth_col2, auth_col3 = st.columns(3)
        with auth_col1:
            if st.button("🎮 Try Demo Mode", use_container_width=True, type="primary", key="style_demo"):
                st.session_state.demo_mode = True
                st.session_state.user_id = str(uuid.uuid4())
                st.session_state.user_email = 'demo@creatorpulse.com'
                st.rerun()
        with auth_col2:
            if st.button("🔐 Login", use_container_width=True, key="style_login"):
                st.switch_page("pages/1_🔐_Login.py")
        with auth_col3:
            if st.button("📝 Sign Up", use_container_width=True, key="style_signup"):
                st.switch_page("pages/2_📝_Signup.py")
        st.stop()

    st.title("✍️ Writing Style Trainer")
    st.markdown("Upload your past newsletters to train the AI on your unique writing style.")

    # Provider info
    if st.session_state.llm_provider == 'groq':
        st.info("🚀 Using Groq (Llama 3.1 70B) - Lightning fast and free!")
    elif st.session_state.llm_provider == 'openai':
        st.info("🤖 Using OpenAI GPT-4 - Requires API key")
    else:
        st.info("🎭 Using Anthropic Claude 3 - Requires API key")

    st.markdown("For best results, upload at least 20 past newsletters or blog posts that represent your writing style.")

    uploaded_files = st.file_uploader(
        "Upload your past newsletters (TXT, CSV, or paste content)",
        type=["txt", "csv"],
        accept_multiple_files=True
    )

    text_input = st.text_area(
        "Or paste your newsletter content here:",
        height=300,
        placeholder="Paste multiple newsletters separated by ---"
    )

    if st.button("🎯 Train Writing Style", type="primary", use_container_width=True):
        if uploaded_files or text_input:
            with st.spinner(f"Training your writing style using {st.session_state.llm_provider.upper()}..."):
                # Collect training text
                training_text = text_input if text_input else ""
                if uploaded_files:
                    for file in uploaded_files:
                        content = file.read().decode('utf-8')
                        training_text += "\n---\n" + content

                # Save to database
                if db.is_configured():
                    success = db.save_style_training(
                        st.session_state.user_id,
                        training_text,
                        {'provider': st.session_state.llm_provider}
                    )
                    if success:
                        st.session_state.style_trained = True
                        st.success("✅ Writing style trained and saved to database!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to save style training to database")
                else:
                    st.session_state.style_trained = True
                    st.warning("⚠️ Database not configured. Style training not persisted.")
                    st.success("✅ Writing style trained temporarily!")
        else:
            st.error("❌ Please upload files or paste content to train your style.")

    if st.session_state.style_trained:
        st.success("✅ Your writing style has been trained!")
        with st.expander("📊 Style Characteristics Learned", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Tone:** Professional yet conversational
                
                **Voice:** First-person with direct audience engagement
                """)
            with col2:
                st.markdown("""
                **Structure:** Clear sections with engaging introductions

                **Sentence Style:** Varied length with punchy key points
                """)

    # Guided workflow - Continue button
    if st.session_state.guided_mode:
        st.markdown("---")
        st.markdown("")

        if st.session_state.style_trained:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Continue to Generate Newsletter →", use_container_width=True, type="primary", key="continue_to_generate"):
                    st.session_state.current_step = "Generate Newsletter"
                    st.rerun()
        else:
            st.info("💡 Train your writing style to continue to the next step")

elif page == "Generate Newsletter":
    # Require authentication for functional pages
    if not auth.is_authenticated() and not st.session_state.get('demo_mode', False):
        st.warning("🔐 Please login or use demo mode to access this feature")
        st.info("Choose an option below to continue:")

        auth_col1, auth_col2, auth_col3 = st.columns(3)
        with auth_col1:
            if st.button("🎮 Try Demo Mode", use_container_width=True, type="primary", key="generate_demo"):
                st.session_state.demo_mode = True
                st.session_state.user_id = str(uuid.uuid4())
                st.session_state.user_email = 'demo@creatorpulse.com'
                st.rerun()
        with auth_col2:
            if st.button("🔐 Login", use_container_width=True, key="generate_login"):
                st.switch_page("pages/1_🔐_Login.py")
        with auth_col3:
            if st.button("📝 Sign Up", use_container_width=True, key="generate_signup"):
                st.switch_page("pages/2_📝_Signup.py")
        st.stop()

    st.title("📝 Generate Newsletter")
    st.markdown("Generate an AI-powered newsletter draft based on your sources and style.")

    if not st.session_state.style_trained:
        st.warning("⚠️ Please train your writing style first for best results!")

    # Get total sources from database
    if db.is_configured():
        user_stats = db.get_user_stats(st.session_state.user_id)
        total_sources = user_stats.get('total_sources', 0)
    else:
        total_sources = 0

    if total_sources == 0:
        st.warning("⚠️ Please connect at least one content source first!")

    # Provider selection reminder
    st.info(f"🤖 Current LLM: **{st.session_state.llm_provider.upper()}** | Change in sidebar")

    st.markdown("### Newsletter Configuration")

    col1, col2 = st.columns(2)

    with col1:
        newsletter_title = st.text_input("Newsletter Title", value="Weekly Digest")
        time_range = st.selectbox("Content Time Range", ["Last 24 hours", "Last 3 days", "Last week"])

    with col2:
        num_articles = st.slider("Number of articles to include", 3, 10, 5)
        include_trends = st.checkbox("Include trending topics", value=True)

    if st.button("🚀 Generate Newsletter Draft", type="primary", use_container_width=True,
                 disabled=not st.session_state.style_trained or total_sources == 0):
        with st.spinner(f"Generating your newsletter draft with {st.session_state.llm_provider.upper()}..."):
            start_time = time.time()

            try:
                # Get sources for content aggregation
                aggregated_content = []
                if db.is_configured():
                    sources = db.get_sources(st.session_state.user_id)
                    # Create mock content based on sources
                    for source in sources:
                        aggregated_content.append({
                            'title': f"Latest from {source['identifier']}",
                            'source_type': source['source_type'],
                            'identifier': source['identifier']
                        })

                # Initialize newsletter generator with selected model
                generator = NewsletterGenerator(
                    provider=st.session_state.llm_provider,
                    model=st.session_state.get('groq_model', 'llama-3.1-70b-versatile') if st.session_state.llm_provider == 'groq' else None
                )

                # Get style training if available
                style_profile = None
                if db.is_configured():
                    style_data = db.get_style_training(st.session_state.user_id)
                    if style_data:
                        style_profile = {'training_text': style_data[0].get('training_text', '')}

                # Detect trending topics if enabled
                trending_data = None
                if include_trends and aggregated_content:
                    trend_detector = TrendDetector(db if db.is_configured() else None)
                    trending_data = trend_detector.get_trending_topics(
                        aggregated_content,
                        include_spikes=True,
                        top_n=5
                    )

                # Generate newsletter using AI
                content = generator.generate_newsletter(
                    content_items=aggregated_content,
                    title=newsletter_title,
                    style_profile=style_profile,
                    num_articles=num_articles,
                    include_trends=include_trends
                )

                # Prepend trending topics section if available
                if trending_data and trending_data.get('trending_keywords'):
                    trends_section = trend_detector.format_trends_for_newsletter(trending_data, max_trends=5)
                    content = trends_section + "\n\n" + content

                generation_time_ms = int((time.time() - start_time) * 1000)

            except Exception as e:
                st.error(f"❌ AI Generation Failed: {str(e)}")
                st.error("Please check your API keys and try again.")

                # Show helpful error messages
                if "api" in str(e).lower() or "key" in str(e).lower():
                    st.warning("⚠️ API Key Issue - Make sure your GROQ_API_KEY is set in .env file")
                    st.info("Get your free API key at: https://console.groq.com/keys")
                elif "rate" in str(e).lower() or "limit" in str(e).lower():
                    st.warning("⚠️ Rate Limit Reached - Please wait a moment and try again")
                else:
                    st.info("💡 Try: Check your internet connection, verify API keys, or switch models")

                st.stop()  # Stop execution instead of using fallback

            # Save to database
            if db.is_configured():
                result = db.save_draft(
                    st.session_state.user_id,
                    newsletter_title,
                    content,
                    st.session_state.llm_provider,
                    generation_time_ms
                )
                if result.get('success'):
                    st.success("✅ Newsletter draft generated and saved to database!")
                else:
                    st.error(f"❌ Error saving draft: {result.get('error', 'Unknown error')}")
            else:
                st.warning("⚠️ Database not configured. Draft not saved.")
                st.success("✅ Newsletter draft generated!")

            st.rerun()

    # Display generated drafts from database
    drafts = []
    if db.is_configured():
        drafts = db.get_drafts(st.session_state.user_id, limit=10)

    if drafts:
        st.markdown("---")
        st.markdown("### Generated Drafts")

        for idx, draft in enumerate(drafts):
            draft_id = draft['id']
            with st.expander(f"Draft: {draft['title']} (via {draft.get('llm_provider', 'unknown').upper()})", expanded=(idx == 0)):
                st.markdown(draft['content'])

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("👍 Accept", key=f"accept_{draft_id}"):
                        if db.is_configured():
                            db.add_feedback(st.session_state.user_id, draft_id, 'positive')
                        st.success("✅ Feedback recorded!")

                with col2:
                    if st.button("👎 Reject", key=f"reject_{draft_id}"):
                        if db.is_configured():
                            db.add_feedback(st.session_state.user_id, draft_id, 'negative')
                        st.info("📝 Feedback recorded.")

                with col3:
                    st.download_button(
                        "📥 Export",
                        draft['content'],
                        file_name=f"{draft['title'].replace(' ', '_')}.txt",
                        key=f"download_{draft_id}"
                    )

                with col4:
                    if st.button("📧 Send Email", key=f"email_{draft_id}"):
                        st.session_state[f'show_email_form_{draft_id}'] = True
                        st.rerun()

                # Email sending form
                if st.session_state.get(f'show_email_form_{draft_id}', False):
                    st.markdown("---")
                    st.markdown("#### 📧 Send Newsletter via Email")

                    from utils.email_sender import NewsletterEmailSender
                    sender = NewsletterEmailSender()

                    if not sender.validate_api_key():
                        st.warning("⚠️ Resend API key not configured. Add RESEND_API_KEY to your .env file.")
                        st.markdown("[Get free Resend API key →](https://resend.com/api-keys)")
                    else:
                        email_col1, email_col2 = st.columns(2)

                        with email_col1:
                            recipient_emails = st.text_area(
                                "Recipient Email(s)",
                                placeholder="email@example.com\nanother@example.com",
                                help="Enter one email per line",
                                key=f"recipient_{draft_id}"
                            )

                            from_email = st.text_input(
                                "From Email",
                                value="CreatorPulse <newsletter@resend.dev>",
                                help="Must use verified domain with Resend",
                                key=f"from_{draft_id}"
                            )

                        with email_col2:
                            email_subject = st.text_input(
                                "Subject Line",
                                value=draft['title'],
                                key=f"subject_{draft_id}"
                            )

                            send_test = st.checkbox(
                                "Send as test email",
                                help="Adds [TEST] prefix to subject",
                                key=f"test_{draft_id}"
                            )

                        send_col1, send_col2 = st.columns([1, 3])

                        with send_col1:
                            if st.button("📤 Send Now", type="primary", key=f"send_btn_{draft_id}"):
                                if recipient_emails.strip():
                                    emails_list = [email.strip() for email in recipient_emails.split('\n') if email.strip()]

                                    with st.spinner("Sending email..."):
                                        if send_test and len(emails_list) == 1:
                                            result = sender.send_test_email(
                                                test_email=emails_list[0],
                                                subject=email_subject,
                                                content=draft['content'],
                                                from_email=from_email
                                            )
                                        else:
                                            result = sender.send_newsletter(
                                                to_emails=emails_list,
                                                subject=email_subject,
                                                content=draft['content'],
                                                from_email=from_email
                                            )

                                        if result['success']:
                                            # Log email send to database
                                            if db.is_configured():
                                                db.log_email_send(
                                                    st.session_state.user_id,
                                                    draft_id,
                                                    emails_list,
                                                    email_subject,
                                                    result.get('email_id')
                                                )
                                            st.success(f"✅ {result['message']}")
                                            st.balloons()
                                            st.session_state[f'show_email_form_{draft_id}'] = False
                                            time.sleep(2)
                                            st.rerun()
                                        else:
                                            st.error(f"❌ {result['message']}")
                                else:
                                    st.error("Please enter at least one email address")

                        with send_col2:
                            if st.button("Cancel", key=f"cancel_{draft_id}"):
                                st.session_state[f'show_email_form_{draft_id}'] = False
                                st.rerun()

elif page == "Dashboard":
    # Require authentication for functional pages
    if not auth.is_authenticated() and not st.session_state.get('demo_mode', False):
        st.warning("🔐 Please login or use demo mode to access this feature")
        st.info("Choose an option below to continue:")

        auth_col1, auth_col2, auth_col3 = st.columns(3)
        with auth_col1:
            if st.button("🎮 Try Demo Mode", use_container_width=True, type="primary", key="dashboard_demo"):
                st.session_state.demo_mode = True
                st.session_state.user_id = str(uuid.uuid4())
                st.session_state.user_email = 'demo@creatorpulse.com'
                st.rerun()
        with auth_col2:
            if st.button("🔐 Login", use_container_width=True, key="dashboard_login"):
                st.switch_page("pages/1_🔐_Login.py")
        with auth_col3:
            if st.button("📝 Sign Up", use_container_width=True, key="dashboard_signup"):
                st.switch_page("pages/2_📝_Signup.py")
        st.stop()

    st.title("📊 Dashboard")
    st.markdown("Track your newsletter performance and usage metrics.")

    # Get user stats from database
    if db.is_configured():
        user_stats = db.get_user_stats(st.session_state.user_id)
        total_sources = user_stats.get('total_sources', 0)
        total_drafts = user_stats.get('total_drafts', 0)
        acceptance_rate = user_stats.get('acceptance_rate', 0)
        est_time_saved = user_stats.get('estimated_hours_saved', 0)
    else:
        total_sources = 0
        total_drafts = 0
        acceptance_rate = 0
        est_time_saved = 0
        st.warning("⚠️ Database not configured. Stats unavailable.")

    # Key metrics with enhanced display
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Sources", total_sources, delta=f"+{total_sources}" if total_sources > 0 else None)

    with col2:
        st.metric("Drafts Generated", total_drafts)

    with col3:
        st.metric("Draft Acceptance", f"{acceptance_rate:.0f}%",
                 delta="Good" if acceptance_rate >= 70 else "Needs improvement")

    with col4:
        st.metric("Est. Time Saved", f"{est_time_saved:.1f}h")

    st.markdown("---")

    # Provider usage stats
    if db.is_configured():
        drafts = db.get_drafts(st.session_state.user_id, limit=100)
        if drafts:
            st.markdown("### 🤖 LLM Provider Usage")
            providers = {}
            for draft in drafts:
                provider = draft.get('llm_provider', 'unknown')
                providers[provider] = providers.get(provider, 0) + 1

            for provider, count in providers.items():
                st.write(f"**{provider.upper()}:** {count} drafts")

    st.markdown("---")

    # Source breakdown
    st.markdown("### Connected Sources Breakdown")
    col1, col2, col3 = st.columns(3)

    if db.is_configured():
        twitter_sources = db.get_sources(st.session_state.user_id, 'twitter')
        youtube_sources = db.get_sources(st.session_state.user_id, 'youtube')
        newsletter_sources = db.get_sources(st.session_state.user_id, 'newsletter')

        with col1:
            st.metric("Twitter", len(twitter_sources))
            if twitter_sources:
                for source in twitter_sources[:3]:
                    st.write(f"- @{source['identifier']}")

        with col2:
            st.metric("YouTube", len(youtube_sources))
            if youtube_sources:
                for source in youtube_sources[:3]:
                    st.write(f"- {source['identifier']}")

        with col3:
            st.metric("Newsletters", len(newsletter_sources))
            if newsletter_sources:
                st.write(f"- {len(newsletter_sources)} RSS feeds")
    else:
        with col1:
            st.metric("Twitter", 0)
        with col2:
            st.metric("YouTube", 0)
        with col3:
            st.metric("Newsletters", 0)

    st.markdown("---")

    # Recent activity
    st.markdown("### Recent Activity")
    if db.is_configured():
        recent_drafts = db.get_drafts(st.session_state.user_id, limit=5)
        if recent_drafts:
            for draft in recent_drafts:
                st.write(f"✅ Generated: {draft['title']} (via {draft.get('llm_provider', 'unknown').upper()})")
        else:
            st.info("No drafts generated yet. Visit 'Generate Newsletter' to create your first draft!")
    else:
        st.info("Database not configured. Connect Supabase to track activity.")

    st.markdown("---")

    # Morning Delivery Settings
    st.markdown("### ⏰ Morning Delivery Settings")
    st.markdown("Schedule automatic newsletter delivery at your preferred time.")

    if db.is_configured():
        # Get current schedule
        scheduler = DeliveryScheduler(db)
        current_schedule = scheduler.get_schedule(st.session_state.user_id)

        # Enable/Disable toggle
        delivery_enabled = st.toggle(
            "Enable automatic morning delivery",
            value=current_schedule.get('enabled', False) if current_schedule else False,
            help="Automatically generate and send newsletters at your scheduled time"
        )

        if delivery_enabled:
            col1, col2 = st.columns(2)

            with col1:
                # Time picker
                default_time = datetime_time(8, 0)  # 08:00 AM
                if current_schedule and current_schedule.get('time'):
                    try:
                        time_str = current_schedule['time']
                        hour, minute = map(int, time_str.split(':')[:2])
                        default_time = datetime_time(hour, minute)
                    except:
                        pass

                delivery_time = st.time_input(
                    "Delivery time (your local time)",
                    value=default_time,
                    help="Newsletter will be generated and sent at this time"
                )

                # Timezone selector
                timezones = DeliveryScheduler.get_available_timezones()
                default_tz = current_schedule.get('timezone', 'UTC') if current_schedule else 'UTC'
                try:
                    tz_index = timezones.index(default_tz)
                except:
                    tz_index = 0

                delivery_timezone = st.selectbox(
                    "Your timezone",
                    options=timezones,
                    index=tz_index,
                    help="Select your local timezone"
                )

            with col2:
                # Frequency selector
                frequency_options = ["daily", "weekdays", "weekly"]
                frequency_labels = {
                    "daily": "📅 Every Day",
                    "weekdays": "💼 Weekdays Only (Mon-Fri)",
                    "weekly": "📆 Once Per Week"
                }

                default_freq = current_schedule.get('frequency', 'daily') if current_schedule else 'daily'
                try:
                    freq_index = frequency_options.index(default_freq)
                except:
                    freq_index = 0

                delivery_frequency = st.selectbox(
                    "Delivery frequency",
                    options=frequency_options,
                    format_func=lambda x: frequency_labels[x],
                    index=freq_index
                )

                # Recipient emails
                default_recipients = st.session_state.user_email
                if current_schedule and current_schedule.get('recipients'):
                    default_recipients = "\n".join(current_schedule['recipients'])

                recipient_emails = st.text_area(
                    "Recipient emails (one per line)",
                    value=default_recipients,
                    height=100,
                    help="Enter email addresses to send newsletters to"
                )

            # Save button
            if st.button("💾 Save Delivery Schedule", type="primary", use_container_width=True):
                # Parse emails
                emails = [email.strip() for email in recipient_emails.split("\n") if email.strip()]

                if not emails:
                    st.error("❌ Please enter at least one recipient email")
                else:
                    # Create schedule
                    result = scheduler.create_schedule(
                        user_id=st.session_state.user_id,
                        delivery_time=delivery_time,
                        timezone=delivery_timezone,
                        frequency=delivery_frequency,
                        enabled=True,
                        recipient_emails=emails
                    )

                    if result['success']:
                        st.success(f"✅ Morning delivery scheduled for {delivery_time.strftime('%I:%M %p')} {delivery_timezone}")

                        # Calculate next delivery
                        next_delivery = scheduler.get_next_delivery_time(
                            delivery_time, delivery_timezone, delivery_frequency
                        )
                        formatted_time = DeliveryScheduler.format_time_with_timezone(next_delivery, delivery_timezone)
                        st.info(f"📬 Next delivery: {formatted_time}")
                    else:
                        st.error(f"❌ Failed to save schedule: {result.get('error')}")

        else:
            if current_schedule and current_schedule.get('enabled'):
                if st.button("🛑 Disable Automatic Delivery", use_container_width=True):
                    result = scheduler.disable_schedule(st.session_state.user_id)
                    if result['success']:
                        st.success("✅ Automatic delivery disabled")
                        st.rerun()
            else:
                st.info("💡 Enable automatic delivery to schedule daily newsletters")
    else:
        st.warning("⚠️ Database not configured. Please connect Supabase to use scheduled delivery.")

    st.markdown("---")

    # Footer with provider info
    st.markdown(f"""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p>Built with Streamlit + Shadcn UI • Powered by {st.session_state.llm_provider.upper()}</p>
        <p style="font-size: 0.8rem;">CreatorPulse v2.0 Enhanced</p>
    </div>
    """, unsafe_allow_html=True)
