#!/usr/bin/env python3
"""
Scheduled Newsletter Delivery Script
Run this hourly via cron service to send scheduled newsletters
"""

import os
import sys
from datetime import datetime, time as datetime_time
import pytz

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.supabase_client import get_db
from utils.llm_generator import NewsletterGenerator
from utils.email_sender import NewsletterEmailSender
from utils.delivery_scheduler import DeliveryScheduler
from utils.trend_detector import TrendDetector


def main():
    """Check for users due for delivery and send newsletters"""

    print(f"[{datetime.now()}] Starting scheduled delivery check...")

    # Initialize clients
    db = get_db()
    if not db.is_configured():
        print("ERROR: Database not configured. Check SUPABASE_URL and SUPABASE_KEY")
        return 1

    scheduler = DeliveryScheduler(db)
    email_sender = NewsletterEmailSender()

    # Check if email is configured
    if not os.getenv('RESEND_API_KEY'):
        print("WARNING: RESEND_API_KEY not configured. Emails cannot be sent.")

    # Get users who have automatic delivery enabled
    try:
        result = db.client.rpc('get_users_due_for_delivery').execute()
        users = result.data if result.data else []
    except Exception as e:
        print(f"ERROR fetching users: {e}")
        return 1

    print(f"Found {len(users)} users with automatic delivery enabled")

    if len(users) == 0:
        print("No users to process. Exiting.")
        return 0

    # Check each user
    now_utc = datetime.now(pytz.UTC)
    newsletters_sent = 0

    for user in users:
        try:
            user_id = user['user_id']
            delivery_time_str = user['delivery_time']
            timezone_str = user['delivery_timezone']
            frequency = user['delivery_frequency']
            recipients = user.get('delivery_recipients', [])
            last_delivery = user.get('last_delivery_at')

            print(f"\n--- Processing user {user_id} ---")
            print(f"  Time: {delivery_time_str} {timezone_str}")
            print(f"  Frequency: {frequency}")
            print(f"  Recipients: {len(recipients)}")

            # Parse delivery time
            try:
                hour, minute, second = map(int, delivery_time_str.split(':'))
                delivery_time = datetime_time(hour, minute, second)
            except:
                print(f"  ERROR: Invalid delivery time format: {delivery_time_str}")
                continue

            # Convert last delivery to datetime if exists
            if last_delivery:
                try:
                    last_delivery = datetime.fromisoformat(last_delivery.replace('Z', '+00:00'))
                except:
                    last_delivery = None

            # Check if should send today based on frequency
            if not scheduler.should_send_today(frequency, last_delivery):
                print(f"  SKIP: Not scheduled for today ({frequency})")
                continue

            # Calculate next delivery time
            next_delivery = scheduler.get_next_delivery_time(
                delivery_time, timezone_str, frequency
            )

            # Check if it's time to send (within 1 hour window)
            time_diff = abs((next_delivery - now_utc).total_seconds())
            hours_until = time_diff / 3600

            print(f"  Next delivery: {next_delivery}")
            print(f"  Time until delivery: {hours_until:.2f} hours")

            if time_diff < 3600:  # Within 1 hour
                print(f"  ✓ TIME TO SEND!")

                if not recipients:
                    print(f"  ERROR: No recipients configured")
                    continue

                # Generate newsletter
                print(f"  Generating newsletter...")

                try:
                    # Get sources
                    sources = db.get_sources(user_id)

                    # Create aggregated content
                    aggregated_content = []
                    for source in sources:
                        aggregated_content.append({
                            'title': f"Latest from {source['identifier']}",
                            'content': f"Content from {source['source_type']} source: {source['identifier']}",
                            'source_type': source['source_type'],
                            'identifier': source['identifier']
                        })

                    if not aggregated_content:
                        print(f"  WARNING: No content sources found")
                        aggregated_content = [{
                            'title': 'Your Daily Newsletter',
                            'content': 'Stay tuned for curated content from your sources!'
                        }]

                    # Get style profile
                    style_data = db.get_style_training(user_id)
                    style_profile = None
                    if style_data:
                        style_profile = {'training_text': style_data[0].get('training_text', '')}

                    # Detect trends
                    trend_detector = TrendDetector(db)
                    trending_data = trend_detector.get_trending_topics(
                        aggregated_content,
                        include_spikes=True,
                        top_n=5
                    )

                    # Generate newsletter using Groq
                    generator = NewsletterGenerator(provider='groq', model='llama-3.3-70b-versatile')
                    content = generator.generate_newsletter(
                        content_items=aggregated_content,
                        title=f"Your Morning Digest - {datetime.now().strftime('%B %d, %Y')}",
                        style_profile=style_profile,
                        num_articles=5,
                        include_trends=True
                    )

                    # Prepend trending topics
                    if trending_data and trending_data.get('trending_keywords'):
                        trends_section = trend_detector.format_trends_for_newsletter(trending_data, max_trends=5)
                        content = trends_section + "\n\n" + content

                    print(f"  Newsletter generated ({len(content)} chars)")

                    # Send email
                    print(f"  Sending to {len(recipients)} recipients...")
                    result = email_sender.send_newsletter(
                        to_emails=recipients,
                        subject=f"Your Morning Newsletter - {datetime.now().strftime('%B %d')}",
                        content=content,
                        from_email="CreatorPulse <newsletter@resend.dev>"
                    )

                    if result['success']:
                        print(f"  ✅ Newsletter sent successfully!")
                        newsletters_sent += 1

                        # Update last delivery time
                        try:
                            db.client.rpc('update_last_delivery', {'p_user_id': user_id}).execute()
                            print(f"  Updated last_delivery_at timestamp")
                        except Exception as e:
                            print(f"  WARNING: Could not update timestamp: {e}")
                    else:
                        print(f"  ❌ Failed to send: {result.get('error')}")

                except Exception as e:
                    print(f"  ❌ Error generating/sending newsletter: {e}")
                    import traceback
                    traceback.print_exc()

            else:
                print(f"  ⏳ Not yet time (next delivery in {hours_until:.1f} hours)")

        except Exception as e:
            print(f"  ERROR processing user {user.get('user_id', 'unknown')}: {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\n{'='*60}")
    print(f"Delivery check complete")
    print(f"Newsletters sent: {newsletters_sent}")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
