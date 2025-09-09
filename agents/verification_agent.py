# File: agents/verification_agent.py
# This agent performs a final review of the entire analysis for logic and accuracy.

import json
from .base_agent import Agent
from vertexai.generative_models import GenerativeModel

class VerificationAgent(Agent[dict, str]):
    """
    Acts as a final review layer. It takes the complete data structure
    (trends + startups) and adds a verification and confidence score.
    """
    def __init__(self, model: GenerativeModel):
        self.model = model

    def execute(self, full_report_data: dict) -> str:
        """
        Takes the full report as a dictionary, analyzes it, and returns the
        final, verified report as a JSON string.
        """
        print("[VerificationAgent] Starting final review of the complete report...")
        
        report_str = json.dumps(full_report_data, indent=2)

        prompt = f"""
        You are a skeptical, highly experienced senior partner at a top-tier venture capital firm. You are reviewing a trend report compiled by your junior analysts. Your job is to perform a final "red team" review for logical consistency, accuracy, and potential blind spots before it's presented to the investment committee.

        Here is the report you need to review:
        ---
        {report_str}
        ---

        Instructions:
        1.  Critically assess the entire report. Are the connections between the trends and the listed startups logical?
        2.  Is the investment thesis for each trend well-supported by the (implied) raw signals?
        3.  Identify any potential hype, buzzwords, or areas where the analysis might be too optimistic.
        4.  Based on your assessment, create a "verification_summary" object. This object must contain:
            - `confidence_score`: Your confidence in the report's overall quality and accuracy, on a scale of 1 (low) to 10 (high).
            - `assessment`: A 2-4 sentence summary of your review. What are the report's strengths and weaknesses?
            - `potential_blind_spots`: A list of 2-3 critical questions or potential risks that the analysts may have overlooked.

        Your final output must be the *original JSON report* with your new `verification_summary` object added as a top-level key. Do not modify any other part of the original report.
        """
        
        response = self.model.generate_content(prompt)
        print("[VerificationAgent] Verification complete.")

        # Clean up the response to ensure it's valid JSON
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")

        try:
            # Validate and format the JSON
            parsed_json = json.loads(cleaned_text)
            return json.dumps(parsed_json, indent=2)
        except json.JSONDecodeError:
            print("[VerificationAgent] Warning: LLM failed to return a valid final JSON. Appending verification as text.")
            full_report_data['verification_summary'] = {"assessment": "Verification failed due to LLM format error.", "raw_output": cleaned_text}
            return json.dumps(full_report_data, indent=2)