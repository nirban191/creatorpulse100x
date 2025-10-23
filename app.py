import streamlit as st

# Page configuration
st.set_page_config(
    page_title="CreatorPulse - Newsletter Curator",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'sources' not in st.session_state:
    st.session_state.sources = {
        'twitter': [],
        'youtube': [],
        'newsletters': []
    }

if 'style_trained' not in st.session_state:
    st.session_state.style_trained = False

if 'generated_drafts' not in st.session_state:
    st.session_state.generated_drafts = []

if 'user_feedback' not in st.session_state:
    st.session_state.user_feedback = []

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #6366f1;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .feature-card {
        background: #1e293b;
        padding: 2rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
        height: 100%;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("# 📰 CreatorPulse")
    st.markdown("---")

    st.markdown("### Navigation")
    page = st.radio(
        "Go to",
        ["Home", "Source Connections", "Style Trainer", "Generate Newsletter", "Dashboard"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Quick Stats")
    st.metric("Connected Sources", len(st.session_state.sources['twitter']) +
              len(st.session_state.sources['youtube']) +
              len(st.session_state.sources['newsletters']))
    st.metric("Drafts Generated", len(st.session_state.generated_drafts))
    st.metric("Style Trained", "Yes" if st.session_state.style_trained else "No")

# Main content
if page == "Home":
    st.markdown('<h1 class="main-header">CreatorPulse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-powered newsletter curator and drafting assistant</p>', unsafe_allow_html=True)

    # Hero section
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### Welcome to CreatorPulse

        CreatorPulse helps content creators and curators save time by:
        - Aggregating insights from multiple sources (Twitter, YouTube, Newsletters)
        - Detecting emerging trends automatically
        - Generating voice-matched newsletter drafts
        - Delivering curated content every morning

        **Get started in 3 simple steps:**
        1. Connect your content sources
        2. Train your writing style
        3. Generate your first newsletter draft
        """)

        if st.button("Get Started", use_container_width=True, type="primary"):
            st.info("Navigate to 'Source Connections' in the sidebar to begin!")

    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<p class="stat-label">Time Saved</p>', unsafe_allow_html=True)
        st.markdown('<p class="stat-value">2-3 hours</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8;">per newsletter</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<p class="stat-label">Target Draft Time</p>', unsafe_allow_html=True)
        st.markdown('<p class="stat-value">&lt; 20 min</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8;">review & send</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Features section
    st.markdown("### Core Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔗</div>
            <h4>Multi-Source Aggregation</h4>
            <p>Connect Twitter handles, YouTube channels, and newsletter RSS feeds to aggregate content from all your trusted sources.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h4>Trend Detection</h4>
            <p>AI-powered trend analysis surfaces emerging topics and insights automatically, so you never miss what matters.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✍️</div>
            <h4>Voice-Matched Drafts</h4>
            <p>Upload your past newsletters to train the AI on your unique writing style for 70%+ ready-to-send drafts.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Getting started guide
    with st.expander("Quick Start Guide", expanded=False):
        st.markdown("""
        #### Step 1: Connect Your Sources
        Navigate to **Source Connections** and add:
        - Twitter handles or hashtags you follow
        - YouTube channels you watch
        - Newsletter RSS feeds you subscribe to

        #### Step 2: Train Your Writing Style
        Go to **Style Trainer** and:
        - Upload at least 20 of your past newsletters
        - The AI will learn your voice, tone, and structure

        #### Step 3: Generate Your First Draft
        Visit **Generate Newsletter** to:
        - Select your topics and time range
        - Generate an AI-powered draft
        - Review and edit in under 20 minutes

        #### Step 4: Monitor Performance
        Check the **Dashboard** for:
        - Engagement analytics
        - Draft acceptance rates
        - Time savings metrics
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p>Built with Streamlit - Powered by AI</p>
        <p style="font-size: 0.8rem;">CreatorPulse v1.0 MVP</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Source Connections":
    # Source Connections page
    st.title("🔗 Source Connections")
    st.markdown("Connect your content sources to start curating your newsletter.")

    tab1, tab2, tab3 = st.tabs(["Twitter", "YouTube", "Newsletters"])

    with tab1:
        st.markdown("### Twitter Sources")
        st.markdown("Add Twitter handles or hashtags to monitor")

        twitter_handle = st.text_input("Enter Twitter handle (without @)", key="twitter_input")
        if st.button("Add Twitter Source", key="add_twitter"):
            if twitter_handle:
                st.session_state.sources['twitter'].append(twitter_handle)
                st.success(f"Added @{twitter_handle}")
                st.rerun()

        if st.session_state.sources['twitter']:
            st.markdown("#### Connected Twitter Sources")
            for idx, handle in enumerate(st.session_state.sources['twitter']):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"@{handle}")
                with col2:
                    if st.button("Remove", key=f"remove_twitter_{idx}"):
                        st.session_state.sources['twitter'].pop(idx)
                        st.rerun()

    with tab2:
        st.markdown("### YouTube Channels")
        st.markdown("Add YouTube channel IDs or names to monitor")

        youtube_channel = st.text_input("Enter YouTube channel", key="youtube_input")
        if st.button("Add YouTube Source", key="add_youtube"):
            if youtube_channel:
                st.session_state.sources['youtube'].append(youtube_channel)
                st.success(f"Added {youtube_channel}")
                st.rerun()

        if st.session_state.sources['youtube']:
            st.markdown("#### Connected YouTube Channels")
            for idx, channel in enumerate(st.session_state.sources['youtube']):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(channel)
                with col2:
                    if st.button("Remove", key=f"remove_youtube_{idx}"):
                        st.session_state.sources['youtube'].pop(idx)
                        st.rerun()

    with tab3:
        st.markdown("### Newsletter RSS Feeds")
        st.markdown("Add RSS feed URLs from newsletters you follow")

        newsletter_url = st.text_input("Enter RSS feed URL", key="newsletter_input")
        if st.button("Add Newsletter Source", key="add_newsletter"):
            if newsletter_url:
                st.session_state.sources['newsletters'].append(newsletter_url)
                st.success(f"Added newsletter feed")
                st.rerun()

        if st.session_state.sources['newsletters']:
            st.markdown("#### Connected Newsletter Feeds")
            for idx, url in enumerate(st.session_state.sources['newsletters']):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(url)
                with col2:
                    if st.button("Remove", key=f"remove_newsletter_{idx}"):
                        st.session_state.sources['newsletters'].pop(idx)
                        st.rerun()

elif page == "Style Trainer":
    st.title("✍️ Writing Style Trainer")
    st.markdown("Upload your past newsletters to train the AI on your unique writing style.")

    st.info("For best results, upload at least 20 past newsletters or blog posts that represent your writing style.")

    uploaded_files = st.file_uploader(
        "Upload your past newsletters (TXT, CSV, or paste content)",
        type=["txt", "csv"],
        accept_multiple_files=True
    )

    text_input = st.text_area(
        "Or paste your newsletter content here:",
        height=300,
        placeholder="Paste multiple newsletters separated by ---"
    )

    if st.button("Train Writing Style", type="primary"):
        if uploaded_files or text_input:
            with st.spinner("Training your writing style..."):
                # Simulate training process
                import time
                time.sleep(2)
                st.session_state.style_trained = True
                st.success("Writing style trained successfully! The AI has learned your voice.")
                st.balloons()
        else:
            st.error("Please upload files or paste content to train your style.")

    if st.session_state.style_trained:
        st.success("✅ Your writing style has been trained!")
        st.markdown("""
        **Style Characteristics Learned:**
        - Tone: Professional yet conversational
        - Structure: Clear sections with engaging introductions
        - Length: Medium-form content (500-800 words)
        - Voice: First-person perspective with direct audience engagement
        """)

elif page == "Generate Newsletter":
    st.title("📝 Generate Newsletter")
    st.markdown("Generate an AI-powered newsletter draft based on your sources and style.")

    if not st.session_state.style_trained:
        st.warning("⚠️ Please train your writing style first for best results!")

    total_sources = (len(st.session_state.sources['twitter']) +
                    len(st.session_state.sources['youtube']) +
                    len(st.session_state.sources['newsletters']))

    if total_sources == 0:
        st.warning("⚠️ Please connect at least one content source first!")

    st.markdown("### Newsletter Configuration")

    col1, col2 = st.columns(2)

    with col1:
        newsletter_title = st.text_input("Newsletter Title", value="Weekly Digest")
        time_range = st.selectbox("Content Time Range", ["Last 24 hours", "Last 3 days", "Last week"])

    with col2:
        num_articles = st.slider("Number of articles to include", 3, 10, 5)
        include_trends = st.checkbox("Include trending topics", value=True)

    if st.button("Generate Newsletter Draft", type="primary", disabled=not st.session_state.style_trained or total_sources == 0):
        with st.spinner("Generating your newsletter draft..."):
            import time
            time.sleep(3)

            # Create sample draft
            draft = {
                'title': newsletter_title,
                'content': f"""
# {newsletter_title}

Hey there!

Welcome to this week's curated insights. I've been scanning through the latest updates from your trusted sources, and here are the most compelling stories and trends worth your attention.

## 🔥 Top Stories

### 1. AI Innovation Reaches New Heights
The latest developments in artificial intelligence continue to reshape our digital landscape. Key players in the tech industry are pushing boundaries with breakthrough applications.

**Why it matters:** This could fundamentally change how we approach creative work and automation.

### 2. Content Creator Economy Expands
More creators are finding sustainable revenue streams through diversified platforms and direct audience engagement.

**Key takeaway:** The shift toward creator-owned platforms is accelerating.

### 3. Remote Work Tools Evolution
New collaboration tools are making distributed teams more effective than ever before.

## 📊 Trending Topics

{f"- Emerging trend in AI-powered content curation" if include_trends else ""}
{f"- Growth of newsletter platforms" if include_trends else ""}
{f"- Evolution of social media algorithms" if include_trends else ""}

## 💡 Quick Takes

- Twitter buzz around new productivity tools
- YouTube creators sharing workflow optimizations
- Newsletter best practices from industry leaders

---

That's all for this week! Let me know what resonated with you.

Until next time,
[Your Name]
                """,
                'timestamp': time.time()
            }

            st.session_state.generated_drafts.append(draft)
            st.success("Newsletter draft generated successfully!")
            st.rerun()

    # Display generated drafts
    if st.session_state.generated_drafts:
        st.markdown("---")
        st.markdown("### Generated Drafts")

        for idx, draft in enumerate(reversed(st.session_state.generated_drafts)):
            with st.expander(f"Draft: {draft['title']}", expanded=(idx == 0)):
                st.markdown(draft['content'])

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Accept", key=f"accept_{idx}"):
                        st.session_state.user_feedback.append({'draft_id': idx, 'feedback': 'positive'})
                        st.success("Feedback recorded! This helps improve future drafts.")

                with col2:
                    if st.button("👎 Reject", key=f"reject_{idx}"):
                        st.session_state.user_feedback.append({'draft_id': idx, 'feedback': 'negative'})
                        st.info("Feedback recorded. Consider adjusting sources or style training.")

                with col3:
                    if st.button("📧 Export", key=f"export_{idx}"):
                        st.download_button(
                            "Download as TXT",
                            draft['content'],
                            file_name=f"{draft['title'].replace(' ', '_')}.txt",
                            key=f"download_{idx}"
                        )

elif page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Track your newsletter performance and usage metrics.")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Sources", len(st.session_state.sources['twitter']) +
                 len(st.session_state.sources['youtube']) +
                 len(st.session_state.sources['newsletters']))

    with col2:
        st.metric("Drafts Generated", len(st.session_state.generated_drafts))

    with col3:
        acceptance_rate = (len([f for f in st.session_state.user_feedback if f['feedback'] == 'positive']) /
                          max(len(st.session_state.user_feedback), 1) * 100)
        st.metric("Draft Acceptance", f"{acceptance_rate:.0f}%")

    with col4:
        est_time_saved = len(st.session_state.generated_drafts) * 2.5
        st.metric("Est. Time Saved", f"{est_time_saved:.1f}h")

    st.markdown("---")

    # Source breakdown
    st.markdown("### Connected Sources Breakdown")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Twitter", len(st.session_state.sources['twitter']))
        if st.session_state.sources['twitter']:
            for handle in st.session_state.sources['twitter'][:3]:
                st.write(f"- @{handle}")

    with col2:
        st.metric("YouTube", len(st.session_state.sources['youtube']))
        if st.session_state.sources['youtube']:
            for channel in st.session_state.sources['youtube'][:3]:
                st.write(f"- {channel}")

    with col3:
        st.metric("Newsletters", len(st.session_state.sources['newsletters']))
        if st.session_state.sources['newsletters']:
            st.write(f"- {len(st.session_state.sources['newsletters'])} RSS feeds")

    st.markdown("---")

    # Recent activity
    st.markdown("### Recent Activity")
    if st.session_state.generated_drafts:
        for idx, draft in enumerate(list(reversed(st.session_state.generated_drafts))[:5]):
            st.write(f"✅ Generated: {draft['title']}")
    else:
        st.info("No drafts generated yet. Visit 'Generate Newsletter' to create your first draft!")
