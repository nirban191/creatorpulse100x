# 🚀 Deploy CreatorPulse to Hugging Face Spaces

## Step-by-Step Deployment Guide

### Prerequisites
1. Hugging Face account (sign up at https://huggingface.co/join)
2. HF access token with write permissions
3. Your CreatorPulse repository is ready

---

## Method 1: Push Directly to HF Space (Recommended)

### Step 1: Create a New Space on Hugging Face

1. Go to: https://huggingface.co/new-space
2. Fill in the form:
   - **Owner**: nirban191 (your username)
   - **Space name**: `creatorpulse` (or any name you want)
   - **License**: MIT
   - **Select SDK**: Choose **Docker**
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public or Private
3. Click **"Create Space"**

### Step 2: Get Your HF Access Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name it: `creatorpulse-deploy`
4. Type: Select **"Write"** (important!)
5. Click **"Generate token"**
6. **Copy the token** (you'll need it soon)

### Step 3: Add HF Space as Git Remote

Open your terminal and run these commands:

```bash
# Navigate to your project
cd /Users/nirbanbiswas/Desktop/100x/code/creatorpulse

# Add HF Space as a new git remote
git remote add huggingface https://huggingface.co/spaces/nirban191/creatorpulse

# Verify remotes
git remote -v
```

You should see both `origin` (GitHub) and `huggingface` remotes.

### Step 4: Push to Hugging Face Space

```bash
# Push your main branch to HF Space
git push huggingface main
```

When prompted for credentials:
- **Username**: `nirban191` (your HF username)
- **Password**: Paste your HF access token (from Step 2)

### Step 5: Add Environment Variables (Secrets)

1. Go to your Space: https://huggingface.co/spaces/nirban191/creatorpulse
2. Click **"Settings"** tab
3. Scroll to **"Repository secrets"** section
4. Click **"Add a secret"** for each:

```
Name: GROQ_API_KEY
Value: <your-groq-api-key>

Name: SUPABASE_URL
Value: <your-supabase-url>

Name: SUPABASE_KEY
Value: <your-supabase-key>

Name: RESEND_API_KEY
Value: <your-resend-api-key>
```

**Note**: Get your actual keys from the `.env` file in your local project.

### Step 6: Wait for Build

- HF will automatically detect the Dockerfile
- Build process starts (takes 5-10 minutes)
- Monitor build logs in the Space interface
- Once complete, your app will be live!

### Step 7: Access Your Deployed App

Your app will be available at:
```
https://nirban191-creatorpulse.hf.space
```

Or:
```
https://huggingface.co/spaces/nirban191/creatorpulse
```

---

## Method 2: Use HF CLI (Alternative)

### Install HF CLI

```bash
pip install huggingface_hub
```

### Login to HF

```bash
huggingface-cli login
```

Paste your access token when prompted.

### Push Files to Space

```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/nirban191/creatorpulse hf-space

# Copy your files to the cloned space
cp -r * hf-space/
cd hf-space

# Commit and push
git add .
git commit -m "Deploy CreatorPulse app"
git push
```

---

## Method 3: Manual File Upload (Not Recommended)

If you prefer manual upload:

1. Go to your Space: https://huggingface.co/spaces/nirban191/creatorpulse
2. Click **"Files"** tab
3. Click **"Add file"** → **"Upload files"**
4. Upload these files:
   - `app_enhanced.py`
   - `Dockerfile`
   - `README.md` (with HF metadata)
   - `requirements.txt`
   - All folders: `utils/`, `pages/`, `database/`, `demo_newsletters/`
   - `.streamlit/config.toml`

**Note**: This is tedious and error-prone. Use Method 1 instead!

---

## Troubleshooting

### Build Fails

**Check build logs** in the HF Space interface:
- Click on your Space
- Look for build errors in the logs
- Common issues:
  - Missing secrets (add them in Settings)
  - Python dependency conflicts (check requirements.txt)
  - Dockerfile issues (ensure port 7860 is exposed)

### App Crashes on Startup

1. Check if all secrets are added correctly
2. Verify Supabase credentials
3. Check Groq API key is valid
4. Review application logs in HF Space

### Database Errors

- Ensure Supabase database schema is created
- Run the SQL from `database/schema.sql` in Supabase SQL Editor
- Temporarily disable RLS for testing (see `database/disable_rls_for_dev.sql`)

---

## Updating Your Deployed App

Whenever you make changes locally:

```bash
# Commit changes locally
git add .
git commit -m "Update feature X"

# Push to GitHub
git push origin main

# Push to HF Space
git push huggingface main
```

HF Space will automatically rebuild with the new code.

---

## Important Files for HF Deployment

### README.md (Root)
Must include HF frontmatter:
```yaml
---
title: CreatorPulse
emoji: 📰
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---
```

### Dockerfile
Must expose port 7860:
```dockerfile
EXPOSE 7860
CMD ["streamlit", "run", "app_enhanced.py", "--server.port=7860", ...]
```

### requirements.txt
All Python dependencies must be listed.

---

## Quick Reference

| Action | Command |
|--------|---------|
| Add HF remote | `git remote add huggingface https://huggingface.co/spaces/USERNAME/SPACE_NAME` |
| Push to HF | `git push huggingface main` |
| View Space | `https://huggingface.co/spaces/USERNAME/SPACE_NAME` |
| Add secrets | Go to Space Settings → Repository secrets |
| View logs | Go to Space → Check build logs |

---

## Your Deployment URLs

- **GitHub Repo**: https://github.com/nirban191/creatorpulse100x
- **HF Space** (after deployment): https://huggingface.co/spaces/nirban191/creatorpulse
- **Live App URL**: https://nirban191-creatorpulse.hf.space

---

## Next Steps

1. ✅ Create HF Space
2. ✅ Get HF access token
3. ✅ Add HF as git remote
4. ✅ Push code to HF
5. ✅ Add secrets in HF Space settings
6. ✅ Wait for build to complete
7. ✅ Access your live app!

**Need help?** Check the HF Spaces documentation: https://huggingface.co/docs/hub/spaces
