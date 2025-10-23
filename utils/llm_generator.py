"""
LLM Generator for CreatorPulse
Handles writing style training and newsletter draft generation using LLMs
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import OpenAI
import anthropic
from groq import Groq


class StyleTrainer:
    """Trains on user's writing style using past newsletters"""

    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.style_profile = {}

        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        elif provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        elif provider == "groq":
            self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def analyze_writing_style(self, sample_texts: List[str]) -> Dict[str, Any]:
        """
        Analyze writing samples to extract style characteristics

        Args:
            sample_texts: List of past newsletter or blog post content

        Returns:
            Dictionary containing style profile
        """
        # Combine samples for analysis
        combined_text = "\n\n---\n\n".join(sample_texts[:20])  # Use up to 20 samples

        prompt = f"""Analyze the following writing samples and extract the key style characteristics:

{combined_text}

Provide a detailed analysis including:
1. Tone (e.g., professional, casual, conversational, formal)
2. Voice (e.g., first-person, second-person, authoritative, friendly)
3. Sentence structure (e.g., short and punchy, long and detailed, varied)
4. Common phrases or expressions
5. Content structure patterns
6. Typical opening and closing styles
7. Use of humor, analogies, or storytelling

Format as JSON."""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a writing style analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                analysis = response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                analysis = response.content[0].text
            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model="llama-3.1-70b-versatile",  # Fast and free!
                    messages=[
                        {"role": "system", "content": "You are a writing style analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                analysis = response.choices[0].message.content

            self.style_profile = {
                'analysis': analysis,
                'sample_count': len(sample_texts),
                'trained': True
            }

            return self.style_profile

        except Exception as e:
            print(f"Error analyzing style: {e}")
            # Return mock analysis for demo
            return {
                'tone': 'Professional yet conversational',
                'voice': 'First-person with direct audience engagement',
                'structure': 'Clear sections with engaging introductions',
                'sentence_style': 'Varied length with punchy key points',
                'trained': True
            }

    def get_style_prompt(self) -> str:
        """Generate a prompt describing the learned writing style"""
        if not self.style_profile.get('trained'):
            return ""

        return f"""Write in the following style:
{self.style_profile.get('analysis', 'Professional and engaging tone')}

Maintain consistency with these characteristics throughout the newsletter."""


class NewsletterGenerator:
    """Generates newsletter drafts using LLM with trained style"""

    def __init__(self, provider: str = "groq", model: str = None):
        self.provider = provider
        self.model = model  # For Groq model selection

        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        elif provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        elif provider == "groq":
            self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
            if not model:
                self.model = "llama-3.1-70b-versatile"  # Default Groq model

    def generate_draft(
        self,
        aggregated_content: Dict[str, List[Dict]],
        trends: List[Dict[str, Any]],
        style_prompt: str = "",
        title: str = "Weekly Newsletter",
        num_articles: int = 5
    ) -> str:
        """
        Generate a newsletter draft based on aggregated content and style

        Args:
            aggregated_content: Content from various sources
            trends: List of detected trends
            style_prompt: Style guidance from StyleTrainer
            title: Newsletter title
            num_articles: Number of main articles to include

        Returns:
            Generated newsletter draft as markdown string
        """
        # Prepare content summary
        content_summary = self._prepare_content_summary(aggregated_content, num_articles)
        trends_summary = self._prepare_trends_summary(trends)

        prompt = f"""Create a compelling newsletter draft with the following specifications:

Title: {title}

Content to curate:
{content_summary}

Trending Topics:
{trends_summary}

{style_prompt}

Structure the newsletter with:
1. Engaging introduction (2-3 sentences)
2. Top {num_articles} curated stories with:
   - Catchy headline
   - Brief summary (2-3 sentences)
   - "Why it matters" insight
   - Source link
3. Trending topics section (if applicable)
4. Quick takes or additional links
5. Closing remarks

Make it engaging, informative, and ready to send with minimal editing.
Format in Markdown."""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert newsletter curator and writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                draft = response.choices[0].message.content

            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=3000,
                    messages=[{"role": "user", "content": prompt}]
                )
                draft = response.content[0].text

            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,  # Use selected Groq model
                    messages=[
                        {"role": "system", "content": "You are an expert newsletter curator and writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                draft = response.choices[0].message.content

            return draft

        except Exception as e:
            # Re-raise the exception so the app can handle it properly
            raise Exception(f"AI generation failed: {str(e)}")

    def _prepare_content_summary(self, content: Dict[str, List[Dict]], limit: int) -> str:
        """Prepare a summary of aggregated content for the LLM"""
        summary_parts = []

        # Twitter content
        if content.get('twitter'):
            summary_parts.append("Twitter insights:")
            for tweet in content['twitter'][:limit]:
                summary_parts.append(f"- @{tweet['author']}: {tweet['content']}")

        # YouTube content
        if content.get('youtube'):
            summary_parts.append("\nYouTube videos:")
            for video in content['youtube'][:limit]:
                summary_parts.append(f"- {video['title']}: {video['description']}")

        # Newsletter content
        if content.get('newsletters'):
            summary_parts.append("\nNewsletter articles:")
            for article in content['newsletters'][:limit]:
                summary_parts.append(f"- {article['title']}: {article['content'][:200]}...")

        return "\n".join(summary_parts)

    def _prepare_trends_summary(self, trends: List[Dict]) -> str:
        """Prepare a summary of trending topics"""
        if not trends:
            return "No specific trends detected."

        summary = []
        for trend in trends[:3]:
            summary.append(f"- {trend['topic']}: {trend['description']}")

        return "\n".join(summary)

    def generate_newsletter(
        self,
        content_items: List[Dict],
        title: str = "Weekly Newsletter",
        style_profile: Optional[Dict] = None,
        num_articles: int = 5,
        include_trends: bool = True
    ) -> str:
        """
        Simplified newsletter generation method

        Args:
            content_items: List of content items from sources
            title: Newsletter title
            style_profile: Optional style training data
            num_articles: Number of articles to include
            include_trends: Whether to include trending topics

        Returns:
            Generated newsletter as markdown string
        """
        # Prepare style prompt if available
        style_prompt = ""
        if style_profile and style_profile.get('training_text'):
            style_prompt = f"\n\nWrite in a style similar to this sample:\n{style_profile['training_text'][:500]}..."

        # Prepare content summary
        content_summary = "\n".join([f"- {item.get('title', 'Content from ' + item.get('identifier', 'unknown'))}" for item in content_items[:num_articles]])

        prompt = f"""Create an engaging newsletter with the title "{title}".

Available content sources:
{content_summary}

Requirements:
1. Write an engaging introduction (2-3 sentences)
2. Include {num_articles} curated stories with:
   - Catchy headline
   - Brief summary (2-3 sentences)
   - "Why it matters" insight
3. {"Include a trending topics section" if include_trends else ""}
4. Add quick takes or additional insights
5. Close with a friendly sign-off

{style_prompt}

Make it informative, engaging, and ready to send. Format in Markdown."""

        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert newsletter curator and writer. Create engaging, informative newsletters that readers love."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                return response.choices[0].message.content

            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert newsletter curator and writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=3000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text

        except Exception as e:
            # Re-raise the exception so the app can handle it properly
            raise Exception(f"AI generation failed: {str(e)}")


class FeedbackProcessor:
    """Processes user feedback to improve future drafts"""

    def __init__(self):
        self.feedback_history = []

    def add_feedback(self, draft_id: str, feedback_type: str, edits: Optional[str] = None):
        """
        Record user feedback on a draft

        Args:
            draft_id: Identifier for the draft
            feedback_type: 'positive' or 'negative'
            edits: Optional text showing user's edits
        """
        self.feedback_history.append({
            'draft_id': draft_id,
            'type': feedback_type,
            'edits': edits,
            'timestamp': str(datetime.now())
        })

    def analyze_feedback_patterns(self) -> Dict[str, Any]:
        """
        Analyze feedback history to identify improvement areas

        Returns:
            Dictionary with insights on what to adjust
        """
        if not self.feedback_history:
            return {'message': 'No feedback yet'}

        positive_count = len([f for f in self.feedback_history if f['type'] == 'positive'])
        total_count = len(self.feedback_history)

        acceptance_rate = (positive_count / total_count) * 100 if total_count > 0 else 0

        return {
            'acceptance_rate': acceptance_rate,
            'total_drafts': total_count,
            'positive_feedback': positive_count,
            'needs_improvement': acceptance_rate < 70
        }
