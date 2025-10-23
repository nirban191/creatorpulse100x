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

# Modern Custom CSS (matching login page)
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

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Center Container */
    .block-container {
        max-width: 600px;
        padding-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Check if already authenticated
if auth.is_authenticated():
    st.markdown('<h1 class="main-header">✅ Welcome!</h1>', unsafe_allow_html=True)
    user = auth.get_current_user()
    st.success(f"You are already logged in as **{user['email']}**")

    if st.button("🏠 Go to Dashboard", type="primary", use_container_width=True):
        st.switch_page("app_enhanced.py")
    st.stop()

# Header
st.markdown('<h1 class="main-header">📝 CreatorPulse</h1>', unsafe_allow_html=True)
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
        "Email Address *",
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

    st.markdown("")

    # Terms and conditions
    agree_terms = st.checkbox(
        "I agree to the Terms of Service and Privacy Policy",
        value=False
    )

    st.markdown("")

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
                    **✨ Next Steps:**

                    1. Check your email inbox for a verification link
                    2. Click the link to verify your account
                    3. Return here and login with your credentials

                    **Note:** You won't be able to login until you verify your email.
                """)

                st.markdown("---")
                if st.button("🔐 Go to Login Page", type="primary", use_container_width=True):
                    st.switch_page("pages/1_🔐_Login.py")
            else:
                st.error(f"❌ {result['error']}")

# Additional options
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### Already have an account?")

with col2:
    if st.button("🔐 Sign In", use_container_width=True):
        st.switch_page("pages/1_🔐_Login.py")

# Features section
st.markdown("---")
st.markdown("### ✨ Why Join CreatorPulse?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        **🎯 Personalized Experience**
        - Train your unique writing style
        - Connect your favorite sources
        - Generate custom newsletters
        - Schedule automatic delivery
    """)

with col2:
    st.markdown("""
        **🔒 Secure & Private**
        - End-to-end encryption
        - Your data stays yours
        - No third-party sharing
        - Supabase-powered auth
    """)

st.info("""
**⚡ Powered by cutting-edge tech:**

🤖 **Groq AI** - Lightning-fast AI generation
🗄️ **Supabase** - Secure database & authentication
📧 **Resend** - Reliable email delivery
""")

# Footer
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0; margin-top: 2rem;">
        <p style="font-size: 0.9rem;">By signing up, you agree to our Terms of Service and Privacy Policy</p>
        <p style="font-size: 0.85rem; color: #475569;">CreatorPulse v2.0 Enhanced</p>
    </div>
""", unsafe_allow_html=True)
