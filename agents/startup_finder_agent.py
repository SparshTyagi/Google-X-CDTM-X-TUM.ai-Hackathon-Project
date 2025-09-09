# File: agents/startup_finder_agent.py
# This agent finds early-stage startups related to a specific, identified trend.

import json
from .base_agent import Agent
from vertexai.generative_models import GenerativeModel

class StartupFinderAgent(Agent[str, str]):
    """
    Finds early-stage startups operating within a given trend.
    
    Note: This agent relies on the LLM's training data. For production use,
    integrating a real-time data source like Crunchbase or PitchBook via their APIs
    would provide more current and accurate results.
    """
    def __init__(self, model: GenerativeModel):
        self.model = model

    def execute(self, trend_name: str) -> str:
        """
        Takes a trend name and returns a JSON string of relevant startups.
        """
        print(f"[StartupFinderAgent] Searching for startups in trend: '{trend_name}'...")

        prompt = f"""
        You are a venture capital associate specializing in deep tech. Your task is to identify promising, real-world, early-stage (Seed or Series A) startups operating within a specific technological trend.

        Technological Trend: "{trend_name}"

        Instructions:
        1.  Search your knowledge base for 2-4 companies that are clear leaders or innovative players in this exact space.
        2.  For each company, provide its name, a one-sentence summary of what it does, and a brief rationale for why it's a good fit for this trend.
        3.  If you cannot find any real companies, return an empty list. Do not invent companies.
        4.  Return the result as a JSON object string. The JSON should have a single key "startups", which is a list of objects. Each object must have three keys: "name" (string), "summary" (string), and "rationale" (string).

        Example Output Format:
        {{
          "startups": [
            {{
              "name": "ExampleTech Inc.",
              "summary": "Develops a novel platform for AI-driven material discovery.",
              "rationale": "Directly applies the trend to solve a major R&D problem in manufacturing."
            }}
          ]
        }}

        Now, produce the JSON object for the specified trend.
        """
        
        response = self.model.generate_content(prompt)
        print(f"[StartupFinderAgent] Found potential startups for '{trend_name}'.")

        # Clean up the response to ensure it's valid JSON
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
        
        try:
            # Validate and return the JSON string
            json.loads(cleaned_text)
            return cleaned_text
        except json.JSONDecodeError:
            print(f"[StartupFinderAgent] Warning: LLM did not return valid JSON for trend '{trend_name}'.")
            return '{"startups": []}' # Return an empty list in case of error