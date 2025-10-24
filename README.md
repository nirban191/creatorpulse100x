---
title: CreatorPulse
emoji: 📰
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 📰 CreatorPulse - AI Newsletter Curator

> Transform newsletter creation from hours to minutes using AI-powered automation

An intelligent newsletter automation platform that aggregates content from multiple sources, detects trends, and generates voice-matched newsletter drafts using state-of-the-art AI models.

[![Live Demo](https://img.shields.io/badge/🚀-Live%20Demo-blue?style=for-the-badge)](https://huggingface.co/spaces/nirban191/creatorpulse)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/nirban191/creatorpulse100x)

---

## ✨ Key Features

### 🤖 **AI-Powered Generation**
- 10 cutting-edge AI models (Llama 3.3, Llama 3.1, Mixtral, Gemma 2)
- Voice-matched drafts that sound like you
- Automated trend detection and topic analysis

### 🔗 **Multi-Source Aggregation**
- Twitter/X handles monitoring
- YouTube channel tracking
- Newsletter RSS feed integration

### 🎨 **Modern UI/UX**
- Sleek, modern interface with animated gradients
- Seamless guided onboarding workflow
- Responsive design with glassmorphism effects

### 🔐 **Enterprise Features**
- Secure authentication with Supabase
- Database persistence (PostgreSQL)
- Email delivery via Resend
- Morning delivery scheduling

---

## 🚀 Quick Start

### Option 1: Live Demo (Recommended)
Visit **[huggingface.co/spaces/nirban191/creatorpulse](https://huggingface.co/spaces/nirban191/creatorpulse)**

1. Click **"Get Started"** or use **Demo Mode**
2. Follow the guided workflow to:
   - Connect your content sources
   - Train your writing style
   - Generate your first newsletter

### Option 2: Local Setup

```bash
# Clone the repository
git clone https://github.com/nirban191/creatorpulse100x.git
cd creatorpulse100x

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_enhanced.py
```

---

## 🔑 Required API Keys

All services offer free tiers:

| Service | Purpose | Get Key |
|---------|---------|---------|
| **Groq** | AI Model Inference | [console.groq.com/keys](https://console.groq.com/keys) |
| **Supabase** | Auth + Database | [supabase.com](https://supabase.com) |
| **Resend** | Email Delivery (Optional) | [resend.com](https://resend.com) |

### Configuration
Add your API keys in the app settings or create a `.env` file:

```env
GROQ_API_KEY=your_groq_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
RESEND_API_KEY=your_resend_key_here  # Optional
```

---

## 📁 Project Structure

```
creatorpulse/
├── app_enhanced.py          # Main Streamlit application
├── pages/                   # Streamlit pages
│   ├── 1_🔐_Login.py
│   └── 2_📝_Signup.py
├── utils/                   # Core utilities
│   ├── auth.py             # Authentication manager
│   ├── llm_generator.py    # AI generation logic
│   ├── content_aggregator.py
│   ├── trend_detector.py
│   ├── email_sender.py
│   └── supabase_client.py
├── docs/                    # Documentation
│   ├── SETUP_GUIDE.md
│   ├── GROQ_SETUP_GUIDE.md
│   ├── SUPABASE_SETUP_GUIDE.md
│   └── ARCHITECTURE.md
├── scripts/                 # Automation scripts
│   └── send_scheduled_newsletters.py
├── database/                # Database schemas
└── demo_newsletters/        # Example training data
```

---

## 🛠️ Tech Stack

**Frontend:**
- Streamlit 1.40.1 (Python web framework)
- Custom CSS with glassmorphism and animated gradients

**AI/ML:**
- Groq API (Lightning-fast inference)
- Llama 3.3 70B, Llama 3.1 (70B/8B), Mixtral 8x7B, Gemma 2 9B

**Backend:**
- Python 3.9+
- Supabase (PostgreSQL + Auth)
- Resend (Email delivery)

**Deployment:**
- Docker
- Hugging Face Spaces
- GitHub Actions (CI/CD ready)

---

## 📖 Documentation

Comprehensive guides available in the [`docs/`](./docs/) directory:

- **[Setup Guide](./docs/SETUP_GUIDE.md)** - Complete installation instructions
- **[Groq Setup](./docs/GROQ_SETUP_GUIDE.md)** - AI model configuration
- **[Supabase Setup](./docs/SUPABASE_SETUP_GUIDE.md)** - Database & auth setup
- **[Resend Setup](./docs/RESEND_SETUP_GUIDE.md)** - Email delivery configuration
- **[Architecture](./docs/ARCHITECTURE.md)** - System design and components
- **[Deployment Guide](./docs/HUGGINGFACE_DEPLOYMENT.md)** - HF Spaces deployment

---

## 🎯 How It Works

1. **Content Aggregation**: CreatorPulse monitors your connected sources (Twitter, YouTube, RSS feeds) and aggregates the latest content

2. **Trend Detection**: AI analyzes aggregated content to identify emerging topics, trending themes, and key insights

3. **Style Learning**: Upload your past newsletters to train the AI on your unique writing voice, tone, and structure

4. **Draft Generation**: AI generates newsletter drafts that match your style with 70%+ ready-to-send accuracy

5. **Review & Send**: Review the generated draft, make any final tweaks, and deliver to your audience via email

---

## 🌟 Features in Detail

### Seamless Onboarding
- Click "Get Started" to begin guided workflow
- Smart "Continue" buttons that appear when requirements are met
- Automatic navigation through setup steps

### AI Model Selection
- Choose from 10 different AI models
- Real-time model switching
- Optimized for speed and quality

### Writing Style Training
- Upload past newsletters (TXT, CSV)
- Paste content directly
- AI learns tone, voice, structure, and sentence style

### Content Sources
- **Twitter/X**: Monitor handles and hashtags
- **YouTube**: Track channel updates
- **RSS Feeds**: Aggregate newsletter content

### Dashboard & Analytics
- Track connected sources
- Monitor drafts generated
- View style training status

---

## 🚧 Roadmap

- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Integration with more content platforms (LinkedIn, Medium, Substack)
- [ ] A/B testing for newsletter variants
- [ ] Automated scheduling and delivery
- [ ] Collaborative editing features

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** for lightning-fast AI inference
- **Supabase** for robust auth and database services
- **Resend** for reliable email delivery
- **Hugging Face** for free hosting and deployment

---

## 📧 Contact & Support

- **Live Demo**: [huggingface.co/spaces/nirban191/creatorpulse](https://huggingface.co/spaces/nirban191/creatorpulse)
- **GitHub**: [github.com/nirban191/creatorpulse100x](https://github.com/nirban191/creatorpulse100x)
- **Issues**: [GitHub Issues](https://github.com/nirban191/creatorpulse100x/issues)

---

<p align="center">
  <strong>Built with ❤️ using Groq AI + Supabase + Resend</strong>
</p>

<p align="center">
  <sub>Made by <a href="https://github.com/nirban191">@nirban191</a></sub>
</p>
