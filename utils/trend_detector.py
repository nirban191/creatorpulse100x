"""
Trend Detection Module for CreatorPulse
Analyzes content to detect trending topics and spikes
"""

from collections import Counter
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re


class TrendDetector:
    """Detects trending topics and keyword spikes in content"""

    def __init__(self, db=None):
        """
        Initialize trend detector

        Args:
            db: Optional database client for historical data
        """
        self.db = db
        self.stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
            'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
            'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
            'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one',
            'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
            'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when',
            'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
            'take', 'people', 'into', 'year', 'your', 'good', 'some',
            'could', 'them', 'see', 'other', 'than', 'then', 'now',
            'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
            'well', 'way', 'even', 'new', 'want', 'because', 'any',
            'these', 'give', 'day', 'most', 'us', 'is', 'was', 'are'
        }

    def extract_keywords(self, text: str, min_length: int = 4) -> List[str]:
        """
        Extract meaningful keywords from text

        Args:
            text: Input text to analyze
            min_length: Minimum keyword length

        Returns:
            List of extracted keywords
        """
        # Convert to lowercase and split
        words = re.findall(r'\b[a-z]+\b', text.lower())

        # Filter out stop words and short words
        keywords = [
            word for word in words
            if word not in self.stop_words and len(word) >= min_length
        ]

        return keywords

    def analyze_content(
        self,
        content_items: List[Dict],
        top_n: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Analyze content items and extract trending keywords

        Args:
            content_items: List of content dictionaries
            top_n: Number of top keywords to return

        Returns:
            List of trending keyword dictionaries
        """
        all_keywords = []

        # Extract keywords from all content
        for item in content_items:
            # Combine title and content
            text = ""
            if 'title' in item:
                text += item['title'] + " "
            if 'content' in item:
                text += str(item['content']) + " "
            if 'description' in item:
                text += str(item['description']) + " "

            keywords = self.extract_keywords(text)
            all_keywords.extend(keywords)

        # Count frequency
        keyword_counts = Counter(all_keywords)

        # Get top keywords
        top_keywords = keyword_counts.most_common(top_n)

        # Format results
        trending = []
        for keyword, count in top_keywords:
            trending.append({
                'keyword': keyword,
                'count': count,
                'relevance_score': self._calculate_relevance(keyword, count, len(content_items))
            })

        return trending

    def detect_spikes(
        self,
        current_keywords: List[Dict],
        historical_data: Optional[List[Dict]] = None,
        spike_threshold: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Detect keyword spikes compared to historical baseline

        Args:
            current_keywords: Current keyword frequencies
            historical_data: Historical keyword data (optional)
            spike_threshold: Multiplier to detect spike (default 2x)

        Returns:
            List of keywords with detected spikes
        """
        if not historical_data and self.db and self.db.is_configured():
            # Try to get from database if available
            try:
                historical_data = self._get_historical_keywords()
            except Exception:
                historical_data = []

        if not historical_data:
            # No historical data, return top keywords as trending
            return current_keywords[:10]

        # Build historical baseline
        historical_counts = {}
        for item in historical_data:
            keyword = item.get('keyword')
            count = item.get('count', 0)
            if keyword:
                historical_counts[keyword] = historical_counts.get(keyword, 0) + count

        # Calculate average baseline
        if historical_counts:
            avg_baseline = sum(historical_counts.values()) / len(historical_counts)
        else:
            avg_baseline = 1

        # Detect spikes
        spikes = []
        for keyword_data in current_keywords:
            keyword = keyword_data['keyword']
            current_count = keyword_data['count']
            baseline = historical_counts.get(keyword, avg_baseline)

            spike_factor = current_count / max(baseline, 1)

            if spike_factor >= spike_threshold:
                spikes.append({
                    **keyword_data,
                    'baseline': baseline,
                    'spike_factor': round(spike_factor, 2),
                    'is_spike': True,
                    'trend': 'rising' if spike_factor > 2 else 'steady'
                })

        return spikes

    def get_trending_topics(
        self,
        content_items: List[Dict],
        include_spikes: bool = True,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Get comprehensive trending topics analysis

        Args:
            content_items: List of content items to analyze
            include_spikes: Whether to include spike detection
            top_n: Number of top trends to return

        Returns:
            Dictionary with trending analysis
        """
        # Extract current keywords
        current_keywords = self.analyze_content(content_items, top_n=20)

        # Detect spikes if requested
        if include_spikes:
            spikes = self.detect_spikes(current_keywords)
        else:
            spikes = current_keywords[:top_n]

        # Store in database if available
        if self.db and self.db.is_configured():
            try:
                self._store_keywords(current_keywords)
            except Exception:
                pass  # Fail silently if database storage fails

        return {
            'trending_keywords': spikes[:top_n],
            'total_analyzed': len(content_items),
            'analyzed_at': datetime.now().isoformat(),
            'has_spikes': len(spikes) > 0
        }

    def format_trends_for_newsletter(
        self,
        trends: Dict[str, Any],
        max_trends: int = 5
    ) -> str:
        """
        Format trending topics for inclusion in newsletter

        Args:
            trends: Trending topics dictionary
            max_trends: Maximum number of trends to include

        Returns:
            Formatted markdown string
        """
        if not trends or not trends.get('trending_keywords'):
            return ""

        trending_keywords = trends['trending_keywords'][:max_trends]

        output = "## 🔥 What's Trending\n\n"

        for i, trend in enumerate(trending_keywords, 1):
            keyword = trend['keyword'].title()
            count = trend['count']

            if trend.get('is_spike'):
                spike_factor = trend.get('spike_factor', 0)
                emoji = "🚀" if spike_factor > 3 else "📈"
                output += f"{emoji} **{keyword}** - {count} mentions ({spike_factor}x spike)\n"
            else:
                output += f"• **{keyword}** - {count} mentions\n"

        output += "\n*These topics are generating buzz in your sources*\n\n"

        return output

    def _calculate_relevance(self, keyword: str, count: int, total_items: int) -> float:
        """Calculate relevance score for a keyword"""
        # Simple relevance: frequency weighted by keyword length
        frequency_score = count / max(total_items, 1)
        length_bonus = min(len(keyword) / 10, 1.0)  # Bonus for longer, more specific keywords
        return round((frequency_score + length_bonus) / 2, 3)

    def _get_historical_keywords(self, days: int = 7) -> List[Dict]:
        """Get historical keyword data from database"""
        if not self.db or not self.db.is_configured():
            return []

        try:
            # Get keywords from last N days
            cutoff_date = datetime.now() - timedelta(days=days)

            # This assumes a trends table exists (we'll create it)
            result = self.db.client.table('trends')\
                .select('keyword, mention_count as count')\
                .gte('detected_at', cutoff_date.isoformat())\
                .execute()

            return result.data if result.data else []
        except Exception:
            return []

    def _store_keywords(self, keywords: List[Dict]) -> None:
        """Store keyword data in database for future trend analysis"""
        if not self.db or not self.db.is_configured():
            return

        try:
            # Store top keywords for historical tracking
            for keyword_data in keywords[:20]:
                self.db.client.table('trends').insert({
                    'keyword': keyword_data['keyword'],
                    'mention_count': keyword_data['count'],
                    'detected_at': datetime.now().isoformat()
                }).execute()
        except Exception:
            pass  # Fail silently


def detect_trends_simple(content_items: List[Dict], top_n: int = 5) -> List[Dict]:
    """
    Simple standalone function to detect trends without database

    Args:
        content_items: List of content dictionaries
        top_n: Number of top trends to return

    Returns:
        List of trending topics
    """
    detector = TrendDetector()
    trends = detector.get_trending_topics(content_items, include_spikes=False, top_n=top_n)
    return trends.get('trending_keywords', [])
