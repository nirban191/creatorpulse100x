"""
Trend Discovery Settings Page
Configure automated daily trend discovery from Google Trends
"""

import streamlit as st
from utils.auth import AuthManager
from utils.supabase_client import get_db
from utils.scheduler import trigger_job_manually, get_scheduled_jobs, is_scheduler_running
from datetime import datetime, timedelta
import pandas as pd

# Page config
st.set_page_config(
    page_title="Trend Discovery - CreatorPulse",
    page_icon="📈",
    layout="wide"
)

# Initialize auth and database
auth = AuthManager()
db = get_db()

# Check authentication
if not auth.is_authenticated():
    st.warning("Please log in to access Trend Discovery settings.")
    st.stop()

user = auth.get_current_user()
user_id = user['id']

# Header
st.title("📈 Automated Trend Discovery")
st.markdown("Discover trending topics daily from Google Trends and use them in your newsletters")

# Main tabs
tab1, tab2, tab3 = st.tabs(["⚙️ Settings", "📊 Discovered Trends", "🔧 Advanced"])

# ==================== SETTINGS TAB ====================
with tab1:
    st.header("Trend Discovery Settings")

    # Load current settings
    current_settings = db.get_user_trend_settings(user_id)

    if current_settings:
        is_enabled = current_settings.get('enabled', False)
        selected_categories = current_settings.get('categories', ['tech', 'ai', 'business'])
        custom_keywords = current_settings.get('custom_keywords', [])
        schedule_time = current_settings.get('schedule_time', '09:00:00')
        last_run = current_settings.get('last_run_at')
    else:
        is_enabled = False
        selected_categories = ['tech', 'ai', 'business']
        custom_keywords = []
        schedule_time = '09:00:00'
        last_run = None

    # Enable/Disable toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        enabled = st.toggle(
            "Enable Automated Trend Discovery",
            value=is_enabled,
            help="When enabled, trends will be discovered daily at your scheduled time"
        )

    with col2:
        if last_run:
            last_run_dt = datetime.fromisoformat(last_run.replace('Z', '+00:00'))
            st.caption(f"Last run: {last_run_dt.strftime('%Y-%m-%d %H:%M')}")
        else:
            st.caption("Never run")

    st.divider()

    # Category selection
    st.subheader("Select Categories")
    st.caption("Choose which categories to monitor for trending topics")

    col1, col2, col3 = st.columns(3)

    available_categories = {
        'tech': 'Technology & Computing',
        'ai': 'Artificial Intelligence',
        'business': 'Business & Finance',
        'science': 'Science & Research',
        'news': 'News & Current Events',
        'entertainment': 'Entertainment',
        'health': 'Health & Wellness',
        'sports': 'Sports'
    }

    selected_cats = []

    for idx, (cat_key, cat_label) in enumerate(available_categories.items()):
        col = [col1, col2, col3][idx % 3]
        with col:
            if st.checkbox(
                cat_label,
                value=cat_key in selected_categories,
                key=f"cat_{cat_key}"
            ):
                selected_cats.append(cat_key)

    if not selected_cats and enabled:
        st.warning("Please select at least one category")

    st.divider()

    # Custom keywords (optional)
    st.subheader("Custom Keywords (Optional)")
    st.caption("Add specific keywords you want to monitor (one per line)")

    keywords_text = st.text_area(
        "Keywords",
        value="\n".join(custom_keywords) if custom_keywords else "",
        height=100,
        placeholder="GPT-5\nStreamlit\nAI agents\nWeb3",
        label_visibility="collapsed"
    )

    custom_kw_list = [kw.strip() for kw in keywords_text.split('\n') if kw.strip()]

    st.divider()

    # Schedule time
    st.subheader("Schedule Time")
    col1, col2 = st.columns([2, 3])

    with col1:
        hour = int(schedule_time.split(':')[0])
        minute = int(schedule_time.split(':')[1])

        schedule_hour = st.selectbox(
            "Hour (EST)",
            options=list(range(24)),
            index=hour,
            format_func=lambda x: f"{x:02d}:00"
        )

    with col2:
        st.info(f"Trends will be discovered daily at {schedule_hour:02d}:00 EST")

    # Save button
    st.divider()

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💾 Save Settings", type="primary", use_container_width=True):
            if enabled and not selected_cats:
                st.error("Please select at least one category")
            else:
                result = db.save_user_trend_settings(
                    user_id=user_id,
                    enabled=enabled,
                    categories=selected_cats,
                    custom_keywords=custom_kw_list,
                    schedule_time=f"{schedule_hour:02d}:00:00"
                )

                if result.get('success'):
                    st.success("Settings saved successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to save settings: {result.get('error')}")

    with col2:
        if st.button("🎯 Trigger Discovery Now", use_container_width=True):
            if not enabled:
                st.warning("Please enable trend discovery first")
            else:
                with st.spinner("Discovering trends... This may take 1-2 minutes"):
                    result = trigger_job_manually()
                    if result.get('success'):
                        st.success("Trends discovered successfully! Check the 'Discovered Trends' tab")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.get('error')}")

# ==================== DISCOVERED TRENDS TAB ====================
with tab2:
    st.header("Recently Discovered Trends")

    # Filter options
    col1, col2, col3 = st.columns(3)

    with col1:
        days_filter = st.selectbox(
            "Show trends from",
            options=[1, 3, 7, 14, 30],
            index=2,
            format_func=lambda x: f"Last {x} days"
        )

    with col2:
        category_filter = st.selectbox(
            "Filter by category",
            options=['all'] + list(available_categories.keys()),
            format_func=lambda x: 'All Categories' if x == 'all' else available_categories.get(x, x)
        )

    with col3:
        st.metric("Total Trends", "Loading...")

    # Fetch trends
    if category_filter == 'all':
        trends = db.get_trending_content(user_id, days_back=days_filter)
    else:
        trends = db.get_trending_by_category(user_id, category_filter, days_back=days_filter)

    # Update metric
    col3.metric("Total Trends", len(trends))

    st.divider()

    if not trends:
        st.info("No trends discovered yet. Enable trend discovery in Settings and trigger a manual discovery, or wait for the next scheduled run.")
    else:
        # Display trends in cards
        for trend in trends:
            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    # Trend title with link
                    if trend.get('url'):
                        st.markdown(f"### [{trend['title']}]({trend['url']})")
                    else:
                        st.markdown(f"### {trend['title']}")

                    # Description
                    if trend.get('description'):
                        st.markdown(trend['description'])

                    # Metadata row
                    meta_col1, meta_col2, meta_col3 = st.columns(3)

                    with meta_col1:
                        category_badge = trend.get('category', 'all')
                        st.caption(f"📂 {available_categories.get(category_badge, category_badge.title())}")

                    with meta_col2:
                        discovered_at = datetime.fromisoformat(trend['discovered_at'].replace('Z', '+00:00'))
                        st.caption(f"🕐 {discovered_at.strftime('%Y-%m-%d %H:%M')}")

                    with meta_col3:
                        if trend.get('keywords'):
                            keywords_str = ", ".join(trend['keywords'][:3])
                            st.caption(f"🏷️ {keywords_str}")

                with col2:
                    if st.button("🗑️ Remove", key=f"del_{trend['id']}", use_container_width=True):
                        if db.delete_trending_content(user_id, trend['id']):
                            st.success("Trend removed")
                            st.rerun()
                        else:
                            st.error("Failed to remove")

                st.divider()

# ==================== ADVANCED TAB ====================
with tab3:
    st.header("Advanced Settings & Information")

    # Scheduler status
    st.subheader("Scheduler Status")

    scheduler_running = is_scheduler_running()

    col1, col2 = st.columns(2)

    with col1:
        if scheduler_running:
            st.success("✅ Scheduler is running")
        else:
            st.warning("⚠️ Scheduler is not running")

    with col2:
        if st.button("🔄 Refresh Status"):
            st.rerun()

    # Scheduled jobs
    st.subheader("Scheduled Jobs")

    jobs = get_scheduled_jobs()

    if jobs:
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'Job ID': job['id'],
                'Name': job['name'],
                'Next Run': job['next_run_time'] if job['next_run_time'] else 'Not scheduled',
                'Trigger': job['trigger']
            })

        st.dataframe(pd.DataFrame(jobs_data), use_container_width=True)
    else:
        st.info("No scheduled jobs found")

    st.divider()

    # Rate limiting info
    st.subheader("Google Trends API Information")

    st.info("""
    **Rate Limiting:**
    - Google Trends uses rate limiting to prevent abuse
    - We automatically wait 61 seconds between requests
    - This is why manual discovery takes 1-2 minutes

    **Data Sources:**
    - Daily trending searches from Google Trends
    - Real-time trending topics
    - Related queries and rising searches

    **Free Tier:**
    - No API key required
    - Unlimited requests (with rate limiting)
    - No cost
    """)

    st.divider()

    # How it works
    with st.expander("📖 How Trend Discovery Works"):
        st.markdown("""
        ### Automated Workflow

        1. **Daily Scheduler** runs at your configured time (default: 9 AM EST)
        2. **Fetches Trends** from Google Trends for your selected categories
        3. **Saves to Database** with metadata (keywords, URLs, timestamps)
        4. **Available for Newsletters** in the Generate Newsletter page

        ### Using Trends in Newsletters

        1. Go to the main page (Generate Newsletter)
        2. Check the "Include trending topics" checkbox
        3. Trending content from the last 7 days will be included
        4. AI will incorporate trends into your newsletter content

        ### Manual Discovery

        You can trigger trend discovery manually at any time by clicking the
        "Trigger Discovery Now" button in the Settings tab. This is useful for:
        - Testing your configuration
        - Getting fresh trends immediately
        - Supplementing automated daily runs
        """)

    with st.expander("🔧 Troubleshooting"):
        st.markdown("""
        ### Common Issues

        **No trends discovered:**
        - Check that you have categories selected
        - Ensure trend discovery is enabled
        - Try triggering manually to see error messages
        - Check database RLS policies are configured

        **Database errors:**
        - Run SQL scripts in `database/` folder in Supabase SQL Editor
        - Ensure tables exist: `trending_content`, `trend_settings`
        - Verify RLS policies allow INSERT/SELECT

        **Scheduler not running:**
        - Scheduler starts automatically with the app
        - Check app logs for error messages
        - Try restarting the Streamlit app
        """)

# Footer
st.divider()
st.caption("💡 Tip: Enable trend discovery to automatically stay updated with the latest trending topics in your industry!")
