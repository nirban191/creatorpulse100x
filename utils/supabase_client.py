"""
Supabase Client for CreatorPulse
Handles all database operations with Supabase
"""

import os
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CreatorPulseDB:
    """Database client for CreatorPulse with Supabase"""

    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.client: Optional[Client] = None

        if self.url and self.key:
            try:
                # Try creating client without options (for newer supabase versions)
                self.client = create_client(self.url, self.key)
            except TypeError:
                # Fallback for older versions or when options are needed
                try:
                    from supabase import ClientOptions
                    options = ClientOptions()
                    self.client = create_client(self.url, self.key, options=options)
                except Exception:
                    # If all else fails, try basic initialization
                    self.client = create_client(self.url, self.key)

    def is_configured(self) -> bool:
        """Check if Supabase is configured"""
        return self.client is not None

    # ===== SOURCES OPERATIONS =====

    def add_source(self, user_id: str, source_type: str, identifier: str) -> Dict:
        """Add a new content source"""
        if not self.client:
            return {'error': 'Database not configured'}

        try:
            response = self.client.table('sources').insert({
                'user_id': user_id,
                'source_type': source_type,
                'identifier': identifier,
                'is_active': True
            }).execute()

            return {'success': True, 'data': response.data}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_sources(self, user_id: str, source_type: Optional[str] = None) -> List[Dict]:
        """Get all sources for a user"""
        if not self.client:
            return []

        try:
            query = self.client.table('sources').select('*').eq('user_id', user_id)

            if source_type:
                query = query.eq('source_type', source_type)

            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error fetching sources: {e}")
            return []

    def delete_source(self, user_id: str, source_id: str) -> bool:
        """Delete a source"""
        if not self.client:
            return False

        try:
            self.client.table('sources').delete().eq('id', source_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting source: {e}")
            return False

    # ===== DRAFTS OPERATIONS =====

    def save_draft(self, user_id: str, title: str, content: str, llm_provider: str, generation_time_ms: int = 0) -> Dict:
        """Save a newsletter draft"""
        if not self.client:
            return {'error': 'Database not configured'}

        try:
            response = self.client.table('drafts').insert({
                'user_id': user_id,
                'title': title,
                'content': content,
                'llm_provider': llm_provider,
                'generation_time_ms': generation_time_ms,
                'status': 'draft'
            }).execute()

            return {'success': True, 'data': response.data}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_drafts(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent drafts for a user"""
        if not self.client:
            return []

        try:
            response = self.client.table('drafts').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching drafts: {e}")
            return []

    def update_draft_status(self, user_id: str, draft_id: str, status: str, sent_at: Optional[str] = None, recipient_count: int = 0) -> bool:
        """Update draft status (e.g., when sent)"""
        if not self.client:
            return False

        try:
            update_data = {'status': status}
            if sent_at:
                update_data['sent_at'] = sent_at
            if recipient_count:
                update_data['recipient_count'] = recipient_count

            self.client.table('drafts').update(update_data).eq('id', draft_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating draft: {e}")
            return False

    # ===== FEEDBACK OPERATIONS =====

    def add_feedback(self, user_id: str, draft_id: str, feedback_type: str, notes: Optional[str] = None) -> bool:
        """Add feedback for a draft"""
        if not self.client:
            return False

        try:
            self.client.table('feedback').insert({
                'user_id': user_id,
                'draft_id': draft_id,
                'feedback_type': feedback_type,
                'notes': notes
            }).execute()
            return True
        except Exception as e:
            print(f"Error adding feedback: {e}")
            return False

    def get_feedback_stats(self, user_id: str) -> Dict:
        """Get feedback statistics"""
        if not self.client:
            return {}

        try:
            response = self.client.table('feedback').select('feedback_type').eq('user_id', user_id).execute()

            feedback_data = response.data
            total = len(feedback_data)
            positive = len([f for f in feedback_data if f['feedback_type'] == 'positive'])

            acceptance_rate = (positive / total * 100) if total > 0 else 0

            return {
                'total': total,
                'positive': positive,
                'negative': total - positive,
                'acceptance_rate': round(acceptance_rate, 1)
            }
        except Exception as e:
            print(f"Error fetching feedback stats: {e}")
            return {}

    # ===== STYLE TRAINING OPERATIONS =====

    def save_style_training(self, user_id: str, training_text: str, analysis_result: Optional[Dict] = None) -> Dict:
        """Save style training data"""
        if not self.client:
            return {'success': False, 'error': 'Database not configured'}

        try:
            self.client.table('style_training').insert({
                'user_id': user_id,
                'training_text': training_text,
                'analysis_result': analysis_result,
                'is_active': True
            }).execute()
            return {'success': True}
        except Exception as e:
            error_msg = str(e)
            print(f"Error saving style training: {error_msg}")
            return {'success': False, 'error': error_msg}

    def get_style_training(self, user_id: str) -> List[Dict]:
        """Get active style training data"""
        if not self.client:
            return []

        try:
            response = self.client.table('style_training').select('*').eq('user_id', user_id).eq('is_active', True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching style training: {e}")
            return []

    # ===== EMAIL SENDS OPERATIONS =====

    def log_email_send(self, user_id: str, draft_id: Optional[str], recipient_emails: List[str], subject: str, resend_email_id: Optional[str] = None) -> bool:
        """Log an email send"""
        if not self.client:
            return False

        try:
            self.client.table('email_sends').insert({
                'user_id': user_id,
                'draft_id': draft_id,
                'recipient_emails': recipient_emails,
                'subject': subject,
                'send_status': 'sent' if resend_email_id else 'failed',
                'resend_email_id': resend_email_id
            }).execute()
            return True
        except Exception as e:
            print(f"Error logging email send: {e}")
            return False

    # ===== ANALYTICS OPERATIONS =====

    def log_event(self, user_id: str, event_type: str, event_data: Optional[Dict] = None) -> bool:
        """Log an analytics event"""
        if not self.client:
            return False

        try:
            self.client.table('analytics').insert({
                'user_id': user_id,
                'event_type': event_type,
                'event_data': event_data
            }).execute()
            return True
        except Exception as e:
            print(f"Error logging event: {e}")
            return False

    # ===== USER STATS =====

    def get_user_stats(self, user_id: str) -> Dict:
        """Get comprehensive user statistics"""
        if not self.client:
            return {}

        try:
            # Get from pre-computed view
            response = self.client.from_('user_stats').select('*').eq('user_id', user_id).execute()

            if response.data:
                return response.data[0]
            else:
                return {
                    'total_sources': 0,
                    'total_drafts': 0,
                    'positive_feedback': 0,
                    'total_feedback': 0,
                    'acceptance_rate': 0,
                    'estimated_hours_saved': 0
                }
        except Exception as e:
            print(f"Error fetching user stats: {e}")
            return {}

    # ===== PROFILE OPERATIONS =====

    def get_or_create_profile(self, user_id: str, email: str) -> Dict:
        """Get or create user profile"""
        if not self.client:
            return {}

        try:
            # Try to get existing profile
            response = self.client.table('profiles').select('*').eq('id', user_id).execute()

            if response.data:
                return response.data[0]
            else:
                # Create new profile
                response = self.client.table('profiles').insert({
                    'id': user_id,
                    'email': email
                }).execute()
                return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error with profile: {e}")
            return {}

    def update_preferred_llm(self, user_id: str, llm_provider: str) -> bool:
        """Update user's preferred LLM provider"""
        if not self.client:
            return False

        try:
            self.client.table('profiles').update({
                'preferred_llm_provider': llm_provider
            }).eq('id', user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating LLM preference: {e}")
            return False


# Singleton instance
_db_instance = None

def get_db() -> CreatorPulseDB:
    """Get database instance (singleton pattern)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = CreatorPulseDB()
    return _db_instance
