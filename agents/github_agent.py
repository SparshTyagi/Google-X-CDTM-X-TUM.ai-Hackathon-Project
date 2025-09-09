# File: agents/github_agent.py
# This agent scans GitHub for new, fast-growing repositories to spot emerging technical trends.

import requests
import json
from datetime import datetime, timedelta
from .base_agent import Agent
from config import GITHUB_TOKEN
from vertexai.generative_models import GenerativeModel

class GithubScoutAgent(Agent[str, str]):
    """
    Scans GitHub for new repositories gaining traction within a specific
    technical area of interest.
    """
    def __init__(self, model: GenerativeModel):
        self.model = model

    def execute(self, interest_area: str) -> str:
        """
        Runs the full pipeline: strategize -> collect -> analyze.
        Returns a string report of the discovered technical trends.
        """
        print("[GithubScoutAgent] Starting scan...")

        # Step 1: Generate a technical search strategy.
        strategy_prompt = f"""
        For the broad technical area of "{interest_area}", generate 5 specific and technical search queries for the GitHub API. 
        Focus on nascent technologies, new libraries, or emerging architectural patterns.
        
        Return only the 5 queries, one per line.
        """
        strategy_response = self.model.generate_content(strategy_prompt)
        queries = [q.strip() for q in strategy_response.text.strip().split('\n') if q.strip()]

        if not queries:
            print("[GithubScoutAgent] Could not generate a search strategy.")
            return "No GitHub trends found: failed to generate search strategy."

        # Step 2: Collect data from GitHub API.
        all_repos = []
        print(f"[GithubScoutAgent] Executing strategy with queries: {queries}")
        for query in queries:
            raw_data, error = self._search_github(query, days_ago=90, min_stars=20)
            if error:
                print(f"[GithubScoutAgent] Error searching GitHub for '{query}': {error}")
                continue
            if raw_data:
                all_repos.extend(self._parse_repos(raw_data))

        unique_repos = list({repo['name']: repo for repo in all_repos}.values())
        if not unique_repos:
            print("[GithubScoutAgent] No emerging repositories found for the generated queries.")
            return "No emerging GitHub repositories found."

        # Step 3: Synthesize collected data into a trend report.
        analysis_prompt = f"""
        As a principal engineer interested in "{interest_area}", analyze this list of new GitHub repositories.
        Identify the top 2-3 most significant technical trends.
        A trend is a pattern of multiple new tools being created to solve a similar new problem.
        For each trend, describe the signal and why it's gaining traction now.

        Repository Data:
        {json.dumps(unique_repos, indent=2)}
        """
        analysis_response = self.model.generate_content(analysis_prompt)
        print("[GithubScoutAgent] Scan complete.")
        return analysis_response.text

    def _search_github(self, query, days_ago, min_stars):
        """Helper function to call the GitHub Search API."""
        if not GITHUB_TOKEN:
            return None, "GITHUB_TOKEN not set in config or .env file."
        
        date_threshold = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        api_query = f"{query} created:>{date_threshold} stars:>{min_stars}"
        url = "https://api.github.com/search/repositories"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        params = {
            "q": api_query,
            "sort": "stars",
            "order": "desc",
            "per_page": 25 # Get top 25 per query
        }
        try:
            res = requests.get(url, headers=headers, params=params)
            res.raise_for_status()
            return res.json(), None
        except requests.exceptions.RequestException as e:
            return None, str(e)
    
    def _parse_repos(self, api_response):
        """Helper function to parse the GitHub API JSON response."""
        if not api_response or 'items' not in api_response:
            return []
        
        return [
            {
                'name': item.get('full_name'),
                'stars': item.get('stargazers_count'),
                'description': item.get('description', 'N/A')
            }
            for item in api_response['items']
        ]