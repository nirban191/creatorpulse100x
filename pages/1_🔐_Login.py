"""
Login Page for CreatorPulse
"""

import streamlit as st
from utils.auth import AuthManager

# Page config
st.set_page_config(
    page_title="Login - CreatorPulse",
    page_icon="🔐",
    layout="centered"
)

# Initialize auth manager
auth = AuthManager()

# Modern Custom CSS
st.markdown("""
    <style>
    /* CSS Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-bg: rgba(255, 255, 255, 0.05);
        --card-border: rgba(255, 255, 255, 0.1);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
    }

    /* Animated Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    /* Modern Form Container */
    .stForm {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }

    /* Enhanced Form Inputs */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* Modern Buttons */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }

    /* Checkbox Styling */
    .stCheckbox {
        color: var(--text-secondary) !important;
    }

    /* Info/Alert Boxes */
    .stAlert {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }

    /* Section Cards */
    .login-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .login-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Center Container */
    .block-container {
        max-width: 500px;
        padding-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Check if already authenticated
if auth.is_authenticated():
    st.markdown('<h1 class="main-header">✅ Welcome Back!</h1>', unsafe_allow_html=True)
    user = auth.get_current_user()

    st.success(f"You are already logged in as **{user['email']}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Go to Dashboard", type="primary", use_container_width=True):
            st.switch_page("app_enhanced.py")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()
    st.stop()

# Header
st.markdown('<h1 class="main-header">🔐 CreatorPulse</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sign in to your account</p>', unsafe_allow_html=True)

# Login form
with st.form("login_form"):
    st.markdown("### Login Credentials")

    email = st.text_input(
        "Email Address",
        placeholder="your@email.com",
        help="Enter your registered email address"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        help="Your account password"
    )

    st.markdown("")

    col1, col2 = st.columns([2, 1])
    with col1:
        submit = st.form_submit_button("🔐 Sign In", use_container_width=True, type="primary")
    with col2:
        remember = st.checkbox("Remember me", value=True)

# Handle login submission
if submit:
    if not email or not password:
        st.error("❌ Please fill in all fields")
    else:
        with st.spinner("Logging in..."):
            result = auth.login(email, password)

            if result['success']:
                st.success(f"✅ {result['message']}")
                st.balloons()
                st.info("Redirecting to dashboard...")
                st.session_state.login_success = True
                st.rerun()
            else:
                st.error(f"❌ {result['error']}")

# Additional options
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Don't have an account?")
    if st.button("📝 Create Account", use_container_width=True):
        st.switch_page("pages/2_📝_Signup.py")

with col2:
    st.markdown("#### Forgot password?")
    if st.button("🔑 Reset Password", use_container_width=True):
        st.session_state.show_reset = True
        st.rerun()

# Password reset modal
if st.session_state.get('show_reset', False):
    st.markdown("---")
    st.markdown("### 🔑 Reset Your Password")
    st.markdown("Enter your email address and we'll send you a reset link.")

    reset_email = st.text_input(
        "Email Address",
        placeholder="your@email.com",
        key="reset_email"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📧 Send Reset Link", type="primary", use_container_width=True):
            if reset_email:
                result = auth.reset_password(reset_email)
                if result['success']:
                    st.success(f"✅ {result['message']}")
                    st.session_state.show_reset = False
                else:
                    st.error(f"❌ {result['error']}")
            else:
                st.error("Please enter your email address")

    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_reset = False
            st.rerun()

# Getting Started Info
st.markdown("---")
st.info("""
    **📌 First time using CreatorPulse?**

    1. Click **"Create Account"** to sign up
    2. Verify your email address
    3. Login with your credentials

    ✨ Your data is securely stored and accessible only to you!
""")

# Footer
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0; margin-top: 2rem;">
        <p style="font-size: 0.95rem;">🔐 Secured by Supabase Auth</p>
        <p style="font-size: 0.85rem; color: #475569;">CreatorPulse v2.0 Enhanced</p>
    </div>
""", unsafe_allow_html=True)
