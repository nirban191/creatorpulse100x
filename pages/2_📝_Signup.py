"""
Signup Page for CreatorPulse
"""

import streamlit as st
import re
from utils.auth import AuthManager

# Page config
st.set_page_config(
    page_title="Sign Up - CreatorPulse",
    page_icon="📝",
    layout="centered"
)

# Initialize auth manager
auth = AuthManager()

# Custom CSS
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

    if st.button("Go to Dashboard", type="primary", use_container_width=True):
        st.switch_page("app_enhanced.py")
    st.stop()

# Header
st.markdown('<h1 class="main-header">CreatorPulse</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Create your account</p>', unsafe_allow_html=True)

# Helper functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

# Signup form
with st.form("signup_form"):
    st.markdown("### Account Information")

    full_name = st.text_input(
        "Full Name (Optional)",
        placeholder="John Doe",
        help="Your display name in the app"
    )

    email = st.text_input(
        "Email *",
        placeholder="your@email.com",
        help="Use a valid email address - you'll need to verify it"
    )

    col1, col2 = st.columns(2)
    with col1:
        password = st.text_input(
            "Password *",
            type="password",
            placeholder="Create a strong password",
            help="Minimum 8 characters with uppercase, lowercase, and numbers"
        )
    with col2:
        confirm_password = st.text_input(
            "Confirm Password *",
            type="password",
            placeholder="Re-enter your password"
        )

    # Password strength indicator
    if password:
        is_valid, msg = validate_password(password)
        if is_valid:
            st.success(f"✅ {msg}")
        else:
            st.warning(f"⚠️ {msg}")

    st.markdown("---")

    # Terms and conditions
    agree_terms = st.checkbox(
        "I agree to the Terms of Service and Privacy Policy",
        value=False
    )

    # Submit button
    submit = st.form_submit_button(
        "📝 Create Account",
        use_container_width=True,
        type="primary"
    )

# Handle signup submission
if submit:
    # Validation
    errors = []

    if not email:
        errors.append("Email is required")
    elif not validate_email(email):
        errors.append("Invalid email format")

    if not password:
        errors.append("Password is required")
    else:
        is_valid, msg = validate_password(password)
        if not is_valid:
            errors.append(msg)

    if password != confirm_password:
        errors.append("Passwords do not match")

    if not agree_terms:
        errors.append("You must agree to the Terms of Service")

    # Show errors or proceed
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        with st.spinner("Creating your account..."):
            result = auth.signup(email, password, full_name)

            if result['success']:
                st.success(f"✅ {result['message']}")
                st.balloons()

                st.info("""
                    **Next Steps:**
                    1. Check your email inbox for a verification link
                    2. Click the link to verify your account
                    3. Return here and login with your credentials

                    **Note:** You won't be able to login until you verify your email.
                """)

                st.markdown("---")
                if st.button("Go to Login Page", type="primary", use_container_width=True):
                    st.switch_page("pages/1_🔐_Login.py")
            else:
                st.error(f"❌ {result['error']}")

# Additional options
st.markdown("---")
st.markdown("### Already have an account?")

if st.button("🔐 Login", use_container_width=True):
    st.switch_page("pages/1_🔐_Login.py")

# Features section
st.markdown("---")
st.markdown("### Why Sign Up?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        **🎯 Personalized Experience**
        - Your own style training
        - Custom source connections
        - Private newsletter drafts
    """)

with col2:
    st.markdown("""
        **🔒 Secure & Private**
        - End-to-end encryption
        - Your data stays yours
        - No third-party sharing
    """)

st.markdown("""
    **⚡ Powered by:**
    - Supabase for secure authentication
    - Groq AI for fast generation
    - Resend for email delivery
""")

# Footer
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0; margin-top: 3rem;">
        <p>By signing up, you agree to our Terms of Service and Privacy Policy</p>
        <p style="font-size: 0.8rem;">CreatorPulse v2.0 with Authentication</p>
    </div>
""", unsafe_allow_html=True)
