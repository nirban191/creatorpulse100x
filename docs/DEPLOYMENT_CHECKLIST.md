# 🚀 CreatorPulse Deployment Checklist

## ✅ Local Setup (COMPLETED)

- [x] API Keys configured in `.env` file
- [x] Groq API Key added
- [x] Supabase credentials added
- [x] Resend API Key added

## 📋 Supabase Database Setup (REQUIRED NEXT)

Your Supabase project: https://htqwegnixlhdhrdbjkgp.supabase.co

### Step 1: Run Database Schema

1. Go to your Supabase Dashboard: https://supabase.com/dashboard/project/htqwegnixlhdhrdbjkgp
2. Click **SQL Editor** in the left sidebar
3. Click **New Query**
4. Copy the entire contents of `database/schema.sql` and paste it
5. Click **Run** to create all tables

### Step 2: Disable RLS for Development (Optional)

If you want to test without authentication complications:

1. In SQL Editor, run the contents of `database/disable_rls_for_dev.sql`
2. This temporarily disables Row Level Security for easier testing

**Note:** Re-enable RLS before production deployment!

## 🖥️ Run Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the app
streamlit run app_enhanced.py
```

The app will open at: http://localhost:8501

## 🤗 Hugging Face Spaces Deployment

### Step 1: Create Space

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `creatorpulse` (or your choice)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: Free CPU (basic)

### Step 2: Link GitHub Repository

Choose one method:

**Method A: Import During Creation**
- During Space creation, select "Import from GitHub"
- Enter: `https://github.com/nirban191/creatorpulse100x`
- Branch: `main`

**Method B: Link After Creation**
- Create empty Space
- Go to Space Settings → Repository
- Click "Link to GitHub"
- Select: `nirban191/creatorpulse100x`

### Step 3: Add Secrets in HF Space

1. Go to your Space Settings
2. Click **Variables and secrets**
3. Add these secrets (use your actual API keys from `.env` file):

```
GROQ_API_KEY=<your_groq_api_key>
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_anon_key>
RESEND_API_KEY=<your_resend_api_key>
```

### Step 4: Deploy

Once secrets are added:
- HF will automatically detect the Dockerfile
- Build process starts automatically
- Monitor build logs in the Space interface
- Your app will be live at: `https://huggingface.co/spaces/nirban191/creatorpulse`

## 🧪 Testing Checklist

After deployment, test these features:

- [ ] Sign up with new account
- [ ] Login with credentials
- [ ] Add Twitter source
- [ ] Add YouTube source
- [ ] Upload writing style sample
- [ ] Generate newsletter with Groq AI
- [ ] Try different AI models (Llama 3.1 70B, 8B, Mixtral, etc.)
- [ ] Send test email (if Resend configured)
- [ ] Check dashboard analytics

## 🔒 Security Notes

### Local Development
- `.env` file is git-ignored ✅
- Never commit API keys to repository ✅

### Production (HF Spaces)
- All secrets stored in HF Space settings (encrypted) ✅
- Environment variables injected at runtime ✅

## 📚 Documentation

- Full setup guide: [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)
- Architecture overview: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Database setup: [docs/SUPABASE_SETUP_GUIDE.md](docs/SUPABASE_SETUP_GUIDE.md)
- HF deployment: [docs/HUGGINGFACE_DEPLOYMENT.md](docs/HUGGINGFACE_DEPLOYMENT.md)

## 🆘 Troubleshooting

### Database Connection Issues
- Verify Supabase credentials in `.env`
- Check if database schema is created
- Temporarily disable RLS for testing

### AI Generation Not Working
- Verify GROQ_API_KEY is valid
- Check Groq console for API limits
- Try switching to a different model

### Email Sending Fails
- Verify RESEND_API_KEY
- Check sender email is verified in Resend dashboard
- Review Resend logs for errors

## 🎯 Next Steps

1. **Run database schema** in Supabase SQL Editor
2. **Test locally** with `streamlit run app_enhanced.py`
3. **Deploy to HF Spaces** following steps above
4. **Share your Space** with the world!

---

**Your Space URL (after deployment):**
`https://huggingface.co/spaces/nirban191/creatorpulse`

**GitHub Repository:**
`https://github.com/nirban191/creatorpulse100x`
