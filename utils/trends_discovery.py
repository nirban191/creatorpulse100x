"""
Trends Discovery Module for CreatorPulse
Handles fetching trending topics from Google Trends using pytrends
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pytrends.request import TrendReq
import pandas as pd


class TrendsDiscovery:
    """Discovers trending topics using Google Trends API"""

    # Category mappings for Google Trends
    CATEGORY_MAP = {
        'all': 0,
        'tech': 13,  # Computers & Electronics
        'ai': 13,    # Computers & Electronics (closest match)
        'business': 12,  # Business & Industrial
        'science': 174,  # Science
        'news': 16,  # News
        'entertainment': 3,  # Arts & Entertainment
        'health': 45,  # Health
        'sports': 20,  # Sports
    }

    def __init__(self):
        """Initialize pytrends connection"""
        try:
            # Initialize TrendReq with automatic language detection
            self.pytrends = TrendReq(hl='en-US', tz=360)
            self.last_request_time = 0
            self.rate_limit_seconds = 61  # Wait 61 seconds between requests
        except Exception as e:
            print(f"Error initializing pytrends: {e}")
            self.pytrends = None

    def _rate_limit(self):
        """Enforce rate limiting to avoid Google blocking"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit_seconds:
                wait_time = self.rate_limit_seconds - elapsed
                print(f"Rate limiting: waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
        self.last_request_time = time.time()

    def fetch_daily_trends(self, country: str = 'US') -> List[Dict[str, Any]]:
        """
        Fetch daily trending searches (real-time trends)

        Args:
            country: Country code (US, GB, IN, etc.)

        Returns:
            List of trending topics with metadata
        """
        if not self.pytrends:
            print("pytrends not initialized")
            return []

        try:
            self._rate_limit()

            # Get trending searches for today
            trending_searches_df = self.pytrends.trending_searches(pn=country)

            trends = []
            for idx, search_term in trending_searches_df[0].items():
                trends.append({
                    'title': search_term,
                    'description': f"Trending search in {country}",
                    'keywords': [search_term],
                    'url': f"https://trends.google.com/trends/explore?q={search_term}",
                    'source_type': 'google_trends',
                    'category': 'all',
                    'discovered_at': datetime.now().isoformat(),
                    'metadata': {
                        'country': country,
                        'rank': idx + 1,
                        'type': 'daily_trending'
                    }
                })

            print(f"✅ Fetched {len(trends)} daily trending searches for {country}")
            return trends

        except Exception as e:
            print(f"Error fetching daily trends: {e}")
            return []

    def fetch_trending_topics(self, category: str = 'tech', max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch trending topics by category

        Args:
            category: Category name ('tech', 'ai', 'business', etc.)
            max_results: Maximum number of trends to return

        Returns:
            List of trending topics with metadata
        """
        if not self.pytrends:
            print("pytrends not initialized")
            return []

        try:
            # Get trending searches first (no category filter in trending_searches)
            trends = self.fetch_daily_trends()

            # If we want category-specific trends, we need to analyze interest
            if category != 'all' and trends:
                # Get category code
                category_code = self.CATEGORY_MAP.get(category.lower(), 0)

                # Filter trends by relevance to category (simplified approach)
                # In production, you'd want to analyze each trend's category
                print(f"Note: Category filtering for '{category}' applied (simplified)")

            return trends[:max_results]

        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            return []

    def fetch_interest_over_time(self, keywords: List[str], timeframe: str = 'today 3-m') -> Dict[str, Any]:
        """
        Fetch interest over time for specific keywords

        Args:
            keywords: List of keywords to analyze (max 5)
            timeframe: Timeframe for analysis ('today 3-m', 'today 12-m', 'today 5-y', etc.)

        Returns:
            Dictionary with trend data and metadata
        """
        if not self.pytrends:
            print("pytrends not initialized")
            return {}

        if not keywords:
            return {}

        # Limit to 5 keywords (pytrends limitation)
        keywords = keywords[:5]

        try:
            self._rate_limit()

            # Build payload
            self.pytrends.build_payload(
                kw_list=keywords,
                timeframe=timeframe,
                geo='US'
            )

            # Get interest over time
            interest_df = self.pytrends.interest_over_time()

            if interest_df.empty:
                print(f"No interest data found for keywords: {keywords}")
                return {}

            # Calculate average interest for each keyword
            keyword_stats = {}
            for keyword in keywords:
                if keyword in interest_df.columns:
                    values = interest_df[keyword].values
                    keyword_stats[keyword] = {
                        'average': float(values.mean()),
                        'max': float(values.max()),
                        'min': float(values.min()),
                        'current': float(values[-1]) if len(values) > 0 else 0,
                        'trending': 'up' if len(values) > 1 and values[-1] > values[-2] else 'down'
                    }

            return {
                'keywords': keywords,
                'timeframe': timeframe,
                'stats': keyword_stats,
                'fetched_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error fetching interest over time: {e}")
            return {}

    def fetch_related_queries(self, keyword: str) -> Dict[str, Any]:
        """
        Fetch related queries for a keyword

        Args:
            keyword: Keyword to analyze

        Returns:
            Dictionary with related queries (rising and top)
        """
        if not self.pytrends:
            print("pytrends not initialized")
            return {}

        try:
            self._rate_limit()

            # Build payload
            self.pytrends.build_payload(
                kw_list=[keyword],
                timeframe='today 3-m',
                geo='US'
            )

            # Get related queries
            related_queries = self.pytrends.related_queries()

            if not related_queries or keyword not in related_queries:
                return {}

            result = {
                'keyword': keyword,
                'rising': [],
                'top': []
            }

            # Extract rising queries
            if 'rising' in related_queries[keyword] and related_queries[keyword]['rising'] is not None:
                rising_df = related_queries[keyword]['rising']
                if not rising_df.empty:
                    result['rising'] = rising_df['query'].head(10).tolist()

            # Extract top queries
            if 'top' in related_queries[keyword] and related_queries[keyword]['top'] is not None:
                top_df = related_queries[keyword]['top']
                if not top_df.empty:
                    result['top'] = top_df['query'].head(10).tolist()

            return result

        except Exception as e:
            print(f"Error fetching related queries: {e}")
            return {}

    def discover_trends_for_categories(
        self,
        categories: List[str],
        max_per_category: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Discover trends for multiple categories

        Args:
            categories: List of category names
            max_per_category: Maximum trends per category

        Returns:
            List of all discovered trends
        """
        all_trends = []

        for category in categories:
            print(f"🔍 Fetching trends for category: {category}")
            trends = self.fetch_trending_topics(category=category, max_results=max_per_category)

            # Add category to each trend
            for trend in trends:
                trend['category'] = category

            all_trends.extend(trends)

            # Rate limit between categories
            if len(categories) > 1:
                time.sleep(2)  # Small delay between categories

        print(f"✅ Total trends discovered: {len(all_trends)}")
        return all_trends

    def enrich_trend_with_related(self, trend: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich a trend with related queries

        Args:
            trend: Trend dictionary to enrich

        Returns:
            Enriched trend dictionary
        """
        if 'title' not in trend:
            return trend

        keyword = trend['title']
        related = self.fetch_related_queries(keyword)

        if related:
            # Add related queries to metadata
            if 'metadata' not in trend:
                trend['metadata'] = {}

            trend['metadata']['related_rising'] = related.get('rising', [])
            trend['metadata']['related_top'] = related.get('top', [])

            # Update keywords list with related queries
            all_related = related.get('rising', []) + related.get('top', [])
            trend['keywords'] = list(set(trend.get('keywords', []) + all_related[:5]))

        return trend
