"""
Content Aggregator for CreatorPulse
Handles fetching content from various sources: Twitter, YouTube, and Newsletter RSS
"""

import os
import requests
from typing import List, Dict, Any
import feedparser
from datetime import datetime, timedelta


class ContentAggregator:
    """Aggregates content from multiple sources"""

    def __init__(self):
        self.twitter_api_key = os.getenv('TWITTER_BEARER_TOKEN')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')

    def fetch_twitter_content(self, handles: List[str], days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Fetch recent tweets from specified handles

        Args:
            handles: List of Twitter handles (without @)
            days_back: Number of days to look back

        Returns:
            List of tweet dictionaries with content, author, timestamp, and URL
        """
        # Placeholder for Twitter API integration
        # In production, use tweepy or Twitter API v2
        tweets = []

        for handle in handles:
            # Mock data for demonstration
            tweets.append({
                'content': f"Sample tweet from @{handle} about AI and content creation",
                'author': handle,
                'timestamp': datetime.now().isoformat(),
                'url': f"https://twitter.com/{handle}/status/123456789",
                'engagement': {'likes': 100, 'retweets': 20}
            })

        return tweets

    def fetch_youtube_content(self, channels: List[str], days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Fetch recent videos from specified YouTube channels

        Args:
            channels: List of YouTube channel IDs or names
            days_back: Number of days to look back

        Returns:
            List of video dictionaries with title, description, URL, and metadata
        """
        # Placeholder for YouTube API integration
        # In production, use google-api-python-client
        videos = []

        for channel in channels:
            # Mock data for demonstration
            videos.append({
                'title': f"Latest video from {channel}",
                'description': "This video covers the latest trends in content creation and AI tools",
                'url': f"https://youtube.com/watch?v=example",
                'channel': channel,
                'published_at': datetime.now().isoformat(),
                'views': 10000
            })

        return videos

    def fetch_newsletter_content(self, rss_feeds: List[str], days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Fetch recent articles from newsletter RSS feeds

        Args:
            rss_feeds: List of RSS feed URLs
            days_back: Number of days to look back

        Returns:
            List of article dictionaries with title, content, URL, and metadata
        """
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries:
                    # Parse published date
                    pub_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()

                    if pub_date >= cutoff_date:
                        articles.append({
                            'title': entry.get('title', 'No title'),
                            'content': entry.get('summary', ''),
                            'url': entry.get('link', ''),
                            'author': entry.get('author', 'Unknown'),
                            'published_at': pub_date.isoformat(),
                            'source': feed.feed.get('title', feed_url)
                        })
            except Exception as e:
                print(f"Error fetching RSS feed {feed_url}: {e}")
                # Add mock data for demo purposes
                articles.append({
                    'title': f"Sample article from {feed_url}",
                    'content': "This is a sample article about content curation and newsletter best practices.",
                    'url': feed_url,
                    'author': 'Demo Author',
                    'published_at': datetime.now().isoformat(),
                    'source': 'Demo Newsletter'
                })

        return articles

    def aggregate_all_content(self, sources: Dict[str, List[str]], days_back: int = 7) -> Dict[str, List[Dict]]:
        """
        Aggregate content from all sources

        Args:
            sources: Dictionary with keys 'twitter', 'youtube', 'newsletters'
            days_back: Number of days to look back

        Returns:
            Dictionary with aggregated content from all sources
        """
        return {
            'twitter': self.fetch_twitter_content(sources.get('twitter', []), days_back),
            'youtube': self.fetch_youtube_content(sources.get('youtube', []), days_back),
            'newsletters': self.fetch_newsletter_content(sources.get('newsletters', []), days_back)
        }


class TrendDetector:
    """Detects emerging trends from aggregated content"""

    def __init__(self):
        pass

    def detect_trends(self, aggregated_content: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Analyze content and detect emerging trends

        Args:
            aggregated_content: Content from ContentAggregator

        Returns:
            List of trend dictionaries with topic, relevance, and supporting content
        """
        # Placeholder for trend detection logic
        # In production, use NLP techniques, keyword extraction, and spike detection

        trends = [
            {
                'topic': 'AI-Powered Content Creation',
                'relevance_score': 0.95,
                'description': 'Growing interest in AI tools for content generation and curation',
                'sources': ['Twitter', 'YouTube', 'Newsletters'],
                'momentum': 'rising'
            },
            {
                'topic': 'Newsletter Platform Evolution',
                'relevance_score': 0.88,
                'description': 'New features and integrations in newsletter platforms like Substack and Beehiiv',
                'sources': ['Newsletters', 'Twitter'],
                'momentum': 'stable'
            },
            {
                'topic': 'Creator Economy Expansion',
                'relevance_score': 0.82,
                'description': 'Increasing opportunities for independent creators across platforms',
                'sources': ['YouTube', 'Twitter'],
                'momentum': 'rising'
            }
        ]

        return trends
