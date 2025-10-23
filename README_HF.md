---
title: CreatorPulse
emoji: 📰
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.32.0"
app_file: app_enhanced.py
pinned: false
license: mit
---

# 📰 CreatorPulse - AI Newsletter Curator

An intelligent newsletter automation platform powered by Groq AI, featuring user authentication, database persistence, and email delivery.

## 🚀 Features

- **🤖 AI Generation**: 5 Groq models (Llama 3.1 70B/8B, Mixtral, Gemma)
- **🔐 User Auth**: Secure login/signup with Supabase
- **💾 Database**: Persistent storage with PostgreSQL
- **📧 Email**: Newsletter delivery via Resend
- **✍️ Style Training**: Learn from your past newsletters
- **🔗 Multi-Source**: Twitter, YouTube, RSS aggregation

## 🎯 Quick Start

1. **Sign Up** or use **Demo Mode**
2. **Add Sources** - Connect Twitter handles, YouTube channels
3. **Train Style** - Upload past newsletters
4. **Generate** - AI creates personalized newsletters
5. **Send** - Deliver via email

## 🔑 API Keys (Add in Settings)

This app requires API keys (all have free tiers):

- **GROQ_API_KEY**: Get free at [console.groq.com](https://console.groq.com/keys)
- **SUPABASE_URL & KEY**: Free tier at [supabase.com](https://supabase.com)
- **RESEND_API_KEY**: Optional, for emails at [resend.com](https://resend.com)

## 📚 Documentation

- Full documentation in repository
- Setup guides for each integration
- API configuration instructions

## 🛠️ Tech Stack

- Streamlit
- Groq API (Llama 3.1, Mixtral, Gemma)
- Supabase (Auth + Database)
- Resend (Email)
- Python 3.9+

## 📖 Repository

[GitHub Repository](https://github.com/nirban191/creatorpulse100x)

---

Built with ❤️ using Groq AI + Supabase + Resend
