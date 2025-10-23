# 📧 Morning Delivery Feature - Implementation Guide

## 🎯 Overview

The Morning Delivery feature allows users to schedule automatic newsletter delivery at a specific time each day (e.g., 08:00 AM local time).

---

## ✅ What's Been Implemented

### 1. Scheduler Module
**File**: [utils/delivery_scheduler.py](../utils/delivery_scheduler.py)

**Features**:
- ✅ Timezone-aware scheduling
- ✅ Multiple delivery frequencies (daily, weekdays, weekly)
- ✅ Next delivery time calculation
- ✅ Database integration for storing schedules
- ✅ 16 common timezones supported

### 2. Database Schema
**File**: [database/add_delivery_schedule.sql](../database/add_delivery_schedule.sql)

**Tables Added**:
- `profiles` - Added delivery preference columns:
  - `auto_delivery_enabled` - Enable/disable automatic delivery
  - `delivery_time` - Time to send (local time)
  - `delivery_timezone` - User's timezone
  - `delivery_frequency` - How often (daily/weekdays/weekly)
  - `delivery_recipients` - Email addresses
  - `last_delivery_at` - Last delivery timestamp

- `scheduled_newsletters` - Track pending deliveries:
  - Schedule tracking
  - Status management (pending/sending/sent/failed)
  - Error logging

**Functions Added**:
- `get_users_due_for_delivery()` - Find users needing newsletters
- `update_last_delivery()` - Update delivery timestamp
- `cleanup_old_scheduled_newsletters()` - Remove old data

---

## 🚀 How to Enable Morning Delivery

### Step 1: Run Database Migration

1. Go to Supabase Dashboard
2. Navigate to SQL Editor
3. Run: [database/add_delivery_schedule.sql](../database/add_delivery_schedule.sql)
4. Verify all columns and tables created

### Step 2: Add UI to App (Implementation Required)

Add this to `app_enhanced.py` in the Dashboard or Settings section:

```python
from utils.delivery_scheduler import DeliveryScheduler
from datetime import time

# In Dashboard or new Settings page
st.markdown("## ⏰ Morning Delivery Settings")

# Get current schedule
scheduler = DeliveryScheduler(db)
current_schedule = scheduler.get_schedule(st.session_state.user_id)

# Enable/Disable toggle
delivery_enabled = st.toggle(
    "Enable automatic morning delivery",
    value=current_schedule.get('enabled', False) if current_schedule else False
)

if delivery_enabled:
    col1, col2 = st.columns(2)

    with col1:
        # Time picker
        delivery_time = st.time_input(
            "Delivery time (your local time)",
            value=time(8, 0),  # Default 08:00 AM
            help="Newsletter will be generated and sent at this time"
        )

        # Timezone selector
        timezones = DeliveryScheduler.get_available_timezones()
        delivery_timezone = st.selectbox(
            "Your timezone",
            options=timezones,
            index=timezones.index(current_schedule['timezone']) if current_schedule else 0
        )

    with col2:
        # Frequency selector
        delivery_frequency = st.selectbox(
            "Delivery frequency",
            options=["daily", "weekdays", "weekly"],
            format_func=lambda x: {
                "daily": "📅 Every Day",
                "weekdays": "💼 Weekdays Only (Mon-Fri)",
                "weekly": "📆 Once Per Week"
            }[x]
        )

        # Recipient emails
        recipient_emails = st.text_area(
            "Recipient emails (one per line)",
            value="\n".join(current_schedule['recipients']) if current_schedule else st.session_state.user_email,
            help="Enter email addresses to send to"
        )

    # Save button
    if st.button("💾 Save Delivery Schedule", type="primary"):
        # Parse emails
        emails = [email.strip() for email in recipient_emails.split("\n") if email.strip()]

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
        if st.button("🛑 Disable Automatic Delivery"):
            result = scheduler.disable_schedule(st.session_state.user_id)
            if result['success']:
                st.success("✅ Automatic delivery disabled")
                st.rerun()
```

### Step 3: Implement Background Worker

**Option A: External Cron Service (Easiest)**

Use a free cron service to hit your API endpoint every hour:

1. Create API endpoint in app (or separate script)
2. Sign up for https://cron-job.org
3. Add job: Every hour, hit `https://your-hf-space.hf.space/api/check-deliveries`

**Option B: GitHub Actions (Recommended)**

Create `.github/workflows/scheduled-delivery.yml`:

```yaml
name: Morning Newsletter Delivery

on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:  # Manual trigger

jobs:
  check-deliveries:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install supabase groq resend python-dotenv

      - name: Check and send scheduled newsletters
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
        run: python scripts/send_scheduled_newsletters.py
```

**Option C: Separate Worker Service**

Deploy a background worker on:
- Railway (free tier)
- Render (free tier)
- Heroku (paid)

### Step 4: Create Delivery Script

Create `scripts/send_scheduled_newsletters.py`:

```python
#!/usr/bin/env python3
"""
Scheduled Newsletter Delivery Script
Run this hourly via cron/GitHub Actions to send scheduled newsletters
"""

import os
from datetime import datetime, time
import pytz
from dotenv import load_dotenv

# Import your modules
from utils.supabase_client import get_db
from utils.llm_generator import NewsletterGenerator
from utils.email_sender import NewsletterEmailSender
from utils.delivery_scheduler import DeliveryScheduler

load_dotenv()

def main():
    """Check for users due for delivery and send newsletters"""

    # Initialize clients
    db = get_db()
    if not db.is_configured():
        print("Error: Database not configured")
        return

    scheduler = DeliveryScheduler(db)
    email_sender = NewsletterEmailSender()

    # Get users who have automatic delivery enabled
    try:
        result = db.client.rpc('get_users_due_for_delivery').execute()
        users = result.data
    except Exception as e:
        print(f"Error fetching users: {e}")
        return

    print(f"Found {len(users)} users with automatic delivery enabled")

    # Check each user
    now_utc = datetime.now(pytz.UTC)

    for user in users:
        try:
            user_id = user['user_id']
            delivery_time = datetime.strptime(user['delivery_time'], '%H:%M:%S').time()
            timezone_str = user['delivery_timezone']
            frequency = user['delivery_frequency']
            recipients = user['delivery_recipients']
            last_delivery = user['last_delivery_at']

            # Convert last delivery to datetime
            if last_delivery:
                last_delivery = datetime.fromisoformat(last_delivery.replace('Z', '+00:00'))

            # Check if should send today based on frequency
            if not scheduler.should_send_today(frequency, last_delivery):
                print(f"Skipping user {user_id}: Not scheduled for today ({frequency})")
                continue

            # Calculate next delivery time
            next_delivery = scheduler.get_next_delivery_time(
                delivery_time, timezone_str, frequency
            )

            # Check if it's time to send (within 1 hour window)
            time_diff = abs((next_delivery - now_utc).total_seconds())

            if time_diff < 3600:  # Within 1 hour
                print(f"Sending newsletter to user {user_id}")

                # Generate newsletter
                sources = db.get_sources(user_id)

                # Create aggregated content
                aggregated_content = []
                for source in sources:
                    aggregated_content.append({
                        'title': f"Latest from {source['identifier']}",
                        'source_type': source['source_type'],
                        'identifier': source['identifier']
                    })

                # Get style profile
                style_data = db.get_style_training(user_id)
                style_profile = None
                if style_data:
                    style_profile = {'training_text': style_data[0].get('training_text', '')}

                # Generate newsletter
                generator = NewsletterGenerator(provider='groq')
                content = generator.generate_newsletter(
                    content_items=aggregated_content,
                    title=f"Your Daily Digest - {datetime.now().strftime('%B %d, %Y')}",
                    style_profile=style_profile,
                    num_articles=5,
                    include_trends=True
                )

                # Send email
                result = email_sender.send_newsletter(
                    to_emails=recipients,
                    subject=f"Your Daily Newsletter - {datetime.now().strftime('%B %d')}",
                    content=content,
                    from_email="CreatorPulse <newsletter@resend.dev>"
                )

                if result['success']:
                    print(f"✅ Newsletter sent to user {user_id}")
                    # Update last delivery time
                    db.client.rpc('update_last_delivery', {'p_user_id': user_id}).execute()
                else:
                    print(f"❌ Failed to send to user {user_id}: {result.get('error')}")

            else:
                print(f"User {user_id}: Not yet time (next delivery in {time_diff/3600:.1f} hours)")

        except Exception as e:
            print(f"Error processing user {user_id}: {e}")
            continue

if __name__ == "__main__":
    main()
```

---

## 🎯 How It Works

### User Flow:

1. **User enables morning delivery** in app settings
2. **Selects time** (e.g., 08:00 AM)
3. **Chooses timezone** (e.g., America/New_York)
4. **Sets frequency** (daily, weekdays, or weekly)
5. **Adds recipient emails**
6. **Saves settings** → stored in database

### Background Worker Flow:

1. **Cron job runs every hour** (GitHub Actions, cron-job.org, etc.)
2. **Queries database** for users with `auto_delivery_enabled = true`
3. **Calculates if it's time** to send based on user's timezone
4. **Generates newsletter** using AI (Groq)
5. **Sends via email** (Resend)
6. **Updates `last_delivery_at`** timestamp
7. **Logs success/failure**

---

## 🔐 Security Considerations

### Environment Variables:
- Store API keys in GitHub Secrets (for GitHub Actions)
- Or in cron service settings (for external cron)
- Never commit keys to repository

### Rate Limiting:
- Free tier limits:
  - Groq: Rate limits apply
  - Resend: 100 emails/day (test mode)
  - Supabase: Generous free tier

### Email Verification:
- Remember: Resend requires domain verification for production
- See: [RESEND_DOMAIN_SETUP.md](RESEND_DOMAIN_SETUP.md)

---

## 📊 Database Queries

### Check users with delivery enabled:
```sql
SELECT * FROM profiles
WHERE auto_delivery_enabled = true;
```

### View scheduled deliveries:
```sql
SELECT * FROM scheduled_newsletters
WHERE status = 'pending'
ORDER BY scheduled_for ASC;
```

### Get delivery history:
```sql
SELECT
    p.email,
    p.delivery_time,
    p.delivery_timezone,
    p.last_delivery_at
FROM profiles p
WHERE p.auto_delivery_enabled = true
ORDER BY p.last_delivery_at DESC;
```

---

## 🧪 Testing

### Test Locally:

1. Run database migration
2. Add UI code to app
3. Set delivery time to 2 minutes from now
4. Run delivery script manually:
   ```bash
   python scripts/send_scheduled_newsletters.py
   ```
5. Check email inbox

### Test on HF Spaces:

1. Deploy app with UI changes
2. Set up GitHub Actions workflow
3. Trigger manually first (workflow_dispatch)
4. Check logs in GitHub Actions tab
5. Verify emails received

---

## 🚀 Deployment Checklist

- [ ] Run database migration in Supabase
- [ ] Add delivery UI to app
- [ ] Create delivery script
- [ ] Set up GitHub Actions (or cron service)
- [ ] Add secrets to GitHub repo
- [ ] Test manually
- [ ] Enable automatic runs
- [ ] Monitor logs
- [ ] Verify deliveries working

---

## 💡 Alternative Approaches

### Simple Approach (No Background Worker):

Instead of automatic delivery, add a "Schedule for Later" button:

1. User generates newsletter
2. Clicks "Schedule Send"
3. Selects date/time
4. Newsletter saved to `scheduled_newsletters` table
5. User manually triggers "Send Scheduled" later
6. Or use a simple external cron to check hourly

### Advanced Approach (Full Automation):

1. Deploy separate worker service (Railway/Render)
2. Use APScheduler for precise timing
3. Run continuously, checking every minute
4. More reliable but requires paid hosting

---

## 📚 Resources

### Code Files:
- Scheduler: [utils/delivery_scheduler.py](../utils/delivery_scheduler.py)
- Database: [database/add_delivery_schedule.sql](../database/add_delivery_schedule.sql)

### External Services:
- GitHub Actions: https://docs.github.com/actions
- cron-job.org: https://cron-job.org
- Railway: https://railway.app
- Render: https://render.com

### Documentation:
- Timezone handling: https://pytz.sourceforge.net
- Supabase RPC: https://supabase.com/docs/guides/database/functions
- Resend API: https://resend.com/docs

---

## 🎯 Current Status

### ✅ Completed:
- Scheduler module with timezone support
- Database schema for delivery preferences
- Scheduled newsletters table
- Helper functions for queries
- Documentation

### ⏳ To Implement:
- UI for delivery settings (code provided above)
- Background delivery script (code provided above)
- GitHub Actions workflow (template provided above)
- Testing and monitoring

### 🚀 Ready to Deploy:
All core functionality is ready. Just need to:
1. Run database migration
2. Add UI code to app
3. Set up delivery mechanism (GitHub Actions/cron)

---

**The Morning Delivery feature is designed and ready for implementation!** 🎉

Follow the steps above to enable automatic newsletter delivery at 08:00 AM (or any time) in your users' local timezones.
