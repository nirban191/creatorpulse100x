# 📅 External Cron Service Setup Guide

## 🎯 Overview

Set up automatic newsletter delivery using **free external cron services**. No server management needed!

---

## ✅ Option 1: cron-job.org (Recommended - Easiest)

**Website**: https://cron-job.org
**Cost**: FREE
**Limits**: 50 jobs, 1-minute minimum interval

### Step-by-Step Setup:

#### 1. Create Account
1. Go to https://cron-job.org
2. Click "Sign up" (free)
3. Verify your email

#### 2. Deploy Script to Server

You need a publicly accessible endpoint. Choose one:

**Option A: Use Hugging Face Space (Recommended)**

Deploy an API endpoint to your HF Space:

1. Add this file: `api.py`
```python
from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "CreatorPulse API Running"}

@app.get("/api/send-scheduled-newsletters")
def send_scheduled():
    """Trigger scheduled newsletter delivery"""
    try:
        result = subprocess.run(
            ["python3", "scripts/send_scheduled_newsletters.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

2. Update `Dockerfile`:
```dockerfile
# Add FastAPI
RUN pip install --no-cache-dir fastapi uvicorn

# Change CMD to run API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
```

3. Push to HF Space
4. Your endpoint: `https://nirban191-creatorpulse.hf.space/api/send-scheduled-newsletters`

**Option B: Use Railway/Render (Alternative)**

Deploy just the script as a web service:
- Railway: https://railway.app (free tier)
- Render: https://render.com (free tier)

#### 3. Configure cron-job.org

1. Login to cron-job.org
2. Click "Create cronjob"
3. Fill in:
   - **Title**: CreatorPulse Newsletter Delivery
   - **Address**: `https://nirban191-creatorpulse.hf.space/api/send-scheduled-newsletters`
   - **Schedule**:
     - Every 1 hour
     - Or use cron expression: `0 * * * *`
   - **Notifications**: Email on failure (optional)
4. Click "Create cronjob"
5. ✅ Done!

#### 4. Test It

1. Click "Execute now" in cron-job.org
2. Check execution log
3. Verify newsletter sent (check email)

---

## ✅ Option 2: EasyCron

**Website**: https://www.easycron.com
**Cost**: FREE (10 cron jobs)
**Limits**: 1-minute minimum interval

### Setup:

1. Sign up at https://www.easycron.com
2. Click "Add Cron Job"
3. Configure:
   - **URL**: Your API endpoint
   - **Cron Expression**: `0 * * * *` (every hour)
   - **Name**: CreatorPulse Delivery
4. Save and enable

---

## ✅ Option 3: UptimeRobot (Clever Hack)

**Website**: https://uptimerobot.com
**Cost**: FREE
**Note**: Designed for monitoring, but can trigger endpoints

### Setup:

1. Sign up at https://uptimerobot.com
2. Add New Monitor:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: CreatorPulse Delivery
   - **URL**: Your API endpoint
   - **Monitoring Interval**: 1 hour (free tier max: 5 min)
3. Save

**Limitation**: Minimum 5-minute checks on free tier (too frequent for our use case). Better for high-frequency checks.

---

## ✅ Option 4: GitHub Actions (Best for HF Spaces)

**Cost**: FREE
**Limits**: Generous (2,000 minutes/month)
**Benefit**: No external dependencies

### Setup:

1. Create `.github/workflows/scheduled-delivery.yml`:

```yaml
name: Send Scheduled Newsletters

on:
  schedule:
    # Runs every hour at minute 0
    - cron: '0 * * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  send-newsletters:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install groq supabase resend python-dotenv pytz

      - name: Send scheduled newsletters
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
        run: python scripts/send_scheduled_newsletters.py
```

2. Add secrets to GitHub:
   - Go to repo Settings → Secrets → Actions
   - Add all 4 API keys

3. Commit and push workflow file

4. GitHub will run it automatically every hour!

---

## 📊 Comparison

| Service | Cost | Interval | Setup | Best For |
|---------|------|----------|-------|----------|
| **cron-job.org** | Free | 1 min+ | Easy | Most users |
| **EasyCron** | Free | 1 min+ | Easy | Alternative |
| **GitHub Actions** | Free | 1 min+ | Medium | Developers |
| **UptimeRobot** | Free | 5 min+ | Easy | Monitoring |

**Recommendation**: Use **cron-job.org** or **GitHub Actions**

---

## 🧪 Testing Your Setup

### Test Locally First:

```bash
# Navigate to project
cd /path/to/creatorpulse

# Activate venv
source venv/bin/activate

# Set environment variables
export GROQ_API_KEY=your_key
export SUPABASE_URL=your_url
export SUPABASE_KEY=your_key
export RESEND_API_KEY=your_key

# Run script manually
python scripts/send_scheduled_newsletters.py
```

**Expected output**:
```
[2025-10-23 08:00:00] Starting scheduled delivery check...
Found 1 users with automatic delivery enabled

--- Processing user abc-123 ---
  Time: 08:00:00 America/New_York
  Frequency: daily
  Recipients: 1
  Next delivery: 2025-10-23 12:00:00+00:00
  Time until delivery: 0.1 hours
  ✓ TIME TO SEND!
  Generating newsletter...
  Newsletter generated (1234 chars)
  Sending to 1 recipients...
  ✅ Newsletter sent successfully!
  Updated last_delivery_at timestamp

====================================================
Delivery check complete
Newsletters sent: 1
====================================================
```

### Test with Cron Service:

1. Configure delivery in app (set time to 5 minutes from now)
2. Wait for cron to trigger
3. Check email inbox
4. Verify newsletter received

---

## 🔐 Security Best Practices

### 1. Use Environment Variables
- Never hardcode API keys
- Use secrets in GitHub Actions
- Use environment variables in HF Space

### 2. Add Authentication (Optional)
Secure your API endpoint:

```python
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

SECRET_TOKEN = os.getenv("CRON_SECRET_TOKEN", "change-me")

@app.get("/api/send-scheduled-newsletters")
def send_scheduled(authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ... rest of code
```

Then configure cron-job.org with header:
```
Authorization: Bearer your-secret-token
```

### 3. Rate Limiting
Add rate limiting to prevent abuse:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/send-scheduled-newsletters")
@limiter.limit("10/hour")
def send_scheduled():
    # ... code
```

---

## 🚨 Troubleshooting

### Cron job fails
1. Check endpoint URL is correct and accessible
2. Verify API keys are set correctly
3. Check execution logs in cron service
4. Test endpoint manually in browser

### Newsletter not sent
1. Check user has delivery enabled in database
2. Verify delivery time is correct
3. Check timezone is set properly
4. Ensure email addresses are valid
5. Check Resend API key is valid

### Timeout errors
1. Increase script timeout (default: 5 minutes)
2. Reduce number of articles generated
3. Use faster AI model (Llama 3.2 3B)

---

## 📈 Monitoring

### Check Delivery Status:

```sql
-- View users with delivery enabled
SELECT
    email,
    delivery_time,
    delivery_timezone,
    delivery_frequency,
    last_delivery_at
FROM profiles
WHERE auto_delivery_enabled = true;

-- Check recent deliveries
SELECT
    p.email,
    sn.title,
    sn.scheduled_for,
    sn.sent_at,
    sn.status
FROM scheduled_newsletters sn
JOIN profiles p ON p.id = sn.user_id
ORDER BY sn.created_at DESC
LIMIT 10;
```

### Set Up Alerts:

**Email Notifications**:
- cron-job.org: Enable "Email on failure"
- GitHub Actions: Set up workflow failure notifications

**Logs**:
- cron-job.org: View execution history
- GitHub Actions: Check workflow runs tab
- HF Space: Check logs in Space interface

---

## 🎯 Next Steps

1. ✅ Deploy script to accessible endpoint
2. ✅ Configure cron service
3. ✅ Test with manual trigger
4. ✅ Wait for first automatic delivery
5. ✅ Monitor and adjust as needed

---

## 📚 Additional Resources

- **cron-job.org docs**: https://cron-job.org/en/documentation/
- **GitHub Actions cron**: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule
- **FastAPI deployment**: https://fastapi.tiangolo.com/deployment/
- **HF Spaces docs**: https://huggingface.co/docs/hub/spaces

---

**🎉 Your automatic morning delivery is now set up!**

Newsletters will be generated and sent automatically every hour to users who have scheduled delivery enabled.
