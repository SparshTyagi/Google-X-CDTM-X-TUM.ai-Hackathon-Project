# File: agents/final_report_agent.py

import json
from typing import List
from .base_agent import Agent
from vertexai.generative_models import GenerativeModel

class FinalReportAgent(Agent[List[str], str]):
    """
    This agent takes all the raw reports from the scouts and synthesizes them
    into the final, nested JSON structure required by the frontend.
    It combines synthesis, startup finding, and verification in one powerful step.
    """
    def __init__(self, model: GenerativeModel):
        self.model = model

    def execute(self, raw_reports: List[str]) -> str:
        print("[FinalReportAgent] Starting final synthesis for frontend...")
        
        combined_context = "\n\n---\n\n".join(raw_reports)
        
        prompt = f"""
        You are a world-class venture capital strategist responsible for creating the final investment report. You have received raw intelligence from your market news, open-source, and academic research divisions.

        Your task is to synthesize all this information into a single, cohesive, and deeply nested JSON object that conforms to the exact schema required by our web application.

        **JSON SCHEMA REQUIREMENTS:**
        The final output MUST be a JSON object with a single top-level key: "trends".
        "trends" is a list of Trend objects.
        A Trend object has:
        - `id`: A unique, URL-friendly string (e.g., "generative-physical-ai").
        - `name`: A short, descriptive name (e.g., "Generative AI for Physical Engineering").
        - `description`: A 2-3 sentence summary of the trend's investment thesis.
        - `importance`: An integer score from 1 to 10 on its disruptive potential.
        - `subtrends`: A list of Subtrend objects related to this Trend.
        
        A Subtrend object has:
        - `id`: A unique, URL-friendly string (e.g., "ai-drug-discovery").
        - `name`: A short, descriptive name (e.g., "AI-Powered Drug Discovery").
        - `description`: A 1-2 sentence summary of this specific niche.
        - `startups`: A list of real-world, early-stage Startup objects in this niche.

        A Startup object has:
        - `name`: The official name of the startup (e.g., "Recursion Pharmaceuticals").
        - `summary`: A one-sentence description of what the startup does.
        - `rationale`: A brief explanation of why this startup is a key player in this subtrend.

        **YOUR TASK:**
        1.  Analyze all the raw intelligence provided below.
        2.  Identify the top 2-3 most powerful "meta-trends" that emerge from the combined data.
        3.  For each meta-trend, identify 2-3 specific "subtrends" or niches.
        4.  For each subtrend, find 2-3 real, early-stage startups from your knowledge base.
        5.  Construct the final JSON object strictly following the schema described above. Do not add any extra commentary outside the JSON structure.

        **RAW INTELLIGENCE REPORTS:**
        ---
        {combined_context}
        ---

        Now, produce ONLY the final JSON object.
        """
        
        response = self.model.generate_content(prompt)
        print("[FinalReportAgent] Final report generated.")
        
        # Clean up the response to ensure it's valid JSON
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
        
        try:
            # Validate and format the JSON for clean output
            parsed_json = json.loads(cleaned_text)
            return json.dumps(parsed_json, indent=2)
        except json.JSONDecodeError:
            print("[FinalReportAgent] CRITICAL ERROR: LLM did not return valid JSON. This will cause frontend errors.")
            return '{"trends": []}' # Return a valid empty state on failure