# orchestrator.py (Updated)
import json
from agents.news_agent import NewsScoutAgent
from agents.github_agent import GithubScoutAgent
from agents.arxiv_agent import ArxivScoutAgent
from agents.synthesis_agent import SynthesisAgent
from agents.startup_finder_agent import StartupFinderAgent
from agents.verification_agent import VerificationAgent
from config import VC_PERSONA, GITHUB_INTEREST_AREA

class Orchestrator:
    def __init__(
        self,
        news_scout: NewsScoutAgent,
        github_scout: GithubScoutAgent,
        arxiv_scout: ArxivScoutAgent,
        synthesis_agent: SynthesisAgent,
        startup_finder: StartupFinderAgent,
        verification_agent: VerificationAgent
    ):
        self.news_scout = news_scout
        self.github_scout = github_scout
        self.arxiv_scout = arxiv_scout
        self.synthesis_agent = synthesis_agent
        self.startup_finder = startup_finder
        self.verification_agent = verification_agent

    def run(self):
        """
        Executes the full, multi-stage trend analysis and verification pipeline.
        """
        print("[Orchestrator] Starting full trend discovery and verification process...")

        # --- 1. Scout for raw signals from all sources ---
        news_report = self.news_scout.execute(VC_PERSONA)
        github_report = self.github_scout.execute(GITHUB_INTEREST_AREA)
        arxiv_report = self.arxiv_scout.execute(VC_PERSONA)
        
        all_reports = [news_report, github_report, arxiv_report]

        # --- 2. Synthesize raw signals into top trends ---
        synthesis_json_str = self.synthesis_agent.execute(all_reports)
        try:
            synthesized_data = json.loads(synthesis_json_str)
        except json.JSONDecodeError:
            print("[Orchestrator] Fatal Error: Synthesis agent did not return valid JSON. Aborting.")
            return
        
        # --- 3. Find relevant startups for each top trend ---
        # We will build our final report object in this step
        final_report = {"trends": []}
        if "top_trends" in synthesized_data and isinstance(synthesized_data["top_trends"], list):
            for trend_obj in synthesized_data["top_trends"]:
                trend_name = trend_obj.get("trend_name")
                if not trend_name:
                    continue

                startups_json_str = self.startup_finder.execute(trend_name)
                try:
                    startups_data = json.loads(startups_json_str)
                    trend_obj["startups"] = startups_data.get("startups", [])
                except json.JSONDecodeError:
                    trend_obj["startups"] = []
                
                final_report["trends"].append(trend_obj)
        
        # --- 4. Perform final verification of the entire report ---
        verified_report_json_str = self.verification_agent.execute(final_report)
        
        # --- 5. Save the final, verified result ---
        output_filename = "verified_trends_report.json"
        try:
            with open(output_filename, "w") as f:
                f.write(verified_report_json_str)
            print(f"\n[Orchestrator] Process complete. Final verified report saved to {output_filename}")
        except Exception as e:
            print(f"Error saving final report: {e}")
            
        return verified_report_json_str