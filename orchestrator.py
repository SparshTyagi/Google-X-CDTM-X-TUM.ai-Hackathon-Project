# orchestrator.py (Updated)
import json
from agents.news_agent import NewsScoutAgent
from agents.github_agent import GithubScoutAgent
from agents.arxiv_agent import ArxivScoutAgent
# Import the new final agent
from agents.final_report_agent import FinalReportAgent
from config import VC_PERSONA, GITHUB_INTEREST_AREA

class Orchestrator:
    def __init__(
        self,
        news_scout: NewsScoutAgent,
        github_scout: GithubScoutAgent,
        arxiv_scout: ArxivScoutAgent,
        final_report_agent: FinalReportAgent # Use the new agent
    ):
        self.news_scout = news_scout
        self.github_scout = github_scout
        self.arxiv_scout = arxiv_scout
        self.final_report_agent = final_report_agent

    def run(self):
        """
        Executes the full pipeline and generates a single, structured report for the frontend.
        """
        print("[Orchestrator] Starting full trend discovery process...")

        # --- 1. Scout for raw signals ---
        news_report = self.news_scout.execute(VC_PERSONA)
        github_report = self.github_scout.execute(GITHUB_INTEREST_AREA)
        arxiv_report = self.arxiv_scout.execute(VC_PERSONA)
        
        all_reports = [news_report, github_report, arxiv_report]

        # --- 2. Generate the final, frontend-compatible report ---
        final_report_json_str = self.final_report_agent.execute(all_reports)

        output_filename = "final_verified_trends_report.json"
        
        with open(output_filename, "w") as f:
            f.write(final_report_json_str)
        print(f"\n[Orchestrator] Process complete. Final verified report saved to {output_filename}")
    
        print(f"\n[Orchestrator] Process complete.")
        return final_report_json_str