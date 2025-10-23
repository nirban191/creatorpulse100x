# 🚀 CreatorPulse Advanced Features Roadmap

## Current Status: MVP Complete ✅

Your CreatorPulse app currently has:
- ✅ Multi-source content aggregation (Twitter, YouTube, RSS)
- ✅ AI-powered newsletter generation (10 Groq models)
- ✅ Writing style training
- ✅ User authentication & database
- ✅ Email delivery (with domain verification)

---

## 🎯 Phase 2: Advanced Features

### 1. Research & Trend Engine 🔥

**Goal:** Automatically detect trending topics and spikes in your niche

#### Components:

**A. Scheduled Content Crawling**
- Set up cron jobs to crawl sources every 6/12/24 hours
- Store content in Supabase with timestamps
- Track mention frequency over time

**B. Spike Detection Algorithm**
```python
# Detect when a topic appears 2-3x more than usual
def detect_spikes(topic_frequency_history):
    baseline = average_last_7_days
    current = today_frequency
    if current > baseline * 2:
        return "TRENDING"
```

**C. Integration Options**

**Option 1: Firecrawl (Recommended)**
- API: https://firecrawl.dev
- Crawls websites, blogs, forums
- Returns clean markdown content
- $0.50/1000 pages

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key='your_key')
result = app.crawl_url('https://news.ycombinator.com')
```

**Option 2: Google Trends API**
- Free tier available
- Track search interest over time
- Compare related topics

```python
from pytrends.request import TrendReq

pytrends = TrendReq()
pytrends.build_payload(['AI', 'ChatGPT'], timeframe='now 7-d')
trending_data = pytrends.interest_over_time()
```

**Option 3: Custom Web Scraper**
- Use BeautifulSoup (already installed)
- Scrape Reddit, HackerNews, Twitter
- Free but requires maintenance

#### Implementation Plan:

**Step 1: Create Trend Detection Module**
```
utils/trend_detector.py
- track_topic_frequency()
- detect_spikes()
- get_trending_topics()
```

**Step 2: Add Scheduled Jobs**
```
utils/scheduler.py
- schedule_content_crawl()
- schedule_trend_analysis()
- Use APScheduler or Celery
```

**Step 3: Store Trend Data**
```sql
-- New table in database/schema.sql
CREATE TABLE trends (
    id UUID PRIMARY KEY,
    topic TEXT,
    mention_count INTEGER,
    spike_detected BOOLEAN,
    detected_at TIMESTAMP
);
```

**Step 4: Integrate with Newsletter Generator**
- Pass trending topics to AI
- AI highlights "What's trending this week"
- Include spike analysis in newsletter

---

### 2. Morning Delivery 📧

**Goal:** Automatically send newsletters at 08:00 local time

#### Components:

**A. Scheduled Email Sending**
```python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import time
import pytz

def schedule_morning_delivery(user_id, timezone, delivery_time):
    scheduler = BackgroundScheduler()

    # Convert user's local time to UTC
    user_tz = pytz.timezone(timezone)
    delivery_time_utc = user_tz.localize(delivery_time).astimezone(pytz.UTC)

    # Schedule daily job
    scheduler.add_job(
        generate_and_send_newsletter,
        'cron',
        hour=delivery_time_utc.hour,
        minute=delivery_time_utc.minute,
        args=[user_id]
    )
    scheduler.start()
```

**B. User Preferences**
```sql
-- Add to profiles table
ALTER TABLE profiles ADD COLUMN delivery_enabled BOOLEAN DEFAULT false;
ALTER TABLE profiles ADD COLUMN delivery_time TIME DEFAULT '08:00:00';
ALTER TABLE profiles ADD COLUMN timezone TEXT DEFAULT 'America/New_York';
ALTER TABLE profiles ADD COLUMN delivery_frequency TEXT DEFAULT 'daily';
```

**C. Background Worker**
- Deploy scheduler as separate service
- Or use HF Spaces with persistent storage
- Alternative: Use external cron service (EasyCron, cron-job.org)

#### Implementation Plan:

**Step 1: Add User Settings UI**
```python
# In app_enhanced.py
st.subheader("⏰ Morning Delivery Settings")
enable_delivery = st.toggle("Enable automatic delivery")
delivery_time = st.time_input("Delivery time", value=time(8, 0))
timezone = st.selectbox("Timezone", pytz.all_timezones)
frequency = st.selectbox("Frequency", ["daily", "weekdays", "weekly"])
```

**Step 2: Create Background Scheduler**
```
utils/delivery_scheduler.py
- setup_user_schedule()
- cancel_user_schedule()
- send_scheduled_newsletter()
```

**Step 3: Deployment Options**

**Option A: Separate Worker Service**
- Deploy to Railway, Render, or Heroku
- Runs 24/7 background scheduler
- Connects to same Supabase database

**Option B: Serverless Cron**
- Use GitHub Actions with cron
- Or Vercel Cron Jobs
- Triggers API endpoint every hour
- Checks which users need newsletters

**Option C: External Cron Service**
- Set up cron-job.org
- Hits your HF Space endpoint
- `/api/send-scheduled-newsletters`

---

## 🛠️ Implementation Priority

### Quick Wins (1-2 days):
1. **Basic Trend Detection**
   - Track topic mentions in aggregated content
   - Simple spike detection algorithm
   - Display in newsletter

2. **Manual Scheduled Sending**
   - Add "Schedule for later" button
   - Store scheduled time in database
   - User manually triggers at set time

### Medium Effort (3-5 days):
3. **Firecrawl Integration**
   - Sign up for Firecrawl
   - Add content crawling
   - Store crawled content in database

4. **Google Trends Integration**
   - Add pytrends library
   - Track topic interest over time
   - Show trending graph in dashboard

### Advanced (1-2 weeks):
5. **Full Automated Delivery**
   - Deploy background worker service
   - Implement timezone-aware scheduling
   - Add delivery logs and monitoring

6. **Advanced Spike Detection**
   - ML-based anomaly detection
   - Compare across multiple sources
   - Predict emerging trends

---

## 📦 Required New Dependencies

```txt
# Trend Detection
pytrends==4.9.2
scikit-learn==1.5.2

# Web Crawling
firecrawl-py==1.9.4
newspaper3k==0.2.8

# Scheduling
apscheduler==3.10.4
celery==5.4.0
redis==5.2.1

# Timezone handling
pytz==2024.2  # Already installed
```

---

## 🎯 Minimal Implementation (Start Here)

### Phase 2A: Basic Trend Detection (No external APIs)

**File: `utils/trend_detector.py`**
```python
from collections import Counter
from datetime import datetime, timedelta

class TrendDetector:
    def __init__(self, db):
        self.db = db

    def analyze_content(self, content_items):
        """Extract keywords and detect trends from content"""
        keywords = []
        for item in content_items:
            # Simple keyword extraction
            words = item.get('content', '').split()
            keywords.extend([w.lower() for w in words if len(w) > 5])

        # Count frequency
        counter = Counter(keywords)

        # Get historical data from last 7 days
        historical = self._get_historical_frequency()

        # Detect spikes
        trending = []
        for keyword, count in counter.most_common(20):
            baseline = historical.get(keyword, 0)
            if count > baseline * 2:  # 2x spike
                trending.append({
                    'keyword': keyword,
                    'current_count': count,
                    'baseline': baseline,
                    'spike_factor': count / max(baseline, 1)
                })

        return trending
```

### Phase 2B: Simple Scheduled Delivery (No background worker)

**Use Streamlit's built-in session state + user triggers**

```python
# In app_enhanced.py
st.subheader("📅 Schedule Newsletter")
schedule_enabled = st.checkbox("Schedule for later")

if schedule_enabled:
    schedule_date = st.date_input("Send date")
    schedule_time = st.time_input("Send time")

    if st.button("Schedule Send"):
        # Store in database
        db.schedule_newsletter(
            user_id=st.session_state.user_id,
            send_at=datetime.combine(schedule_date, schedule_time),
            content=generated_content
        )
        st.success("✅ Newsletter scheduled!")

# User comes back later and clicks "Send Scheduled"
if st.button("📤 Send Scheduled Newsletters"):
    scheduled = db.get_due_newsletters(st.session_state.user_id)
    for newsletter in scheduled:
        send_email(newsletter)
```

---

## 🚀 Quick Start Guide

### To Add Basic Trend Detection (Today):

1. Create `utils/trend_detector.py` with the code above
2. Import in `app_enhanced.py`
3. Add "🔥 Trending Topics" section in UI
4. Pass trends to newsletter generator

### To Add Scheduling (This Week):

1. Add schedule fields to database
2. Add UI for scheduling
3. Create cron job endpoint
4. Set up free cron service to hit endpoint

---

## 📊 Database Schema Updates

```sql
-- Trends tracking
CREATE TABLE IF NOT EXISTS public.trends (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id),
    keyword TEXT NOT NULL,
    mention_count INTEGER DEFAULT 0,
    spike_detected BOOLEAN DEFAULT false,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scheduled newsletters
CREATE TABLE IF NOT EXISTS public.scheduled_newsletters (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id),
    draft_id UUID REFERENCES public.drafts(id),
    scheduled_for TIMESTAMP WITH TIME ZONE NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User delivery preferences
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS auto_delivery_enabled BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS delivery_time TIME DEFAULT '08:00:00',
ADD COLUMN IF NOT EXISTS delivery_timezone TEXT DEFAULT 'UTC',
ADD COLUMN IF NOT EXISTS delivery_frequency TEXT DEFAULT 'daily';
```

---

## 💡 Alternative: Use Existing Tools

Instead of building from scratch:

**For Trends:**
- Use Twitter's Trending API
- Use Google Trends data exports
- Use Reddit's rising posts API

**For Scheduling:**
- Use Beehiiv's scheduler (if you export to Beehiiv)
- Use Substack's scheduler (if you use Substack)
- Use Gmail's "Schedule Send" manually

**Recommendation:** Focus on CreatorPulse's core strength - AI-powered content curation. Let existing newsletter platforms handle delivery scheduling.

---

## 🎯 Next Steps

1. **Choose your priority:**
   - [ ] Trend detection
   - [ ] Morning delivery
   - [ ] Both

2. **Pick implementation level:**
   - [ ] Basic (no external APIs)
   - [ ] Medium (Firecrawl + Trends)
   - [ ] Advanced (Full automation)

3. **Start with Phase 2A** (Basic Trend Detection)
   - No new APIs needed
   - Uses existing content
   - Shows value immediately

**Let me know which feature you want to implement first, and I'll help you build it!** 🚀
