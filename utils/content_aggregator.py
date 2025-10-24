"""
Content Aggregator for CreatorPulse
Handles fetching content from various sources: Twitter, YouTube, and Newsletter RSS
"""

import os
import requests
from typing import List, Dict, Any, Optional
import feedparser
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re


class ContentAggregator:
    """Aggregates content from multiple sources"""

    def __init__(self):
        self.twitter_api_key = os.getenv('TWITTER_BEARER_TOKEN')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube_service = None

        # Initialize YouTube API service if key is available
        if self.youtube_api_key:
            try:
                self.youtube_service = build('youtube', 'v3', developerKey=self.youtube_api_key)
            except Exception as e:
                print(f"Failed to initialize YouTube API: {e}")

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

    def _extract_channel_id(self, channel_input: str) -> Optional[str]:
        """
        Extract channel ID from various input formats:
        - Channel ID: UCxxxxxx
        - Channel URL: youtube.com/@channelname or youtube.com/channel/UCxxxxxx
        - Handle: @channelname
        """
        # If it's already a channel ID (starts with UC)
        if channel_input.startswith('UC') and len(channel_input) == 24:
            return channel_input

        # Extract from URL
        if 'youtube.com' in channel_input or 'youtu.be' in channel_input:
            # Try to extract channel ID from URL
            match = re.search(r'/channel/(UC[\w-]+)', channel_input)
            if match:
                return match.group(1)

            # Extract handle from URL
            match = re.search(r'/@([\w-]+)', channel_input)
            if match:
                handle = match.group(1)
                return self._get_channel_id_from_handle(handle)

        # If it's a handle (starts with @)
        if channel_input.startswith('@'):
            return self._get_channel_id_from_handle(channel_input[1:])

        # Try as handle without @
        return self._get_channel_id_from_handle(channel_input)

    def _get_channel_id_from_handle(self, handle: str) -> Optional[str]:
        """Get channel ID from handle using YouTube API search"""
        if not self.youtube_service:
            return None

        try:
            # Search for channel by handle
            request = self.youtube_service.search().list(
                part='snippet',
                q=handle,
                type='channel',
                maxResults=1
            )
            response = request.execute()

            if response['items']:
                return response['items'][0]['snippet']['channelId']
        except HttpError as e:
            print(f"Error fetching channel ID for {handle}: {e}")

        return None

    def fetch_youtube_content(self, channels: List[str], days_back: int = 7, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch recent videos from specified YouTube channels using real API

        Args:
            channels: List of YouTube channel IDs, URLs, or handles
            days_back: Number of days to look back
            max_results: Maximum number of videos per channel (default 10)

        Returns:
            List of video dictionaries with title, description, URL, and metadata
        """
        if not self.youtube_service:
            print("YouTube API not configured. Please set YOUTUBE_API_KEY environment variable.")
            return self._get_mock_youtube_data(channels)

        videos = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        for channel_input in channels:
            try:
                # Extract channel ID from various formats
                channel_id = self._extract_channel_id(channel_input)

                if not channel_id:
                    print(f"Could not extract channel ID from: {channel_input}")
                    continue

                # Get channel details
                channel_request = self.youtube_service.channels().list(
                    part='snippet',
                    id=channel_id
                )
                channel_response = channel_request.execute()

                if not channel_response['items']:
                    print(f"Channel not found: {channel_id}")
                    continue

                channel_name = channel_response['items'][0]['snippet']['title']

                # Search for recent videos from this channel
                search_request = self.youtube_service.search().list(
                    part='snippet',
                    channelId=channel_id,
                    order='date',
                    type='video',
                    maxResults=max_results,
                    publishedAfter=cutoff_date.isoformat() + 'Z'
                )
                search_response = search_request.execute()

                # Get detailed video statistics
                video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

                if video_ids:
                    videos_request = self.youtube_service.videos().list(
                        part='snippet,statistics,contentDetails',
                        id=','.join(video_ids)
                    )
                    videos_response = videos_request.execute()

                    for video in videos_response.get('items', []):
                        videos.append({
                            'id': video['id'],
                            'title': video['snippet']['title'],
                            'description': video['snippet']['description'][:500],  # Truncate long descriptions
                            'url': f"https://youtube.com/watch?v={video['id']}",
                            'channel': channel_name,
                            'channel_id': channel_id,
                            'thumbnail': video['snippet']['thumbnails']['high']['url'],
                            'published_at': video['snippet']['publishedAt'],
                            'views': int(video['statistics'].get('viewCount', 0)),
                            'likes': int(video['statistics'].get('likeCount', 0)),
                            'comments': int(video['statistics'].get('commentCount', 0)),
                            'duration': video['contentDetails']['duration']
                        })

            except HttpError as e:
                error_details = e.error_details[0] if e.error_details else {}
                if error_details.get('reason') == 'quotaExceeded':
                    print(f"⚠️ YouTube API quota exceeded. Using cached/mock data.")
                    return self._get_mock_youtube_data(channels)
                else:
                    print(f"Error fetching YouTube content for {channel_input}: {e}")
            except Exception as e:
                print(f"Unexpected error fetching YouTube content for {channel_input}: {e}")

        return videos

    def _get_mock_youtube_data(self, channels: List[str]) -> List[Dict[str, Any]]:
        """Return mock YouTube data when API is unavailable"""
        videos = []
        for channel in channels[:3]:  # Limit to 3 channels for mock
            videos.append({
                'id': 'mock_video_id',
                'title': f"Latest video from {channel}",
                'description': "This video covers the latest trends in content creation and AI tools",
                'url': f"https://youtube.com/watch?v=example",
                'channel': channel,
                'channel_id': 'UCmock',
                'thumbnail': 'https://i.ytimg.com/vi/mock/hqdefault.jpg',
                'published_at': datetime.now().isoformat(),
                'views': 10000,
                'likes': 500,
                'comments': 50,
                'duration': 'PT10M30S'
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
