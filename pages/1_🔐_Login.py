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

# Custom CSS for login page
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Check if already authenticated
if auth.is_authenticated():
    st.success("✅ You are already logged in!")
    user = auth.get_current_user()
    st.info(f"Logged in as: **{user['email']}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Dashboard", type="primary", use_container_width=True):
            st.switch_page("app_enhanced.py")
    with col2:
        if st.button("Logout", use_container_width=True):
            auth.logout()
            st.rerun()
    st.stop()

# Header
st.markdown('<h1 class="main-header">CreatorPulse</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sign in to your account</p>', unsafe_allow_html=True)

# Login form
with st.form("login_form"):
    email = st.text_input(
        "Email",
        placeholder="your@email.com",
        help="Enter your registered email address"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        help="Your account password"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        submit = st.form_submit_button("🔐 Login", use_container_width=True, type="primary")
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
    st.markdown("##### Don't have an account?")
    if st.button("📝 Sign Up", use_container_width=True):
        st.switch_page("pages/2_📝_Signup.py")

with col2:
    st.markdown("##### Forgot password?")
    if st.button("🔑 Reset Password", use_container_width=True):
        st.session_state.show_reset = True
        st.rerun()

# Password reset modal
if st.session_state.get('show_reset', False):
    st.markdown("---")
    st.markdown("### Reset Password")

    reset_email = st.text_input(
        "Enter your email address",
        placeholder="your@email.com",
        key="reset_email"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Send Reset Link", type="primary", use_container_width=True):
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
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_reset = False
            st.rerun()

# Demo mode notice
st.markdown("---")
st.info("""
    **📌 First time using CreatorPulse?**

    1. Click "Sign Up" to create a new account
    2. Verify your email address
    3. Login with your credentials

    Your data will be securely stored and accessible only to you!
""")

# Footer
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0; margin-top: 3rem;">
        <p>Powered by Supabase Auth + Groq AI + Resend</p>
        <p style="font-size: 0.8rem;">CreatorPulse v2.0 with Authentication</p>
    </div>
""", unsafe_allow_html=True)
