# Groq API Setup Guide 🚀

## Why Groq?

- **FREE**: No credit card required
- **FAST**: Up to 10x faster than OpenAI
- **POWERFUL**: Uses Llama 3.1 70B model
- **GENEROUS**: 30 requests/minute free tier

## Quick Setup (2 minutes)

### Step 1: Get Your Free API Key

1. Go to **https://console.groq.com/**
2. Sign up with Google/GitHub (takes 30 seconds)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"**
5. Give it a name like "CreatorPulse"
6. Copy the key (starts with `gsk_...`)

### Step 2: Add to Your App

Option A: Create `.env` file
```bash
cd /Users/nirbanbiswas/Desktop/100x/code/creatorpulse
echo "GROQ_API_KEY=gsk_YOUR_KEY_HERE" > .env
```

Option B: Copy from example
```bash
cp .env.example .env
# Then edit .env and paste your Groq API key
```

### Step 3: Run Enhanced App

```bash
# Kill old app first
pkill -f "streamlit run"

# Install new dependencies
pip install groq streamlit-shadcn-ui

# Run enhanced version
streamlit run app_enhanced.py
```

Or use the original app (also updated with Groq):
```bash
streamlit run app.py
```

## Features in Enhanced App

### 🎨 Shadcn UI Components
- Modern card layouts
- Enhanced metrics display
- Better buttons and badges
- Sleek provider selection

### ⚡ LLM Provider Switching
- Toggle between Groq, OpenAI, Claude
- See which provider generated each draft
- Track provider usage stats

### 🚀 Groq-Specific Benefits
- **Speed**: Drafts generated in 2-3 seconds (vs 10-20s)
- **Free**: No API costs during testing
- **Quality**: Llama 3.1 70B rivals GPT-4

## Comparison

| Feature | Groq (FREE) | OpenAI (Paid) | Claude (Paid) |
|---------|-------------|---------------|---------------|
| Speed | ⚡⚡⚡ 2-3s | ⚡ 10-15s | ⚡⚡ 5-8s |
| Cost | FREE | $0.03/draft | $0.02/draft |
| Quality | 🌟🌟🌟🌟 | 🌟🌟🌟🌟🌟 | 🌟🌟🌟🌟🌟 |
| Rate Limit | 30/min | 500/min | 50/min |
| Setup | Easy | Medium | Medium |

## Testing the Enhanced App

1. **Home Page** - See improved layout with better metrics
2. **Provider Selection** - Click Groq/OpenAI/Claude buttons in sidebar
3. **Style Trainer** - Train with Groq (fast!)
4. **Generate** - Create drafts in seconds
5. **Dashboard** - See provider usage stats

## Troubleshooting

### "No module named 'groq'"
```bash
pip install groq
```

### "No module named 'streamlit_shadcn_ui'"
```bash
pip install streamlit-shadcn-ui
```

### API Key Not Working
- Make sure `.env` file is in project root
- Check key starts with `gsk_`
- Try creating a new key
- Verify no extra spaces in `.env`

### App Shows Original UI
- Make sure you're running `app_enhanced.py`
- Check that shadcn-ui is installed
- Restart the app

## Advanced: Using Groq in Code

```python
from groq import Groq
import os

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a newsletter about AI"}
    ],
    temperature=0.7,
    max_tokens=3000
)

print(response.choices[0].message.content)
```

## Available Groq Models

- **llama-3.1-70b-versatile** (Recommended - Best balance)
- **llama-3.1-8b-instant** (Fastest - Good for quick tasks)
- **mixtral-8x7b-32768** (Long context - Up to 32K tokens)
- **gemma-7b-it** (Lightweight - Fast responses)

## Rate Limits (Free Tier)

- **Requests**: 30 per minute
- **Tokens**: 6,000 per minute
- **Daily**: No hard limit
- **Concurrent**: 10 requests

For CreatorPulse, this is MORE than enough!

## Upgrade Path

If you need more:
1. **Free**: 30 req/min (enough for 100+ drafts/day)
2. **Paid**: Contact Groq for higher limits
3. **Hybrid**: Use Groq for dev, GPT-4 for production

## Next Steps

1. ✅ Get Groq API key (2 min)
2. ✅ Add to `.env` file
3. ✅ Run enhanced app
4. ✅ Generate your first draft
5. 🎉 Enjoy lightning-fast AI!

---

**Questions?**
- Groq Docs: https://console.groq.com/docs
- Groq Discord: https://groq.com/discord
- CreatorPulse Issues: See main README.md

**Fun Fact**: Groq uses custom LPU (Language Processing Units) instead of GPUs, making it incredibly fast!
