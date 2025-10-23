# CreatorPulse - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CreatorPulse App                      │
│                      (Streamlit)                         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Home Page   │   │   Sources    │   │Style Trainer │
│              │   │  Management  │   │              │
└──────────────┘   └──────────────┘   └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Generator   │   │  Dashboard   │   │   Feedback   │
│              │   │              │   │     Loop     │
└──────────────┘   └──────────────┘   └──────────────┘
```

## Data Flow

```
1. USER INPUT
   └─> Connect Sources (Twitter/YouTube/RSS)
       └─> Session State Storage

2. CONTENT AGGREGATION
   ├─> Twitter API → Fetch Tweets
   ├─> YouTube API → Fetch Videos
   └─> RSS Parser → Fetch Articles
       └─> ContentAggregator.aggregate_all_content()

3. TREND DETECTION
   └─> Aggregated Content
       └─> TrendDetector.detect_trends()
           └─> Trend List

4. STYLE TRAINING
   └─> User Uploads Samples
       └─> StyleTrainer.analyze_writing_style()
           └─> Style Profile

5. DRAFT GENERATION
   ├─> Aggregated Content
   ├─> Detected Trends
   └─> Style Profile
       └─> NewsletterGenerator.generate_draft()
           └─> Newsletter Draft

6. USER FEEDBACK
   └─> Thumbs Up/Down
       └─> FeedbackProcessor.add_feedback()
           └─> Improve Future Drafts
```

## Component Architecture

### Frontend Layer (Streamlit)
```
app.py
├── Page: Home
│   ├── Hero Section
│   ├── Feature Cards
│   └── Quick Start Guide
│
├── Page: Source Connections
│   ├── Tab: Twitter
│   ├── Tab: YouTube
│   └── Tab: Newsletters
│
├── Page: Style Trainer
│   ├── File Upload
│   ├── Text Input
│   └── Training Display
│
├── Page: Newsletter Generator
│   ├── Configuration Form
│   ├── Draft Preview
│   └── Feedback Buttons
│
└── Page: Dashboard
    ├── Metrics Cards
    ├── Source Breakdown
    └── Activity Feed
```

### Backend Layer (Utilities)

#### 1. Content Aggregator (`content_aggregator.py`)
```python
ContentAggregator
├── fetch_twitter_content()
├── fetch_youtube_content()
├── fetch_newsletter_content()
└── aggregate_all_content()

TrendDetector
└── detect_trends()
```

#### 2. LLM Generator (`llm_generator.py`)
```python
StyleTrainer
├── analyze_writing_style()
└── get_style_prompt()

NewsletterGenerator
├── generate_draft()
├── _prepare_content_summary()
├── _prepare_trends_summary()
└── _generate_mock_draft()

FeedbackProcessor
├── add_feedback()
└── analyze_feedback_patterns()
```

#### 3. Data Models (`data_models.py`)
```python
@dataclass Source
@dataclass Tweet
@dataclass Video
@dataclass Article
@dataclass Trend
@dataclass StyleProfile
@dataclass NewsletterDraft
@dataclass Feedback
@dataclass UserSession
```

## State Management

### Session State Variables
```python
st.session_state = {
    'sources': {
        'twitter': [],      # List of Twitter handles
        'youtube': [],      # List of YouTube channels
        'newsletters': []   # List of RSS feed URLs
    },
    'style_trained': False,  # Boolean flag
    'generated_drafts': [],  # List of draft objects
    'user_feedback': []      # List of feedback objects
}
```

## API Integration Points

### External APIs
```
1. Twitter API (optional)
   Endpoint: Twitter API v2
   Auth: Bearer Token
   Rate Limit: Free tier limits apply

2. YouTube Data API (optional)
   Endpoint: YouTube Data API v3
   Auth: API Key
   Rate Limit: 10,000 units/day

3. RSS Feeds (feedparser)
   Protocol: RSS/Atom
   Auth: None (public feeds)
   Rate Limit: None

4. OpenAI API
   Endpoint: chat.completions
   Model: GPT-4 / GPT-3.5-turbo
   Auth: API Key

5. Anthropic API
   Endpoint: messages
   Model: Claude 3 Sonnet/Haiku
   Auth: API Key
```

## Workflow Diagrams

### User Journey 1: First Time Setup
```
Start
  │
  ├─> Open App
  │     │
  │     ├─> Navigate to Source Connections
  │     │     │
  │     │     ├─> Add Twitter Handle
  │     │     ├─> Add YouTube Channel
  │     │     └─> Add RSS Feed
  │     │
  │     ├─> Navigate to Style Trainer
  │     │     │
  │     │     ├─> Upload Past Newsletters
  │     │     └─> Click "Train Style"
  │     │
  │     └─> Success!
  │
  └─> Ready to Generate
```

### User Journey 2: Generate Newsletter
```
Start
  │
  ├─> Navigate to Generate Newsletter
  │     │
  │     ├─> Configure Settings
  │     │     ├─> Set Title
  │     │     ├─> Choose Time Range
  │     │     └─> Select Options
  │     │
  │     ├─> Click "Generate Draft"
  │     │     │
  │     │     ├─> [Backend] Fetch Content
  │     │     ├─> [Backend] Detect Trends
  │     │     ├─> [Backend] Generate Draft
  │     │     └─> Display Result
  │     │
  │     ├─> Review Draft
  │     │     │
  │     │     ├─> Option A: Accept (👍)
  │     │     ├─> Option B: Reject (👎)
  │     │     └─> Option C: Export (📧)
  │     │
  │     └─> Feedback Recorded
  │
  └─> End
```

## Deployment Architecture

### Option 1: Local Development
```
Developer Machine
├── Python 3.9+
├── Virtual Environment
├── Streamlit Server (localhost:8501)
└── Environment Variables (.env)
```

### Option 2: Streamlit Cloud
```
Streamlit Cloud
├── GitHub Repository
├── Automatic Deployment
├── Secrets Management
└── Free Hosting
```

### Option 3: Container Deployment
```
Docker Container
├── Python Base Image
├── Install Dependencies
├── Copy Application Files
├── Expose Port 8501
└── Run Streamlit
```

## Security Considerations

### API Keys
- Stored in `.env` file (not committed)
- Loaded via environment variables
- Never exposed in client code

### Data Privacy
- No persistent storage (session-based)
- No user authentication (MVP)
- No data collection

### Rate Limiting
- Mock data fallbacks
- Graceful error handling
- API quota management

## Performance Optimization

### Caching Strategy
```python
# Session state caching
st.session_state.cache_key = data

# Future: @st.cache_data decorator
@st.cache_data(ttl=3600)
def fetch_content():
    # Expensive operation
    pass
```

### Lazy Loading
- Content fetched on-demand
- Trends calculated when needed
- Drafts generated per request

### Efficient Reruns
- Minimal st.rerun() calls
- Batch state updates
- Conditional rendering

## Error Handling

### Fallback Strategy
```python
try:
    # API call
    result = api.fetch()
except Exception as e:
    # Log error
    print(f"Error: {e}")
    # Return mock data
    result = generate_mock_data()
```

### User Feedback
- Clear error messages
- Success confirmations
- Loading indicators
- Progress tracking

## Testing Strategy

### Unit Tests
```python
test_content_aggregator.py
test_llm_generator.py
test_data_models.py
```

### Integration Tests
```python
test_api_connections.py
test_draft_generation.py
test_feedback_loop.py
```

### UI Tests
```python
test_streamlit_pages.py
test_navigation.py
test_user_flows.py
```

## Monitoring & Analytics

### Current Metrics
- Drafts generated (count)
- Acceptance rate (%)
- Time saved (hours)
- Sources connected (count)

### Future Metrics
- API response times
- Error rates
- User engagement
- Draft quality scores

## Scalability Considerations

### Vertical Scaling
- Increase compute resources
- Optimize API calls
- Cache frequently used data

### Horizontal Scaling
- Multi-user support
- Database integration
- Queue-based processing

### Future Architecture
```
Load Balancer
    │
    ├─> Web Server 1
    ├─> Web Server 2
    └─> Web Server 3
         │
         ├─> Database (PostgreSQL)
         ├─> Cache (Redis)
         └─> Queue (Celery)
```

## Technology Decisions

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Frontend | Streamlit | Rapid development, Python-native |
| LLM | OpenAI/Anthropic | State-of-art generation quality |
| RSS Parser | feedparser | Robust, well-maintained |
| State Management | Session State | Simple, no DB required for MVP |
| Deployment | Streamlit Cloud | Free, easy, integrated |

## Conclusion

This architecture provides:
- **Simplicity:** Single-file app for easy deployment
- **Modularity:** Separate utilities for maintainability
- **Scalability:** Clear upgrade paths for future features
- **Flexibility:** Easy to swap components (LLM providers, etc.)
- **Reliability:** Mock data fallbacks for testing

Perfect for an MVP that can evolve into a production system!
