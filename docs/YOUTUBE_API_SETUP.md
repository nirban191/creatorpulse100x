# YouTube Data API v3 Setup Guide

This guide will help you set up the YouTube Data API v3 to fetch real video data from YouTube channels for your newsletters.

## Why YouTube API?

The YouTube Data API allows CreatorPulse to:
- Fetch latest videos from specified YouTube channels
- Get video titles, descriptions, and metadata
- Track views, likes, and engagement metrics
- Curate trending video content for your newsletter

## Free Tier Limits

✅ **Completely FREE** - No credit card required
📊 **10,000 quota units/day**
- ~100 video detail requests (1 unit each)
- ~100 searches (100 units each)
- ~30 channel lookups (100 units each)

**Perfect for newsletter curation!**

---

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"NEW PROJECT"**
3. Enter project name: `CreatorPulse` (or any name)
4. Click **"CREATE"**
5. Wait for project creation (30 seconds)

### 2. Enable YouTube Data API v3

1. In the Google Cloud Console, go to **"APIs & Services"** → **"Library"**
2. Search for: `YouTube Data API v3`
3. Click on **"YouTube Data API v3"**
4. Click the **"ENABLE"** button
5. Wait for API to be enabled (~10 seconds)

### 3. Create API Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** → **"API key"**
3. Your API key will be created and displayed
4. **IMPORTANT:** Click **"RESTRICT KEY"** (highly recommended)

### 4. Restrict API Key (Recommended)

To prevent unauthorized use and quota theft:

1. In the "Edit API key" screen:
   - **Application restrictions**: Choose "None" or "IP addresses" (if you have a static IP)
   - **API restrictions**:
     - Select **"Restrict key"**
     - Check **"YouTube Data API v3"** only
2. Click **"SAVE"**

### 5. Copy Your API Key

1. Copy the API key (looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)
2. Keep it secure - don't share it publicly!

### 6. Add to CreatorPulse

1. Open your `.env` file in CreatorPulse project
2. Add your API key:
   ```bash
   YOUTUBE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
3. Save the file
4. Restart CreatorPulse

---

## Testing Your Setup

### Quick Test

1. Go to **Source Connections** in CreatorPulse
2. Add a YouTube channel (try: `@fireship` or `@mkbhd`)
3. Click **"Add Source"**
4. Check if real video data appears!

### Verify in Terminal

You should see logs like:
```
✅ Fetched 10 videos from Fireship
✅ YouTube API working correctly
```

If you see errors:
```
❌ YouTube API quota exceeded
⚠️ YouTube API not configured
```
→ Check your API key or quota

---

## Monitoring Quota Usage

### Check Current Usage

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to: **"APIs & Services"** → **"Dashboard"**
3. Click on **"YouTube Data API v3"**
4. View **"Metrics"** tab to see:
   - Requests today
   - Quota units consumed
   - Errors (if any)

### Understanding Quota Costs

| Operation | Cost (units) | Example |
|-----------|--------------|---------|
| Get video details | 1 | Fetch title, views, likes |
| Search channels | 100 | Find channel by name |
| List channel uploads | 100 | Get recent videos |
| Get video statistics | 1 | Views, likes, comments |

**Example:** Fetching 10 videos from 3 channels:
- 3 channel lookups = 300 units
- 30 video details = 30 units
- **Total: 330 units** (out of 10,000 daily limit)

---

## Quota Exceeded? Here's What Happens

CreatorPulse automatically handles quota exhaustion:

1. **Detects quota exceeded error**
2. **Falls back to mock data** (or cached data if available)
3. **Shows warning** to user: "⚠️ YouTube API quota exceeded"
4. **Resets at midnight UTC** automatically

### Tips to Conserve Quota

- Fetch videos once per day, not on every page load
- Cache results in database (future enhancement)
- Limit `max_results` parameter to 5-10 videos per channel
- Don't fetch from too many channels at once

---

## Troubleshooting

### Error: "API key not valid"

**Solution:**
- Check that you copied the entire API key
- Ensure there are no extra spaces in `.env`
- Verify the key is enabled in Google Cloud Console

### Error: "The request cannot be completed because you have exceeded your quota"

**Solution:**
- Wait until midnight UTC for quota reset
- Check quota usage in Google Cloud Console
- Reduce number of channels or fetch frequency

### Error: "Access Not Configured"

**Solution:**
- Make sure YouTube Data API v3 is **enabled** in your project
- Wait 5-10 minutes after enabling the API
- Refresh your credentials page

### No videos appearing

**Solution:**
- Check if YOUTUBE_API_KEY is set in `.env`
- Restart the CreatorPulse application
- Verify channel URLs/handles are correct
- Check terminal logs for error messages

---

## Security Best Practices

### ✅ DO:
- Restrict API key to YouTube Data API v3 only
- Keep your API key in `.env` file (gitignored)
- Use IP restrictions if deploying to a server
- Regenerate key if accidentally exposed

### ❌ DON'T:
- Commit API keys to GitHub
- Share API keys publicly
- Use the same key across multiple projects
- Leave keys unrestricted

---

## Cost

**100% FREE** ✅

- No credit card required
- No hidden fees
- 10,000 units/day forever
- Sufficient for small-medium newsletters

**Need more quota?**
- [Request quota increase](https://support.google.com/youtube/contact/yt_api_form) (usually approved for legitimate use cases)
- Upgrade to paid Google Cloud plan (rarely needed)

---

## Alternative: Without YouTube API

If you don't want to set up the API:

CreatorPulse will still work! It will:
- Use **mock data** for YouTube videos
- Allow manual paste of video URLs
- Focus on **RSS feeds** and **Twitter** (if configured)

The app gracefully degrades when YouTube API is unavailable.

---

## Need Help?

- **YouTube API Documentation**: https://developers.google.com/youtube/v3
- **Quota Calculator**: https://developers.google.com/youtube/v3/determine_quota_cost
- **Google Cloud Support**: https://cloud.google.com/support

---

## Summary

1. Create Google Cloud project (2 minutes)
2. Enable YouTube Data API v3 (1 minute)
3. Create & restrict API key (2 minutes)
4. Add to `.env` file (30 seconds)
5. Test in CreatorPulse ✅

**Total time: ~5 minutes**
**Cost: $0.00 forever**

Happy curating! 🎬📰
