"""
OpenClaw Content Generation Agent Example

Real-world example: Automated weekly newsletter generation.

This example shows how to:
1. Collect content from multiple sources
2. Use AI to analyze and summarize
3. Generate formatted output
4. Publish to multiple channels
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict

class NewsletterAgent:
    """
    Automated newsletter generation agent.
    
    Features:
    - Multi-source content collection
    - AI-powered summarization
    - Template-based formatting
    - Multi-channel publishing
    """
    
    def __init__(self, sources: List[str], ai_model: str = "gpt-4"):
        self.sources = sources
        self.ai_model = ai_model
        self.collected_items = []
    
    def collect_content(self) -> List[Dict]:
        """
        Collect content from configured sources.
        
        Sources can be:
        - RSS feeds
        - GitHub trending
        - Hacker News
        - Reddit
        - Twitter
        """
        print("📥 Collecting content from sources...")
        
        for source in self.sources:
            if source.startswith("rss://"):
                items = self._fetch_rss(source)
            elif source.startswith("github://"):
                items = self._fetch_github_trending(source)
            elif source.startswith("hn://"):
                items = self._fetch_hackernews()
            else:
                print(f"⚠️  Unknown source: {source}")
                continue
            
            self.collected_items.extend(items)
        
        print(f"✅ Collected {len(self.collected_items)} items")
        return self.collected_items
    
    def _fetch_rss(self, url: str) -> List[Dict]:
        """Fetch items from RSS feed."""
        # Simplified - use feedparser in production
        feed_url = url.replace("rss://", "https://")
        
        try:
            response = requests.get(feed_url, timeout=10)
            # Parse RSS and extract items
            # Return list of {title, link, description, date}
            return []
        except Exception as e:
            print(f"❌ RSS fetch failed: {e}")
            return []
    
    def _fetch_github_trending(self, source: str) -> List[Dict]:
        """Fetch GitHub trending repositories."""
        # Example: github://python/daily
        parts = source.replace("github://", "").split("/")
        language = parts[0] if len(parts) > 0 else ""
        
        url = f"https://api.github.com/search/repositories"
        params = {
            "q": f"language:{language} created:>{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}",
            "sort": "stars",
            "order": "desc",
            "per_page": 10
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            repos = response.json().get("items", [])
            
            return [{
                "title": repo["full_name"],
                "link": repo["html_url"],
                "description": repo["description"],
                "stars": repo["stargazers_count"],
                "source": "GitHub"
            } for repo in repos]
        except Exception as e:
            print(f"❌ GitHub fetch failed: {e}")
            return []
    
    def _fetch_hackernews(self) -> List[Dict]:
        """Fetch top stories from Hacker News."""
        try:
            # Get top story IDs
            response = requests.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json",
                timeout=10
            )
            story_ids = response.json()[:10]
            
            items = []
            for story_id in story_ids:
                story_response = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=5
                )
                story = story_response.json()
                
                items.append({
                    "title": story.get("title"),
                    "link": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "score": story.get("score"),
                    "source": "Hacker News"
                })
            
            return items
        except Exception as e:
            print(f"❌ HN fetch failed: {e}")
            return []
    
    def analyze_and_rank(self) -> List[Dict]:
        """
        Use AI to analyze content and rank by importance.
        
        This is where OpenClaw's AI capabilities shine!
        """
        print("🤖 Analyzing content with AI...")
        
        # In production, use OpenClaw's AI to:
        # 1. Summarize each item
        # 2. Extract key insights
        # 3. Rank by relevance/importance
        # 4. Remove duplicates
        
        # Simplified example:
        ranked_items = sorted(
            self.collected_items,
            key=lambda x: x.get("stars", 0) + x.get("score", 0),
            reverse=True
        )[:10]
        
        print(f"✅ Selected top {len(ranked_items)} items")
        return ranked_items
    
    def generate_newsletter(self, items: List[Dict]) -> str:
        """
        Generate formatted newsletter content.
        
        Uses template + AI for natural language.
        """
        print("📝 Generating newsletter...")
        
        # Header
        date = datetime.now().strftime("%Y-%m-%d")
        newsletter = f"# 🚀 Weekly Tech Digest - {date}\n\n"
        newsletter += "Your curated selection of the week's best tech content.\n\n"
        newsletter += "---\n\n"
        
        # Content
        for i, item in enumerate(items, 1):
            newsletter += f"## {i}. {item['title']}\n\n"
            
            if item.get("description"):
                newsletter += f"{item['description']}\n\n"
            
            newsletter += f"🔗 [{item['link']}]({item['link']})\n"
            
            if item.get("stars"):
                newsletter += f"⭐ {item['stars']} stars"
            if item.get("score"):
                newsletter += f" | 🔥 {item['score']} points"
            
            newsletter += f" | 📍 {item['source']}\n\n"
            newsletter += "---\n\n"
        
        # Footer
        newsletter += "\n**That's all for this week!**\n\n"
        newsletter += "💌 [Subscribe](https://example.com/subscribe) | "
        newsletter += "🐦 [Twitter](https://twitter.com/example) | "
        newsletter += "💬 [Discuss](https://example.com/discuss)\n"
        
        print("✅ Newsletter generated")
        return newsletter
    
    def publish(self, content: str, channels: List[str]):
        """
        Publish newsletter to multiple channels.
        
        Channels:
        - GitHub (as markdown file)
        - Email (via API)
        - Telegram (as message)
        - Website (via webhook)
        """
        print("📤 Publishing to channels...")
        
        for channel in channels:
            if channel == "github":
                self._publish_github(content)
            elif channel == "telegram":
                self._publish_telegram(content)
            elif channel == "email":
                self._publish_email(content)
            else:
                print(f"⚠️  Unknown channel: {channel}")
        
        print("✅ Published to all channels")
    
    def _publish_github(self, content: str):
        """Publish to GitHub repository."""
        # Use git commands to commit and push
        filename = f"weekly/{datetime.now().strftime('%Y-W%W')}.md"
        
        with open(filename, "w") as f:
            f.write(content)
        
        # Git operations would go here
        print(f"✅ Published to GitHub: {filename}")
    
    def _publish_telegram(self, content: str):
        """Publish to Telegram channel."""
        # Truncate for Telegram (4096 char limit)
        summary = content[:500] + "...\n\n[Read full newsletter](https://example.com/latest)"
        
        # Use OpenClaw message tool
        print(f"✅ Published to Telegram")
    
    def _publish_email(self, content: str):
        """Send via email."""
        # Use email service API
        print(f"✅ Sent via email")
    
    def run(self, channels: List[str] = ["github"]):
        """
        Run the complete newsletter generation pipeline.
        
        This is the main method to call from your cron job.
        """
        print("\n🦞 Starting newsletter generation...\n")
        
        # 1. Collect content
        self.collect_content()
        
        if not self.collected_items:
            print("❌ No content collected, aborting")
            return
        
        # 2. Analyze and rank
        top_items = self.analyze_and_rank()
        
        # 3. Generate newsletter
        newsletter = self.generate_newsletter(top_items)
        
        # 4. Publish
        self.publish(newsletter, channels)
        
        print("\n✅ Newsletter generation complete!\n")
        return newsletter


# Example: Use with OpenClaw cron
"""
To automate this with OpenClaw:

1. Create the agent:
   agent = NewsletterAgent(
       sources=[
           "github://python/daily",
           "hn://",
           "rss://https://blog.example.com/feed"
       ]
   )

2. Set up cron job:
   cron(action="add", job={
       "name": "Weekly Newsletter",
       "schedule": {
           "kind": "cron",
           "expr": "0 9 * * 5",  # Every Friday at 9 AM
           "tz": "UTC"
       },
       "sessionTarget": "isolated",
       "payload": {
           "kind": "agentTurn",
           "message": "Generate and publish weekly newsletter",
           "timeoutSeconds": 300
       }
   })

3. The agent will automatically:
   - Collect content every Friday
   - Analyze with AI
   - Generate newsletter
   - Publish to GitHub/Telegram/Email
"""

if __name__ == "__main__":
    # Test run
    agent = NewsletterAgent(
        sources=[
            "github://python/daily",
            "hn://"
        ]
    )
    
    newsletter = agent.run(channels=["github"])
    print("\n" + "="*50)
    print("Generated Newsletter:")
    print("="*50)
    print(newsletter)
