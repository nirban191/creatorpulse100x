"""
Delivery Scheduler for CreatorPulse
Handles scheduled newsletter delivery with timezone support
"""

from datetime import datetime, time, timedelta
from typing import Dict, List, Optional, Any
import pytz
from enum import Enum


class DeliveryFrequency(Enum):
    """Newsletter delivery frequency options"""
    DAILY = "daily"
    WEEKDAYS = "weekdays"  # Monday-Friday
    WEEKLY = "weekly"  # Once per week
    CUSTOM = "custom"  # Custom days


class DeliveryScheduler:
    """Manages scheduled newsletter delivery"""

    def __init__(self, db=None):
        """
        Initialize delivery scheduler

        Args:
            db: Database client for storing schedules
        """
        self.db = db

    def create_schedule(
        self,
        user_id: str,
        delivery_time: time,
        timezone: str = "UTC",
        frequency: str = "daily",
        enabled: bool = True,
        recipient_emails: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new delivery schedule for a user

        Args:
            user_id: User identifier
            delivery_time: Time to send (local time)
            timezone: User's timezone (e.g., 'America/New_York')
            frequency: Delivery frequency ('daily', 'weekdays', 'weekly')
            enabled: Whether schedule is active
            recipient_emails: List of email addresses to send to

        Returns:
            Dictionary with schedule creation result
        """
        if not self.db or not self.db.is_configured():
            return {
                'success': False,
                'error': 'Database not configured'
            }

        try:
            # Validate timezone
            try:
                pytz.timezone(timezone)
            except pytz.exceptions.UnknownTimeZoneError:
                return {
                    'success': False,
                    'error': f'Invalid timezone: {timezone}'
                }

            # Update user profile with delivery preferences
            result = self.db.client.table('profiles').update({
                'auto_delivery_enabled': enabled,
                'delivery_time': delivery_time.isoformat(),
                'delivery_timezone': timezone,
                'delivery_frequency': frequency,
                'delivery_recipients': recipient_emails or []
            }).eq('id', user_id).execute()

            return {
                'success': True,
                'message': 'Delivery schedule created successfully',
                'data': result.data
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_schedule(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get delivery schedule for a user

        Args:
            user_id: User identifier

        Returns:
            Schedule dictionary or None
        """
        if not self.db or not self.db.is_configured():
            return None

        try:
            result = self.db.client.table('profiles')\
                .select('auto_delivery_enabled, delivery_time, delivery_timezone, '
                       'delivery_frequency, delivery_recipients')\
                .eq('id', user_id)\
                .single()\
                .execute()

            if result.data:
                return {
                    'enabled': result.data.get('auto_delivery_enabled', False),
                    'time': result.data.get('delivery_time'),
                    'timezone': result.data.get('delivery_timezone', 'UTC'),
                    'frequency': result.data.get('delivery_frequency', 'daily'),
                    'recipients': result.data.get('delivery_recipients', [])
                }

            return None

        except Exception:
            return None

    def disable_schedule(self, user_id: str) -> Dict[str, Any]:
        """
        Disable automatic delivery for a user

        Args:
            user_id: User identifier

        Returns:
            Result dictionary
        """
        if not self.db or not self.db.is_configured():
            return {'success': False, 'error': 'Database not configured'}

        try:
            self.db.client.table('profiles').update({
                'auto_delivery_enabled': False
            }).eq('id', user_id).execute()

            return {
                'success': True,
                'message': 'Automatic delivery disabled'
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_next_delivery_time(
        self,
        delivery_time: time,
        timezone_str: str,
        frequency: str = "daily"
    ) -> datetime:
        """
        Calculate next delivery time in user's timezone

        Args:
            delivery_time: Scheduled delivery time (local)
            timezone_str: User's timezone
            frequency: Delivery frequency

        Returns:
            Next delivery datetime (UTC)
        """
        # Get user's timezone
        user_tz = pytz.timezone(timezone_str)
        utc_tz = pytz.UTC

        # Get current time in user's timezone
        now_utc = datetime.now(utc_tz)
        now_local = now_utc.astimezone(user_tz)

        # Create next delivery datetime in user's timezone
        next_delivery_local = now_local.replace(
            hour=delivery_time.hour,
            minute=delivery_time.minute,
            second=0,
            microsecond=0
        )

        # If scheduled time has passed today, move to tomorrow
        if next_delivery_local <= now_local:
            next_delivery_local += timedelta(days=1)

        # Handle different frequencies
        if frequency == "weekdays":
            # If next day is weekend, move to Monday
            while next_delivery_local.weekday() >= 5:  # 5=Saturday, 6=Sunday
                next_delivery_local += timedelta(days=1)

        elif frequency == "weekly":
            # Always send on the same day of week
            # If already past this week's day, move to next week
            pass  # Handled by the +1 day logic above

        # Convert to UTC
        next_delivery_utc = next_delivery_local.astimezone(utc_tz)

        return next_delivery_utc

    def should_send_today(
        self,
        frequency: str,
        last_sent: Optional[datetime] = None
    ) -> bool:
        """
        Check if newsletter should be sent today based on frequency

        Args:
            frequency: Delivery frequency
            last_sent: Last time newsletter was sent

        Returns:
            True if should send today
        """
        today = datetime.now()

        if frequency == "daily":
            return True

        elif frequency == "weekdays":
            # Monday = 0, Sunday = 6
            return today.weekday() < 5  # Monday-Friday

        elif frequency == "weekly":
            # Send once per week
            if not last_sent:
                return True
            days_since_last = (today - last_sent).days
            return days_since_last >= 7

        return False

    @staticmethod
    def get_available_timezones() -> List[str]:
        """
        Get list of common timezones for user selection

        Returns:
            List of timezone names
        """
        # Common timezones for better UX
        common_timezones = [
            "UTC",
            "America/New_York",      # EST/EDT
            "America/Chicago",        # CST/CDT
            "America/Denver",         # MST/MDT
            "America/Los_Angeles",    # PST/PDT
            "America/Toronto",        # Canada Eastern
            "America/Vancouver",      # Canada Pacific
            "Europe/London",          # GMT/BST
            "Europe/Paris",           # CET/CEST
            "Europe/Berlin",          # CET/CEST
            "Asia/Tokyo",             # JST
            "Asia/Shanghai",          # CST
            "Asia/Kolkata",           # IST
            "Asia/Dubai",             # GST
            "Australia/Sydney",       # AEST/AEDT
            "Pacific/Auckland",       # NZST/NZDT
        ]

        return common_timezones

    @staticmethod
    def format_time_with_timezone(dt: datetime, timezone_str: str) -> str:
        """
        Format datetime with timezone information

        Args:
            dt: Datetime to format
            timezone_str: Timezone name

        Returns:
            Formatted string
        """
        tz = pytz.timezone(timezone_str)
        local_time = dt.astimezone(tz)
        return local_time.strftime("%Y-%m-%d %I:%M %p %Z")


def schedule_newsletter_delivery(
    user_id: str,
    delivery_time: time,
    timezone: str,
    frequency: str,
    recipient_emails: List[str],
    db
) -> Dict[str, Any]:
    """
    Convenience function to schedule newsletter delivery

    Args:
        user_id: User identifier
        delivery_time: Time to deliver (local)
        timezone: User's timezone
        frequency: How often to send
        recipient_emails: Email addresses
        db: Database client

    Returns:
        Schedule creation result
    """
    scheduler = DeliveryScheduler(db)
    return scheduler.create_schedule(
        user_id=user_id,
        delivery_time=delivery_time,
        timezone=timezone,
        frequency=frequency,
        enabled=True,
        recipient_emails=recipient_emails
    )


def get_user_schedule(user_id: str, db) -> Optional[Dict]:
    """
    Get user's delivery schedule

    Args:
        user_id: User identifier
        db: Database client

    Returns:
        Schedule dictionary or None
    """
    scheduler = DeliveryScheduler(db)
    return scheduler.get_schedule(user_id)
