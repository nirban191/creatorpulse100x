"""
Scheduler Module for CreatorPulse
Handles automated daily trend discovery jobs using APScheduler
"""

import os
from datetime import datetime, time as dt_time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import atexit

from utils.trends_discovery import TrendsDiscovery
from utils.supabase_client import CreatorPulseDB


# Global scheduler instance
_scheduler = None


def daily_trend_discovery_job():
    """
    Main job function that runs daily to discover trends
    This function is executed by APScheduler
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting daily trend discovery job at {datetime.now()}")
    print(f"{'='*60}\n")

    db = CreatorPulseDB()
    if not db.is_configured():
        print("❌ Database not configured. Skipping trend discovery.")
        return

    trends_engine = TrendsDiscovery()
    if not trends_engine.pytrends:
        print("❌ Google Trends not initialized. Skipping trend discovery.")
        return

    try:
        # Get all users with enabled trend discovery
        users = db.get_users_with_trend_discovery_enabled()

        if not users:
            print("ℹ️ No users have trend discovery enabled. Skipping.")
            return

        print(f"📊 Found {len(users)} user(s) with trend discovery enabled")

        # Process each user
        for user in users:
            user_id = user['user_id']
            categories = user.get('categories', ['tech', 'ai', 'business'])
            custom_keywords = user.get('custom_keywords', [])

            print(f"\n👤 Processing user: {user_id[:8]}...")
            print(f"   Categories: {', '.join(categories)}")
            if custom_keywords:
                print(f"   Custom keywords: {', '.join(custom_keywords)}")

            # Discover trends for user's categories
            discovered_trends = trends_engine.discover_trends_for_categories(
                categories=categories,
                max_per_category=3  # Keep it reasonable to avoid rate limits
            )

            # Save discovered trends to database
            saved_count = 0
            for trend in discovered_trends:
                result = db.save_trending_content(
                    user_id=user_id,
                    source_type=trend.get('source_type', 'google_trends'),
                    title=trend['title'],
                    description=trend.get('description', ''),
                    keywords=trend.get('keywords', []),
                    url=trend.get('url', ''),
                    metadata=trend.get('metadata', {}),
                    search_volume=trend.get('metadata', {}).get('rank', 0),
                    category=trend.get('category', 'all')
                )

                if result.get('success'):
                    saved_count += 1

            print(f"   ✅ Saved {saved_count}/{len(discovered_trends)} trends to database")

            # Update last run timestamp
            db.update_trend_settings_last_run(user_id)

        print(f"\n{'='*60}")
        print(f"✨ Daily trend discovery job completed successfully!")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ Error in daily trend discovery job: {e}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()


def job_listener(event):
    """Listen to job execution events for logging"""
    if event.exception:
        print(f"❌ Job {event.job_id} failed with exception: {event.exception}")
    else:
        print(f"✅ Job {event.job_id} executed successfully")


def init_scheduler(test_mode: bool = False):
    """
    Initialize the APScheduler for automated trend discovery

    Args:
        test_mode: If True, runs job immediately for testing
    """
    global _scheduler

    # Prevent multiple initializations
    if _scheduler is not None:
        print("ℹ️ Scheduler already initialized")
        return _scheduler

    print("\n🔧 Initializing APScheduler for trend discovery...")

    # Create scheduler
    _scheduler = BackgroundScheduler(
        timezone='America/New_York',  # Adjust to your timezone
        job_defaults={
            'coalesce': True,  # Combine multiple pending executions
            'max_instances': 1,  # Only one instance of job at a time
            'misfire_grace_time': 3600  # Allow 1 hour grace period for misfires
        }
    )

    # Add event listeners
    _scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    if test_mode:
        # For testing: run immediately
        print("🧪 Test mode: Running job immediately...")
        _scheduler.add_job(
            daily_trend_discovery_job,
            'date',
            run_date=datetime.now(),
            id='test_trend_discovery',
            name='Test Trend Discovery Job'
        )
    else:
        # Schedule daily job at 9 AM
        print("📅 Scheduling daily trend discovery job for 9:00 AM")
        _scheduler.add_job(
            daily_trend_discovery_job,
            CronTrigger(hour=9, minute=0),
            id='daily_trend_discovery',
            name='Daily Trend Discovery Job',
            replace_existing=True
        )

    # Start the scheduler
    _scheduler.start()
    print("✅ Scheduler started successfully!")

    # Register shutdown hook
    atexit.register(lambda: shutdown_scheduler())

    return _scheduler


def shutdown_scheduler():
    """Gracefully shutdown the scheduler"""
    global _scheduler

    if _scheduler is not None:
        print("\n🛑 Shutting down scheduler...")
        _scheduler.shutdown(wait=False)
        _scheduler = None
        print("✅ Scheduler shut down successfully")


def get_scheduler():
    """Get the current scheduler instance"""
    return _scheduler


def is_scheduler_running():
    """Check if scheduler is currently running"""
    return _scheduler is not None and _scheduler.running


def get_scheduled_jobs():
    """Get list of scheduled jobs"""
    if _scheduler is None:
        return []

    jobs = []
    for job in _scheduler.get_jobs():
        jobs.append({
            'id': job.id,
            'name': job.name,
            'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
            'trigger': str(job.trigger)
        })
    return jobs


def trigger_job_manually():
    """
    Manually trigger the trend discovery job
    Useful for testing or on-demand execution
    """
    print("\n🎯 Manually triggering trend discovery job...")
    try:
        daily_trend_discovery_job()
        return {'success': True, 'message': 'Job executed successfully'}
    except Exception as e:
        error_msg = f"Error executing job: {str(e)}"
        print(f"❌ {error_msg}")
        return {'success': False, 'error': error_msg}


def reschedule_job(hour: int = 9, minute: int = 0):
    """
    Reschedule the daily job to a different time

    Args:
        hour: Hour of day (0-23)
        minute: Minute of hour (0-59)
    """
    global _scheduler

    if _scheduler is None:
        print("❌ Scheduler not initialized")
        return False

    try:
        # Remove existing job
        if _scheduler.get_job('daily_trend_discovery'):
            _scheduler.remove_job('daily_trend_discovery')

        # Add new job with updated schedule
        _scheduler.add_job(
            daily_trend_discovery_job,
            CronTrigger(hour=hour, minute=minute),
            id='daily_trend_discovery',
            name='Daily Trend Discovery Job',
            replace_existing=True
        )

        print(f"✅ Job rescheduled to run daily at {hour:02d}:{minute:02d}")
        return True

    except Exception as e:
        print(f"❌ Error rescheduling job: {e}")
        return False
