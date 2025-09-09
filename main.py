# main.py (Updated)
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from agents.news_agent import NewsScoutAgent
from agents.github_agent import GithubScoutAgent
from agents.arxiv_agent import ArxivScoutAgent
from agents.synthesis_agent import SynthesisAgent
from agents.startup_finder_agent import StartupFinderAgent
from agents.verification_agent import VerificationAgent
from orchestrator import Orchestrator
from config import PROJECT_ID, LOCATION, NEWS_API_KEY, GITHUB_TOKEN

def initialize_system():
    """Initializes Vertex AI and the Gemini model."""
    print("Initializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    generation_config = GenerationConfig(
        temperature=0.6,
        top_p=0.95,
        max_output_tokens=8192,
    )
    
    model = GenerativeModel(
        "gemini-2.5-pro",
        generation_config=generation_config
    )
    print("Vertex AI and Gemini 2.5 Pro model initialized.")
    return model

def check_prerequisites():
    """Checks if necessary API keys are set in the environment."""
    if not NEWS_API_KEY or not GITHUB_TOKEN:
        print("\n" + "="*60)
        print("!!! PREREQUISITE ERROR !!!")
        print("Please create a .env file and set your NEWS_API_KEY and GITHUB_TOKEN.")
        print("="*60)
        return False
    return True

if __name__ == "__main__":
    if check_prerequisites():
        # Initialize the core model once
        gemini_model = initialize_system()

        # Instantiate all agents, passing the shared model
        news_agent = NewsScoutAgent(model=gemini_model)
        github_agent = GithubScoutAgent(model=gemini_model)
        arxiv_agent = ArxivScoutAgent(model=gemini_model)
        synthesis_agent = SynthesisAgent(model=gemini_model)
        startup_finder_agent = StartupFinderAgent(model=gemini_model)
        verification_agent = VerificationAgent(model=gemini_model)

        # Create the orchestrator with all the agents
        orchestrator = Orchestrator(
            news_scout=news_agent,
            github_scout=github_agent,
            arxiv_scout=arxiv_agent,
            synthesis_agent=synthesis_agent,
            startup_finder=startup_finder_agent,
            verification_agent=verification_agent
        )
        
        # Run the entire pipeline
        final_verified_report = orchestrator.run()
        
        print("\n" + "="*60)
        print("FINAL VERIFIED REPORT")
        print("="*60)
        print(final_verified_report)