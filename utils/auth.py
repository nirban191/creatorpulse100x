"""
Authentication module for CreatorPulse
Handles user signup, login, and session management with Supabase Auth
"""

import streamlit as st
from typing import Optional, Dict
from utils.supabase_client import get_db


class AuthManager:
    """Manage user authentication with Supabase"""

    def __init__(self):
        self.db = get_db()

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return 'authenticated' in st.session_state and st.session_state.authenticated

    def signup(self, email: str, password: str, full_name: str = "") -> Dict:
        """
        Sign up a new user

        Args:
            email: User's email
            password: User's password
            full_name: Optional full name

        Returns:
            dict with 'success' and 'message' or 'error'
        """
        if not self.db.is_configured():
            return {
                'success': False,
                'error': 'Database not configured. Please add Supabase credentials to .env'
            }

        try:
            # Sign up with Supabase Auth
            response = self.db.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            })

            if response.user:
                return {
                    'success': True,
                    'message': 'Signup successful! Please check your email to verify your account.',
                    'user': response.user
                }
            else:
                return {
                    'success': False,
                    'error': 'Signup failed. Please try again.'
                }

        except Exception as e:
            error_msg = str(e)
            if 'already registered' in error_msg.lower():
                return {
                    'success': False,
                    'error': 'This email is already registered. Please login instead.'
                }
            return {
                'success': False,
                'error': f'Signup error: {error_msg}'
            }

    def login(self, email: str, password: str) -> Dict:
        """
        Log in an existing user

        Args:
            email: User's email
            password: User's password

        Returns:
            dict with 'success' and user data or 'error'
        """
        if not self.db.is_configured():
            return {
                'success': False,
                'error': 'Database not configured. Please add Supabase credentials to .env'
            }

        try:
            # Sign in with Supabase Auth
            response = self.db.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.user:
                # Set session state
                st.session_state.authenticated = True
                st.session_state.user_id = response.user.id
                st.session_state.user_email = response.user.email
                st.session_state.user_data = response.user.user_metadata

                # Create or update profile in database
                self.db.get_or_create_profile(response.user.id, response.user.email)

                return {
                    'success': True,
                    'message': 'Login successful!',
                    'user': response.user
                }
            else:
                return {
                    'success': False,
                    'error': 'Login failed. Please check your credentials.'
                }

        except Exception as e:
            error_msg = str(e)
            if 'invalid login credentials' in error_msg.lower():
                return {
                    'success': False,
                    'error': 'Invalid email or password. Please try again.'
                }
            elif 'email not confirmed' in error_msg.lower():
                return {
                    'success': False,
                    'error': 'Please verify your email address before logging in.'
                }
            return {
                'success': False,
                'error': f'Login error: {error_msg}'
            }

    def logout(self):
        """Log out the current user"""
        try:
            if self.db.is_configured():
                self.db.client.auth.sign_out()

            # Clear session state
            for key in ['authenticated', 'user_id', 'user_email', 'user_data',
                       'sources', 'generated_drafts', 'user_feedback', 'style_trained']:
                if key in st.session_state:
                    del st.session_state[key]

            return {'success': True, 'message': 'Logged out successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_current_user(self) -> Optional[Dict]:
        """Get current user information"""
        if not self.is_authenticated():
            return None

        return {
            'id': st.session_state.get('user_id'),
            'email': st.session_state.get('user_email'),
            'data': st.session_state.get('user_data', {})
        }

    def reset_password(self, email: str) -> Dict:
        """
        Send password reset email

        Args:
            email: User's email address

        Returns:
            dict with 'success' and 'message' or 'error'
        """
        if not self.db.is_configured():
            return {
                'success': False,
                'error': 'Database not configured'
            }

        try:
            self.db.client.auth.reset_password_for_email(email)
            return {
                'success': True,
                'message': 'Password reset email sent! Please check your inbox.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error sending reset email: {str(e)}'
            }


def require_auth():
    """
    Decorator/check to require authentication
    Redirects to login page if not authenticated
    """
    auth = AuthManager()
    if not auth.is_authenticated():
        st.warning("⚠️ Please login to access this page")
        st.switch_page("pages/1_🔐_Login.py")
        st.stop()
