"""
Data Models for CreatorPulse
Defines the structure of data used throughout the application
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Source:
    """Represents a content source"""
    type: str  # 'twitter', 'youtube', 'newsletter'
    identifier: str  # handle, channel name, or RSS URL
    active: bool = True
    added_at: datetime = datetime.now()


@dataclass
class Tweet:
    """Twitter content item"""
    content: str
    author: str
    timestamp: str
    url: str
    engagement: Dict[str, int]  # likes, retweets, replies


@dataclass
class Video:
    """YouTube video content item"""
    title: str
    description: str
    url: str
    channel: str
    published_at: str
    views: int


@dataclass
class Article:
    """Newsletter article content item"""
    title: str
    content: str
    url: str
    author: str
    published_at: str
    source: str


@dataclass
class Trend:
    """Detected trend"""
    topic: str
    relevance_score: float
    description: str
    sources: List[str]
    momentum: str  # 'rising', 'stable', 'declining'


@dataclass
class StyleProfile:
    """User's writing style profile"""
    tone: str
    voice: str
    structure: str
    sentence_style: str
    sample_count: int
    trained: bool
    analysis: Optional[str] = None


@dataclass
class NewsletterDraft:
    """Generated newsletter draft"""
    title: str
    content: str
    timestamp: float
    sources_used: List[str]
    trends_included: List[str]
    word_count: int
    estimated_read_time: int  # minutes


@dataclass
class Feedback:
    """User feedback on a draft"""
    draft_id: str
    feedback_type: str  # 'positive' or 'negative'
    timestamp: str
    edits: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class UserSession:
    """User session data"""
    sources: Dict[str, List[str]]
    style_trained: bool
    generated_drafts: List[NewsletterDraft]
    user_feedback: List[Feedback]
    settings: Dict[str, any]


# Example data structures for reference

EXAMPLE_AGGREGATED_CONTENT = {
    'twitter': [
        {
            'content': 'AI is transforming content creation...',
            'author': 'techcreator',
            'timestamp': '2024-01-15T10:30:00',
            'url': 'https://twitter.com/techcreator/status/123',
            'engagement': {'likes': 150, 'retweets': 30}
        }
    ],
    'youtube': [
        {
            'title': 'How to Build Better Newsletters',
            'description': 'A guide to newsletter best practices',
            'url': 'https://youtube.com/watch?v=abc123',
            'channel': 'ContentMastery',
            'published_at': '2024-01-15T14:00:00',
            'views': 5000
        }
    ],
    'newsletters': [
        {
            'title': 'The Future of Creator Economy',
            'content': 'Creators are finding new ways to monetize...',
            'url': 'https://newsletter.example.com/post/123',
            'author': 'Jane Doe',
            'published_at': '2024-01-15T08:00:00',
            'source': 'Creator Weekly'
        }
    ]
}

EXAMPLE_TRENDS = [
    {
        'topic': 'AI-Powered Content Tools',
        'relevance_score': 0.92,
        'description': 'Growing adoption of AI tools for content creation',
        'sources': ['Twitter', 'YouTube', 'Newsletters'],
        'momentum': 'rising'
    },
    {
        'topic': 'Newsletter Platform Innovation',
        'relevance_score': 0.85,
        'description': 'New features launching in Substack and Beehiiv',
        'sources': ['Newsletters', 'Twitter'],
        'momentum': 'stable'
    }
]

EXAMPLE_STYLE_PROFILE = {
    'tone': 'Professional yet conversational',
    'voice': 'First-person with direct audience engagement',
    'structure': 'Clear sections with engaging introductions',
    'sentence_style': 'Varied length with punchy key points',
    'sample_count': 25,
    'trained': True,
    'analysis': 'User writes with a friendly but authoritative voice...'
}
