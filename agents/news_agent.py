# File: agents/news_agent.py
# This agent scans news headlines to identify emerging market and business trends.

import requests
import json
import time
from .base_agent import Agent
from config import NEWS_API_KEY
from vertexai.generative_models import GenerativeModel

class NewsScoutAgent(Agent[str, str]):
    """
    Scans news sources via NewsAPI to find high-level market trends
    based on a provided VC investment persona.
    """
    def __init__(self, model: GenerativeModel):
        self.model = model

    def execute(self, vc_persona: str) -> str:
        """
        Runs the full pipeline: strategize -> collect -> analyze.
        Returns a string report of the discovered trends.
        """
        print("[NewsScoutAgent] Starting scan...")
        
        # Step 1: Generate a dynamic search strategy based on the VC persona.
        strategy_prompt = f"""
        Based on this VC Persona, generate 4 diverse, high-level news queries to scan for early signals of technological and economic shifts.
        Focus on creating queries that are precise and use boolean operators (AND, OR) to find high-signal results.

        VC Persona: "{vc_persona}"

        Return only the 4 search queries, one per line.
        """
        strategy_response = self.model.generate_content(strategy_prompt)
        queries = [q.strip() for q in strategy_response.text.strip().split('\n') if q.strip()]
        
        if not queries:
            print("[NewsScoutAgent] Could not generate a search strategy.")
            return "No news signals found: failed to generate search strategy."

        # Step 2: Collect data from NewsAPI using the generated strategy.
        all_headlines = []
        print(f"[NewsScoutAgent] Executing strategy with queries: {queries}")
        for query in queries:
            raw_data, error = self._fetch_news(query, 50) # Fetch 50 articles per query
            if error:
                print(f"[NewsScoutAgent] Error fetching news for '{query}': {error}")
                continue
            if raw_data:
                all_headlines.extend(self._parse_articles(raw_data))
        
        if not all_headlines:
            print("[NewsScoutAgent] No articles found for the generated queries.")
            return "No news signals found: API returned no articles."

        # Step 3: Use the LLM to synthesize the collected headlines into a trend report.
        analysis_prompt = f"""
        As a VC analyst with this persona: "{vc_persona}", analyze the following news headlines.
        Identify the top 2-3 most promising, under-the-radar, and investable trends.
        For each trend, briefly describe the signal and its VC angle.

        Headlines:
        {json.dumps(all_headlines, indent=2)}
        """
        analysis_response = self.model.generate_content(analysis_prompt)
        print("[NewsScoutAgent] Scan complete.")
        return analysis_response.text

    def _fetch_news(self, query, page_size):
        """Helper function to call the NewsAPI."""
        if not NEWS_API_KEY:
            return None, "NEWS_API_KEY not set in config or .env file."
            
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': query,
            'pageSize': page_size,
            'sortBy': 'relevancy',
            'language': 'en',
            'apiKey': NEWS_API_KEY
        }
        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            time.sleep(1) # Be a good API citizen
            return res.json(), None
        except requests.exceptions.RequestException as e:
            return None, str(e)

    def _parse_articles(self, api_response):
        """Helper function to parse the NewsAPI JSON response."""
        if not api_response or 'articles' not in api_response:
            return []
        # We only need the title for the synthesis model to find patterns.
        return [
            {'title': entry.get('title', '')}
            for entry in api_response['articles']
            if entry.get('title') and '[Removed]' not in entry.get('title')
        ]