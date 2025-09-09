# agents/synthesis_agent.py
from typing import List
import json
from .base_agent import Agent
from vertexai.generative_models import GenerativeModel

class SynthesisAgent(Agent[List[str], str]):
    def __init__(self, model: GenerativeModel):
        self.model = model

    def execute(self, trend_reports: List[str]) -> str:
        print("[SynthesisAgent] Synthesizing findings from all scouts...")
        
        # Combine all individual reports into one context block
        combined_context = "\n\n---\n\n".join(trend_reports)
        
        prompt = f"""
        You are a world-class venture capital strategist. You have received raw intelligence reports from three different divisions: Market News, Open-Source Technology, and Academic Research.

        Your task is to synthesize these disparate reports into a single, cohesive, and actionable investment thesis. Identify the most powerful "meta-trends" that emerge when you connect the dots between the reports.

        RULES:
        1.  Do not just summarize each report. Find the *intersections* and *reinforcing patterns* between them. For example, if a new algorithm appears in research papers and you also see new open-source tools being built for it, that is a powerful meta-trend.
        2.  Filter out noise and weak signals. Focus on the 2-3 most dominant and commercially viable trends.
        3.  For each meta-trend, provide a clear and compelling investment thesis.
        4.  Rank the trends from most to least important based on their potential for disruption and venture-scale returns.
        5.  Return the final output as a JSON object string. The JSON should have a single key "top_trends", which is a list of objects. Each object must have three keys: "rank" (integer), "trend_name" (string), and "investment_thesis" (string, a 2-3 sentence summary).

        Here are the raw intelligence reports:
        ---
        {combined_context}
        ---

        Now, produce the final synthesized JSON object.
        """
        
        synthesis_response = self.model.generate_content(prompt)
        print("[SynthesisAgent] Synthesis complete.")
        
        # Clean up the response to ensure it's valid JSON
        cleaned_text = synthesis_response.text.strip().replace("```json", "").replace("```", "")
        
        try:
            # Validate and format the JSON
            parsed_json = json.loads(cleaned_text)
            return json.dumps(parsed_json, indent=2)
        except json.JSONDecodeError:
            print("[SynthesisAgent] Warning: LLM did not return valid JSON. Returning raw text.")
            return cleaned_text