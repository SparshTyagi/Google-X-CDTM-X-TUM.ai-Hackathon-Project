# File: agents/arxiv_agent.py
# This agent scans the arXiv research paper repository for early, foundational technology signals.

import requests
import xml.etree.ElementTree as ET
import time
import json
from .base_agent import Agent
from vertexai.generative_models import GenerativeModel

class ArxivScoutAgent(Agent[str, str]):
    """
    Scans arXiv for recent research papers to identify early-stage scientific
    and technological breakthroughs based on a VC investment persona.
    """
    def __init__(self, model: GenerativeModel):
        self.model = model

    def execute(self, vc_persona: str) -> str:
        """
        Runs the full pipeline: strategize -> collect -> analyze.
        Returns a string report of the discovered research trends.
        """
        print("[ArxivScoutAgent] Starting scan...")
        
        # Step 1: Generate a research discovery strategy.
        strategy_prompt = f"""
        Based on this VC Persona, generate a research discovery strategy with 5 diverse arXiv search queries (using categories like 'cat:cs.AI' or keywords).
        The goal is to find early, fundamental research signals that could lead to future startups.

        VC Persona: "{vc_persona}"

        Return only the 5 search queries, one per line.
        """
        strategy_response = self.model.generate_content(strategy_prompt)
        queries = [q.strip() for q in strategy_response.text.strip().split('\n') if q.strip()]

        if not queries:
            print("[ArxivScoutAgent] Could not generate a search strategy.")
            return "No research trends found: failed to generate search strategy."

        # Step 2: Collect data from the arXiv API.
        all_papers = []
        print(f"[ArxivScoutAgent] Executing strategy with queries: {queries}")
        for query in queries[:4]: # Limit to 4 queries to keep runtime reasonable
            xml_data = self._search_arxiv(query, 150) # Fetch 150 papers per query
            if xml_data:
                all_papers.extend(self._parse_papers(xml_data))
        
        if not all_papers:
            print("[ArxivScoutAgent] No papers found for the generated queries.")
            return "No research trends found: API returned no papers."

        # Step 3: Synthesize findings into a trend report.
        analysis_prompt = f"""
        As a deep-tech VC analyst with this persona: "{vc_persona}", analyze the titles of the following recent research papers from arXiv.
        Identify the top 2-3 most compelling, granular, and specific emerging patterns that could become major investment opportunities.
        Ignore well-known trends. Focus on what is truly new and foundational. For each, describe the research signal and its potential commercial application.

        Research Papers Data (Title and Date):
        {json.dumps(all_papers[:300], indent=2)} 
        """
        analysis_response = self.model.generate_content(analysis_prompt)
        print("[ArxivScoutAgent] Scan complete.")
        return analysis_response.text

    def _search_arxiv(self, query, max_results):
        """Helper function to call the arXiv API."""
        base_url = "http://export.arxiv.org/api/query?"
        params = {
            'search_query': query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        url = base_url + '&'.join([f"{k}={v}" for k, v in params.items()])
        try:
            response = requests.get(url)
            response.raise_for_status()
            time.sleep(1) # Be a good API citizen
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[ArxivScoutAgent] API request failed for query '{query}': {e}")
            return ""

    def _parse_papers(self, xml_data):
        """Helper function to parse the XML response from arXiv."""
        try:
            root = ET.fromstring(xml_data)
            papers = []
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns):
                papers.append({
                    'title': entry.find('atom:title', ns).text.strip(),
                    'published': entry.find('atom:published', ns).text[:10]
                })
            return papers
        except ET.ParseError as e:
            print(f"[ArxivScoutAgent] Failed to parse XML: {e}")
            return []