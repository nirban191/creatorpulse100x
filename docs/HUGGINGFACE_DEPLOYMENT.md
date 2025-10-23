# 🚀 Deploy CreatorPulse to Hugging Face Spaces

Complete guide to deploy your CreatorPulse app on Hugging Face Spaces.

---

## 📋 Prerequisites

- Hugging Face account (free): https://huggingface.co/join
- GitHub repository with your code: https://github.com/nirban191/creatorpulse100x
- API keys ready (Groq, Supabase, Resend)

---

## 🎯 Step-by-Step Deployment

### Step 1: Create a New Space

1. Go to: https://huggingface.co/new-space
2. Fill in details:
   - **Space name**: `creatorpulse` (or your choice)
   - **License**: MIT
   - **Select SDK**: Streamlit
   - **Space hardware**: CPU basic (free tier)
   - **Visibility**: Public (or Private)
3. Click **"Create Space"**

### Step 2: Connect to GitHub

**Option A: Import from GitHub (Recommended)**

1. After creating the space, click **"Files and versions"** tab
2. Click **"⚙️ Settings"** (top right)
3. Scroll to **"Sync with GitHub"**
4. Click **"Connect to GitHub"**
5. Authorize Hugging Face
6. Select repository: `nirban191/creatorpulse100x`
7. Select branch: `main`
8. Click **"Sync repository"**

**Option B: Manual Upload**

1. Clone your repo locally (if not already)
2. Go to **"Files and versions"** tab
3. Click **"Add file"** → **"Upload files"**
4. Upload all files from your project

### Step 3: Add API Keys (Secrets)

1. Go to your Space settings: **"⚙️ Settings"** tab
2. Scroll to **"Repository secrets"**
3. Add these secrets one by one:

```
GROQ_API_KEY = your_groq_api_key_here
SUPABASE_URL = https://your-project.supabase.co
SUPABASE_KEY = your_supabase_anon_key_here
RESEND_API_KEY = your_resend_api_key_here
```

**To add each secret:**
- Click **"New secret"**
- Name: `GROQ_API_KEY`
- Value: `your_actual_key`
- Click **"Save"**
- Repeat for all keys

### Step 4: Configure Space (if needed)

The space should auto-configure from `README_HF.md`, but if needed:

1. Make sure these files exist in your repo:
   - `README_HF.md` (with frontmatter metadata)
   - `requirements.txt` (all dependencies)
   - `packages.txt` (system dependencies)
   - `.streamlit/config.toml` (Streamlit config)
   - `app_enhanced.py` (main app file)

2. The frontmatter in `README_HF.md` should have:
```yaml
---
title: CreatorPulse
sdk: streamlit
sdk_version: "1.32.0"
app_file: app_enhanced.py
---
```

### Step 5: Wait for Build

1. Go to **"App"** tab
2. You'll see **"Building..."** status
3. Wait 2-5 minutes for deployment
4. Once done, you'll see **"Running"** status
5. Your app is live! 🎉

---

## 🔑 Setting Up API Keys

Users of your deployed app will need to add their API keys. Here's how:

### For Groq API:
1. Get free key: https://console.groq.com/keys
2. In app sidebar: Settings → Secrets → Add `GROQ_API_KEY`

### For Supabase:
1. Create free project: https://supabase.com
2. Run the database schema from `database/schema.sql`
3. Get URL and Key from Settings → API
4. Add to Hugging Face Secrets

### For Resend (Optional):
1. Get free key: https://resend.com/api-keys
2. Add to Hugging Face Secrets

---

## 🎨 Customization

### Change App Title/Icon

Edit `README_HF.md` frontmatter:
```yaml
---
title: Your Custom Name
emoji: 🚀
colorFrom: red
colorTo: blue
---
```

### Update Python Version

Edit `README_HF.md`:
```yaml
python_version: "3.9"
```

### Change Hardware

In Space Settings:
- Free: CPU basic (2 vCPU, 16GB RAM)
- Paid: CPU upgrade, GPU options

---

## 🐛 Troubleshooting

### Build Fails

**Check logs:**
1. Go to **"App"** tab
2. Click **"See logs"** at bottom
3. Look for error messages

**Common issues:**
- Missing dependencies → Check `requirements.txt`
- Import errors → Verify all files uploaded
- API errors → Check secrets are set correctly

### App Runs but Errors

**Check:**
1. API keys are set in Secrets
2. Supabase database schema is created
3. RLS is disabled for development (see `database/disable_rls_for_dev.sql`)

### Secrets Not Working

1. Make sure secret names match exactly (case-sensitive)
2. No spaces in secret names
3. Re-save secrets if changed
4. Restart space: Settings → "Factory reboot"

---

## 📊 Monitoring

### View Logs

```bash
# In Space settings, enable "Detailed logs"
# Then view in App tab → "See logs"
```

### Check Usage

- Go to Space → "Analytics" tab
- See visitor count, resource usage
- Monitor API calls

### Update App

**If using GitHub sync:**
1. Push changes to GitHub
2. Hugging Face auto-syncs
3. App rebuilds automatically

**If manual:**
1. Upload changed files
2. Space rebuilds automatically

---

## 🌐 Share Your Space

Once deployed, share your app:

**URL Format:**
```
https://huggingface.co/spaces/nirban191/creatorpulse
```

**Embed in Website:**
```html
<iframe src="https://nirban191-creatorpulse.hf.space"
        width="100%" height="800px"></iframe>
```

**Share on Social Media:**
- Twitter/X: Include screenshot + link
- LinkedIn: Write post about your AI project
- Reddit: Share in relevant communities

---

## 💰 Cost

**Free Tier:**
- CPU basic (2 vCPU, 16GB RAM)
- Unlimited usage
- Public spaces
- Great for demos and personal use

**Paid Tiers:**
- CPU upgrade: $0.05/hour
- GPU T4: $0.60/hour
- GPU A10G: $3.15/hour
- Private spaces available

---

## 🎯 Post-Deployment Checklist

- [ ] Space is running
- [ ] All API keys added to Secrets
- [ ] Database schema created in Supabase
- [ ] Test login/signup flow
- [ ] Test AI generation with different models
- [ ] Test email sending (if using Resend)
- [ ] Share your space URL!

---

## 📚 Resources

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Streamlit Docs**: https://docs.streamlit.io/
- **Groq API Docs**: https://console.groq.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Your GitHub Repo**: https://github.com/nirban191/creatorpulse100x

---

## 🆘 Support

**Issues?**
- Check Space logs first
- Review this guide
- Check GitHub Issues
- Ask in Hugging Face Discussions

---

**Your CreatorPulse app is ready for deployment!** 🚀

Deploy to Hugging Face Spaces for free hosting and share your AI newsletter curator with the world!
