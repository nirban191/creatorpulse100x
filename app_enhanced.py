import streamlit as st
import time
import uuid
from utils.supabase_client import get_db
from utils.auth import AuthManager
from utils.llm_generator import NewsletterGenerator
from utils.content_aggregator import ContentAggregator
from utils.trend_detector import TrendDetector

# Initialize database and auth
db = get_db()
auth = AuthManager()

# Page configuration
st.set_page_config(
    page_title="CreatorPulse - Newsletter Curator",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication
if not auth.is_authenticated():
    st.warning("⚠️ Please login to access CreatorPulse")
    st.info("You will be redirected to the login page...")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔐 Login", use_container_width=True, type="primary"):
            st.switch_page("pages/1_🔐_Login.py")
    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.switch_page("pages/2_📝_Signup.py")
    with col3:
        if st.button("🎮 Demo Mode", use_container_width=True):
            # Enable demo mode without authentication
            st.session_state.demo_mode = True
            st.session_state.user_id = str(uuid.uuid4())
            st.session_state.user_email = 'demo@creatorpulse.com'
            st.rerun()

    if not st.session_state.get('demo_mode', False):
        st.stop()

# Get authenticated user or use demo
if auth.is_authenticated():
    user = auth.get_current_user()
    st.session_state.user_id = user['id']
    st.session_state.user_email = user['email']
else:
    # Demo mode - user chose to continue without auth
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.user_email = 'demo@creatorpulse.com'

# Always initialize llm_provider and model first (default)
if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = 'groq'

if 'groq_model' not in st.session_state:
    st.session_state.groq_model = 'llama-3.3-70b-versatile'  # Default to latest Llama 3.3

# Try to load user profile from database
if db.is_configured():
    try:
        profile = db.get_or_create_profile(st.session_state.user_id, st.session_state.user_email)
        if profile and profile.get('preferred_llm_provider'):
            st.session_state.llm_provider = profile.get('preferred_llm_provider')
    except Exception as e:
        # If database has RLS or other issues, just use default
        pass

# Initialize style_trained state
if 'style_trained' not in st.session_state:
    st.session_state.style_trained = False
    # Try to check if user has style training in database
    if db.is_configured():
        try:
            style_data = db.get_style_training(st.session_state.user_id)
            st.session_state.style_trained = len(style_data) > 0
        except Exception as e:
            # If database has issues, just use default
            pass

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
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("# 📰 CreatorPulse")
    st.markdown("---")

    # User info section
    if auth.is_authenticated():
        user = auth.get_current_user()
        st.success(f"👤 {user['email']}")
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()
    else:
        st.info("🎮 Demo Mode")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Login", use_container_width=True, key="sidebar_login"):
                st.switch_page("pages/1_🔐_Login.py")
        with col2:
            if st.button("📝 Sign Up", use_container_width=True, key="sidebar_signup"):
                st.switch_page("pages/2_📝_Signup.py")

    st.markdown("---")

    st.markdown("### Navigation")
    page = st.radio(
        "Go to",
        ["Home", "Source Connections", "Style Trainer", "Generate Newsletter", "Dashboard"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # LLM Provider Selection with shadcn badge
    st.markdown("### ⚡ LLM Provider")
    provider_col1, provider_col2, provider_col3 = st.columns(3)
    
    with provider_col1:
        if st.button("Groq", use_container_width=True, type="primary" if st.session_state.llm_provider == 'groq' else "secondary"):
            st.session_state.llm_provider = 'groq'
            st.rerun()
    
    with provider_col2:
        if st.button("OpenAI", use_container_width=True, type="primary" if st.session_state.llm_provider == 'openai' else "secondary"):
            st.session_state.llm_provider = 'openai'
            st.rerun()
    
    with provider_col3:
        if st.button("Claude", use_container_width=True, type="primary" if st.session_state.llm_provider == 'anthropic' else "secondary"):
            st.session_state.llm_provider = 'anthropic'
            st.rerun()
    
    # Show current provider badge and model selection
    if st.session_state.llm_provider == 'groq':
        st.success("🚀 Using Groq (Fast & Free!)")

        # Groq model selection - All models available via Groq's fast inference
        groq_models = {
            'llama-3.3-70b-versatile': '🌟 Llama 3.3 70B (Latest, Best)',
            'llama-3.1-70b-versatile': '🚀 Llama 3.1 70B (Fast, Reliable)',
            'llama-3.1-8b-instant': '⚡ Llama 3.1 8B (Instant)',
            'llama3-70b-8192': '🔥 Llama 3 70B (Long Context)',
            'mixtral-8x7b-32768': '🎯 Mixtral 8x7B (32K Context)',
            'gemma2-9b-it': '💎 Gemma 2 9B (Google)',
            'llama-3.2-90b-vision-preview': '👁️ Llama 3.2 90B Vision',
            'llama-3.2-11b-vision-preview': '📸 Llama 3.2 11B Vision',
            'llama-3.2-3b-preview': '⚡ Llama 3.2 3B (Ultra Fast)',
            'llama-3.2-1b-preview': '🏃 Llama 3.2 1B (Lightning)',
        }

        selected_model = st.selectbox(
            "Model",
            options=list(groq_models.keys()),
            format_func=lambda x: groq_models[x],
            index=list(groq_models.keys()).index(st.session_state.groq_model),
            key="groq_model_selector"
        )

        if selected_model != st.session_state.groq_model:
            st.session_state.groq_model = selected_model
            st.success(f"✅ Switched to {groq_models[selected_model]}")

    elif st.session_state.llm_provider == 'openai':
        st.info("🤖 Using OpenAI GPT-4")
    else:
        st.info("🎭 Using Anthropic Claude")

    st.markdown("---")
    st.markdown("### Quick Stats")

    # Get stats from database or fallback
    if db.is_configured():
        user_stats = db.get_user_stats(st.session_state.user_id)
        total_sources = user_stats.get('total_sources', 0)
        total_drafts = user_stats.get('total_drafts', 0)
    else:
        # Fallback to session state
        total_sources = (len(st.session_state.get('sources', {}).get('twitter', [])) +
                        len(st.session_state.get('sources', {}).get('youtube', [])) +
                        len(st.session_state.get('sources', {}).get('newsletters', [])))
        total_drafts = len(st.session_state.get('generated_drafts', []))

    st.metric("Connected Sources", total_sources)
    st.metric("Drafts Generated", total_drafts)
    st.metric("Style Trained", "Yes ✓" if st.session_state.style_trained else "No ✗")

# Main content
if page == "Home":
    st.markdown('<h1 class="main-header">CreatorPulse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-powered newsletter curator and drafting assistant</p>', unsafe_allow_html=True)

    # Hero section with shadcn cards
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

        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            st.info("Navigate to 'Source Connections' in the sidebar to begin!")

    with col2:
        # Stats cards
        st.markdown("### 📊 Quick Stats")
        st.metric(label="Time Saved", value="2-3 hours", delta="per newsletter")
        st.metric(label="Target Draft Time", value="< 20 min", delta="review & send")
        st.metric(label="Draft Acceptance", value="≥70%", delta="target rate")

    st.markdown("---")

    # Features section with enhanced cards
    st.markdown("### Core Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container():
            st.markdown("#### 🔗 Multi-Source Aggregation")
            st.write("Connect Twitter handles, YouTube channels, and newsletter RSS feeds to aggregate content from all your trusted sources.")

    with col2:
        with st.container():
            st.markdown("#### 🎯 Trend Detection")
            st.write("AI-powered trend analysis surfaces emerging topics and insights automatically, so you never miss what matters.")

    with col3:
        with st.container():
            st.markdown("#### ✍️ Voice-Matched Drafts")
            st.write("Upload your past newsletters to train the AI on your unique writing style for 70%+ ready-to-send drafts.")

elif page == "Source Connections":
    st.title("🔗 Source Connections")
    st.markdown("Connect your content sources to start curating your newsletter.")

    tab1, tab2, tab3 = st.tabs(["Twitter", "YouTube", "Newsletters"])

    with tab1:
        st.markdown("### Twitter Sources")
        st.markdown("Add Twitter handles or hashtags to monitor")

        twitter_handle = st.text_input("Enter Twitter handle (without @)", key="twitter_input")
        if st.button("Add Twitter Source", key="add_twitter", type="primary"):
            if twitter_handle:
                if db.is_configured():
                    # Ensure profile exists before adding source
                    try:
                        db.get_or_create_profile(st.session_state.user_id, st.session_state.user_email)
                    except Exception as e:
                        st.error(f"❌ Please run the database fix script first. Error: {str(e)}")
                        st.info("See FIX_DATABASE_WARNING.md for instructions")
                        st.stop()

                    result = db.add_source(st.session_state.user_id, 'twitter', twitter_handle)
                    if result.get('success'):
                        st.success(f"✅ Added @{twitter_handle}")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        error_msg = result.get('error', 'Unknown error')
                        st.error(f"❌ Error: {error_msg}")
                        if 'violates foreign key constraint' in str(error_msg) or 'row-level security' in str(error_msg).lower():
                            st.error("🔧 Database needs RLS disabled. Run the SQL script from database/quick_fix_rls.sql")
                else:
                    st.warning("⚠️ Database not configured. Source not saved.")

        # Get Twitter sources from database
        twitter_sources = []
        if db.is_configured():
            twitter_sources = db.get_sources(st.session_state.user_id, 'twitter')

        if twitter_sources:
            st.markdown("#### Connected Twitter Sources")
            for source in twitter_sources:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"@{source['identifier']}")
                with col2:
                    if st.button("Remove", key=f"remove_twitter_{source['id']}"):
                        if db.delete_source(st.session_state.user_id, source['id']):
                            st.success("Removed!")
                            time.sleep(0.3)
                            st.rerun()

    with tab2:
        st.markdown("### YouTube Channels")
        st.markdown("Add YouTube channel IDs or names to monitor")

        youtube_channel = st.text_input("Enter YouTube channel", key="youtube_input")
        if st.button("Add YouTube Source", key="add_youtube", type="primary"):
            if youtube_channel:
                if db.is_configured():
                    result = db.add_source(st.session_state.user_id, 'youtube', youtube_channel)
                    if result.get('success'):
                        st.success(f"✅ Added {youtube_channel}")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                else:
                    st.warning("⚠️ Database not configured. Source not saved.")

        # Get YouTube sources from database
        youtube_sources = []
        if db.is_configured():
            youtube_sources = db.get_sources(st.session_state.user_id, 'youtube')

        if youtube_sources:
            st.markdown("#### Connected YouTube Channels")
            for source in youtube_sources:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(source['identifier'])
                with col2:
                    if st.button("Remove", key=f"remove_youtube_{source['id']}"):
                        if db.delete_source(st.session_state.user_id, source['id']):
                            st.success("Removed!")
                            time.sleep(0.3)
                            st.rerun()

    with tab3:
        st.markdown("### Newsletter RSS Feeds")
        st.markdown("Add RSS feed URLs from newsletters you follow")

        newsletter_url = st.text_input("Enter RSS feed URL", key="newsletter_input")
        if st.button("Add Newsletter Source", key="add_newsletter", type="primary"):
            if newsletter_url:
                if db.is_configured():
                    result = db.add_source(st.session_state.user_id, 'newsletter', newsletter_url)
                    if result.get('success'):
                        st.success(f"✅ Added newsletter feed")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                else:
                    st.warning("⚠️ Database not configured. Source not saved.")

        # Get Newsletter sources from database
        newsletter_sources = []
        if db.is_configured():
            newsletter_sources = db.get_sources(st.session_state.user_id, 'newsletter')

        if newsletter_sources:
            st.markdown("#### Connected Newsletter Feeds")
            for source in newsletter_sources:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(source['identifier'])
                with col2:
                    if st.button("Remove", key=f"remove_newsletter_{source['id']}"):
                        if db.delete_source(st.session_state.user_id, source['id']):
                            st.success("Removed!")
                            time.sleep(0.3)
                            st.rerun()

elif page == "Style Trainer":
    st.title("✍️ Writing Style Trainer")
    st.markdown("Upload your past newsletters to train the AI on your unique writing style.")

    # Provider info
    if st.session_state.llm_provider == 'groq':
        st.info("🚀 Using Groq (Llama 3.1 70B) - Lightning fast and free!")
    elif st.session_state.llm_provider == 'openai':
        st.info("🤖 Using OpenAI GPT-4 - Requires API key")
    else:
        st.info("🎭 Using Anthropic Claude 3 - Requires API key")

    st.markdown("For best results, upload at least 20 past newsletters or blog posts that represent your writing style.")

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

    if st.button("🎯 Train Writing Style", type="primary", use_container_width=True):
        if uploaded_files or text_input:
            with st.spinner(f"Training your writing style using {st.session_state.llm_provider.upper()}..."):
                # Collect training text
                training_text = text_input if text_input else ""
                if uploaded_files:
                    for file in uploaded_files:
                        content = file.read().decode('utf-8')
                        training_text += "\n---\n" + content

                # Save to database
                if db.is_configured():
                    success = db.save_style_training(
                        st.session_state.user_id,
                        training_text,
                        {'provider': st.session_state.llm_provider}
                    )
                    if success:
                        st.session_state.style_trained = True
                        st.success("✅ Writing style trained and saved to database!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to save style training to database")
                else:
                    st.session_state.style_trained = True
                    st.warning("⚠️ Database not configured. Style training not persisted.")
                    st.success("✅ Writing style trained temporarily!")
        else:
            st.error("❌ Please upload files or paste content to train your style.")

    if st.session_state.style_trained:
        st.success("✅ Your writing style has been trained!")
        with st.expander("📊 Style Characteristics Learned", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Tone:** Professional yet conversational
                
                **Voice:** First-person with direct audience engagement
                """)
            with col2:
                st.markdown("""
                **Structure:** Clear sections with engaging introductions
                
                **Sentence Style:** Varied length with punchy key points
                """)

elif page == "Generate Newsletter":
    st.title("📝 Generate Newsletter")
    st.markdown("Generate an AI-powered newsletter draft based on your sources and style.")

    if not st.session_state.style_trained:
        st.warning("⚠️ Please train your writing style first for best results!")

    # Get total sources from database
    if db.is_configured():
        user_stats = db.get_user_stats(st.session_state.user_id)
        total_sources = user_stats.get('total_sources', 0)
    else:
        total_sources = 0

    if total_sources == 0:
        st.warning("⚠️ Please connect at least one content source first!")

    # Provider selection reminder
    st.info(f"🤖 Current LLM: **{st.session_state.llm_provider.upper()}** | Change in sidebar")

    st.markdown("### Newsletter Configuration")

    col1, col2 = st.columns(2)

    with col1:
        newsletter_title = st.text_input("Newsletter Title", value="Weekly Digest")
        time_range = st.selectbox("Content Time Range", ["Last 24 hours", "Last 3 days", "Last week"])

    with col2:
        num_articles = st.slider("Number of articles to include", 3, 10, 5)
        include_trends = st.checkbox("Include trending topics", value=True)

    if st.button("🚀 Generate Newsletter Draft", type="primary", use_container_width=True,
                 disabled=not st.session_state.style_trained or total_sources == 0):
        with st.spinner(f"Generating your newsletter draft with {st.session_state.llm_provider.upper()}..."):
            start_time = time.time()

            try:
                # Get sources for content aggregation
                aggregated_content = []
                if db.is_configured():
                    sources = db.get_sources(st.session_state.user_id)
                    # Create mock content based on sources
                    for source in sources:
                        aggregated_content.append({
                            'title': f"Latest from {source['identifier']}",
                            'source_type': source['source_type'],
                            'identifier': source['identifier']
                        })

                # Initialize newsletter generator with selected model
                generator = NewsletterGenerator(
                    provider=st.session_state.llm_provider,
                    model=st.session_state.get('groq_model', 'llama-3.1-70b-versatile') if st.session_state.llm_provider == 'groq' else None
                )

                # Get style training if available
                style_profile = None
                if db.is_configured():
                    style_data = db.get_style_training(st.session_state.user_id)
                    if style_data:
                        style_profile = {'training_text': style_data[0].get('training_text', '')}

                # Detect trending topics if enabled
                trending_data = None
                if include_trends and aggregated_content:
                    trend_detector = TrendDetector(db if db.is_configured() else None)
                    trending_data = trend_detector.get_trending_topics(
                        aggregated_content,
                        include_spikes=True,
                        top_n=5
                    )

                # Generate newsletter using AI
                content = generator.generate_newsletter(
                    content_items=aggregated_content,
                    title=newsletter_title,
                    style_profile=style_profile,
                    num_articles=num_articles,
                    include_trends=include_trends
                )

                # Prepend trending topics section if available
                if trending_data and trending_data.get('trending_keywords'):
                    trends_section = trend_detector.format_trends_for_newsletter(trending_data, max_trends=5)
                    content = trends_section + "\n\n" + content

                generation_time_ms = int((time.time() - start_time) * 1000)

            except Exception as e:
                st.error(f"❌ AI Generation Failed: {str(e)}")
                st.error("Please check your API keys and try again.")

                # Show helpful error messages
                if "api" in str(e).lower() or "key" in str(e).lower():
                    st.warning("⚠️ API Key Issue - Make sure your GROQ_API_KEY is set in .env file")
                    st.info("Get your free API key at: https://console.groq.com/keys")
                elif "rate" in str(e).lower() or "limit" in str(e).lower():
                    st.warning("⚠️ Rate Limit Reached - Please wait a moment and try again")
                else:
                    st.info("💡 Try: Check your internet connection, verify API keys, or switch models")

                st.stop()  # Stop execution instead of using fallback

            # Save to database
            if db.is_configured():
                result = db.save_draft(
                    st.session_state.user_id,
                    newsletter_title,
                    content,
                    st.session_state.llm_provider,
                    generation_time_ms
                )
                if result.get('success'):
                    st.success("✅ Newsletter draft generated and saved to database!")
                else:
                    st.error(f"❌ Error saving draft: {result.get('error', 'Unknown error')}")
            else:
                st.warning("⚠️ Database not configured. Draft not saved.")
                st.success("✅ Newsletter draft generated!")

            st.rerun()

    # Display generated drafts from database
    drafts = []
    if db.is_configured():
        drafts = db.get_drafts(st.session_state.user_id, limit=10)

    if drafts:
        st.markdown("---")
        st.markdown("### Generated Drafts")

        for idx, draft in enumerate(drafts):
            draft_id = draft['id']
            with st.expander(f"Draft: {draft['title']} (via {draft.get('llm_provider', 'unknown').upper()})", expanded=(idx == 0)):
                st.markdown(draft['content'])

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("👍 Accept", key=f"accept_{draft_id}"):
                        if db.is_configured():
                            db.add_feedback(st.session_state.user_id, draft_id, 'positive')
                        st.success("✅ Feedback recorded!")

                with col2:
                    if st.button("👎 Reject", key=f"reject_{draft_id}"):
                        if db.is_configured():
                            db.add_feedback(st.session_state.user_id, draft_id, 'negative')
                        st.info("📝 Feedback recorded.")

                with col3:
                    st.download_button(
                        "📥 Export",
                        draft['content'],
                        file_name=f"{draft['title'].replace(' ', '_')}.txt",
                        key=f"download_{draft_id}"
                    )

                with col4:
                    if st.button("📧 Send Email", key=f"email_{draft_id}"):
                        st.session_state[f'show_email_form_{draft_id}'] = True
                        st.rerun()

                # Email sending form
                if st.session_state.get(f'show_email_form_{draft_id}', False):
                    st.markdown("---")
                    st.markdown("#### 📧 Send Newsletter via Email")

                    from utils.email_sender import NewsletterEmailSender
                    sender = NewsletterEmailSender()

                    if not sender.validate_api_key():
                        st.warning("⚠️ Resend API key not configured. Add RESEND_API_KEY to your .env file.")
                        st.markdown("[Get free Resend API key →](https://resend.com/api-keys)")
                    else:
                        email_col1, email_col2 = st.columns(2)

                        with email_col1:
                            recipient_emails = st.text_area(
                                "Recipient Email(s)",
                                placeholder="email@example.com\nanother@example.com",
                                help="Enter one email per line",
                                key=f"recipient_{draft_id}"
                            )

                            from_email = st.text_input(
                                "From Email",
                                value="CreatorPulse <newsletter@resend.dev>",
                                help="Must use verified domain with Resend",
                                key=f"from_{draft_id}"
                            )

                        with email_col2:
                            email_subject = st.text_input(
                                "Subject Line",
                                value=draft['title'],
                                key=f"subject_{draft_id}"
                            )

                            send_test = st.checkbox(
                                "Send as test email",
                                help="Adds [TEST] prefix to subject",
                                key=f"test_{draft_id}"
                            )

                        send_col1, send_col2 = st.columns([1, 3])

                        with send_col1:
                            if st.button("📤 Send Now", type="primary", key=f"send_btn_{draft_id}"):
                                if recipient_emails.strip():
                                    emails_list = [email.strip() for email in recipient_emails.split('\n') if email.strip()]

                                    with st.spinner("Sending email..."):
                                        if send_test and len(emails_list) == 1:
                                            result = sender.send_test_email(
                                                test_email=emails_list[0],
                                                subject=email_subject,
                                                content=draft['content'],
                                                from_email=from_email
                                            )
                                        else:
                                            result = sender.send_newsletter(
                                                to_emails=emails_list,
                                                subject=email_subject,
                                                content=draft['content'],
                                                from_email=from_email
                                            )

                                        if result['success']:
                                            # Log email send to database
                                            if db.is_configured():
                                                db.log_email_send(
                                                    st.session_state.user_id,
                                                    draft_id,
                                                    emails_list,
                                                    email_subject,
                                                    result.get('email_id')
                                                )
                                            st.success(f"✅ {result['message']}")
                                            st.balloons()
                                            st.session_state[f'show_email_form_{draft_id}'] = False
                                            time.sleep(2)
                                            st.rerun()
                                        else:
                                            st.error(f"❌ {result['message']}")
                                else:
                                    st.error("Please enter at least one email address")

                        with send_col2:
                            if st.button("Cancel", key=f"cancel_{draft_id}"):
                                st.session_state[f'show_email_form_{draft_id}'] = False
                                st.rerun()

elif page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Track your newsletter performance and usage metrics.")

    # Get user stats from database
    if db.is_configured():
        user_stats = db.get_user_stats(st.session_state.user_id)
        total_sources = user_stats.get('total_sources', 0)
        total_drafts = user_stats.get('total_drafts', 0)
        acceptance_rate = user_stats.get('acceptance_rate', 0)
        est_time_saved = user_stats.get('estimated_hours_saved', 0)
    else:
        total_sources = 0
        total_drafts = 0
        acceptance_rate = 0
        est_time_saved = 0
        st.warning("⚠️ Database not configured. Stats unavailable.")

    # Key metrics with enhanced display
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Sources", total_sources, delta=f"+{total_sources}" if total_sources > 0 else None)

    with col2:
        st.metric("Drafts Generated", total_drafts)

    with col3:
        st.metric("Draft Acceptance", f"{acceptance_rate:.0f}%",
                 delta="Good" if acceptance_rate >= 70 else "Needs improvement")

    with col4:
        st.metric("Est. Time Saved", f"{est_time_saved:.1f}h")

    st.markdown("---")

    # Provider usage stats
    if db.is_configured():
        drafts = db.get_drafts(st.session_state.user_id, limit=100)
        if drafts:
            st.markdown("### 🤖 LLM Provider Usage")
            providers = {}
            for draft in drafts:
                provider = draft.get('llm_provider', 'unknown')
                providers[provider] = providers.get(provider, 0) + 1

            for provider, count in providers.items():
                st.write(f"**{provider.upper()}:** {count} drafts")

    st.markdown("---")

    # Source breakdown
    st.markdown("### Connected Sources Breakdown")
    col1, col2, col3 = st.columns(3)

    if db.is_configured():
        twitter_sources = db.get_sources(st.session_state.user_id, 'twitter')
        youtube_sources = db.get_sources(st.session_state.user_id, 'youtube')
        newsletter_sources = db.get_sources(st.session_state.user_id, 'newsletter')

        with col1:
            st.metric("Twitter", len(twitter_sources))
            if twitter_sources:
                for source in twitter_sources[:3]:
                    st.write(f"- @{source['identifier']}")

        with col2:
            st.metric("YouTube", len(youtube_sources))
            if youtube_sources:
                for source in youtube_sources[:3]:
                    st.write(f"- {source['identifier']}")

        with col3:
            st.metric("Newsletters", len(newsletter_sources))
            if newsletter_sources:
                st.write(f"- {len(newsletter_sources)} RSS feeds")
    else:
        with col1:
            st.metric("Twitter", 0)
        with col2:
            st.metric("YouTube", 0)
        with col3:
            st.metric("Newsletters", 0)

    st.markdown("---")

    # Recent activity
    st.markdown("### Recent Activity")
    if db.is_configured():
        recent_drafts = db.get_drafts(st.session_state.user_id, limit=5)
        if recent_drafts:
            for draft in recent_drafts:
                st.write(f"✅ Generated: {draft['title']} (via {draft.get('llm_provider', 'unknown').upper()})")
        else:
            st.info("No drafts generated yet. Visit 'Generate Newsletter' to create your first draft!")
    else:
        st.info("Database not configured. Connect Supabase to track activity.")

    st.markdown("---")
    
    # Footer with provider info
    st.markdown(f"""
    <div style="text-align: center; color: #64748b; padding: 2rem 0;">
        <p>Built with Streamlit + Shadcn UI • Powered by {st.session_state.llm_provider.upper()}</p>
        <p style="font-size: 0.8rem;">CreatorPulse v2.0 Enhanced</p>
    </div>
    """, unsafe_allow_html=True)
