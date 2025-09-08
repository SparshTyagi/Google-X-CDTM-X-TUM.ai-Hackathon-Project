#
# An AI Agent for Discovering Nascent, Cross-Domain Market Trends for VCs
#
# This agent is designed to overcome the limitation of a single-topic focus.
# It broadly scans multiple key market sectors, then uses advanced reasoning
# to find the hidden, investable trends emerging at the *intersections* of those sectors.
#

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import requests
import json
import os
import time

# --- Configuration ---

# 1. Google Cloud & Vertex AI Configuration
PROJECT_ID = "tum-cdtm25mun-8789"  # Your Google Cloud project ID
LOCATION = "global"             # The location for Vertex AI

# 2. NewsAPI.org Configuration
from secrets import NEWS_API_KEY


# --- Initialization ---

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Configure the Gemini 2.5 Pro model for deep reasoning and synthesis
generation_config = GenerationConfig(
    temperature=0.5, # Lower temperature for more focused, factual synthesis
    top_p=0.95,
    max_output_tokens=8192,
)

model = GenerativeModel(
    "gemini-2.5-pro",
    generation_config=generation_config
)

# --- Core Functions ---

def fetch_news_from_sector(query, page_size=100):
    """
    Searches NewsAPI.org for a given query string.
    """
    if not NEWS_API_KEY:
        return None, "NEWS_API_KEY environment variable not set."

    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'pageSize': page_size,
        'sortBy': 'relevancy', # Sort by relevance to the query
        'language': 'en',
        'apiKey': NEWS_API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        time.sleep(1) # Be respectful to the API
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"API request failed for query '{query}': {e}"

def parse_articles_for_synthesis(api_response):
    """
    Parses NewsAPI response, keeping only essential info for trend analysis.
    """
    if not api_response or 'articles' not in api_response:
        return []
    
    # We only need the title and a snippet for the synthesis model
    return [
        {'title': entry.get('title', '')}
        for entry in api_response['articles']
        if entry.get('title') and '[Removed]' not in entry.get('title')
    ]

def discover_market_trends(vc_persona):
    """
    Main agent function: Scans the market, synthesizes data, and identifies
    top 3 emerging, investable trends.
    """
    # === STEP 1: GENERATE BROAD MARKET SCANNING STRATEGY ===
    # Instead of taking a user topic, the agent uses its VC persona to decide
    # which broad sectors to scan for signals of innovation and disruption.
    strategy_prompt = f"""
    <thinking>
    My goal is to find *nascent*, *investable* trends. A single search is useless. I need to scan the fundamental pillars of the modern economy and technology landscape.
    1.  I need to cover core technology advancements (AI, computing, software).
    2.  I must look at applied sciences where tech creates massive value (Biotech, Health).
    3.  I need to track the flow of money and new business models (Fintech, Venture Capital).
    4.  I must consider macro shifts in physical industries (Energy, Climate Tech, Supply Chain).
    5.  I will create distinct, high-signal search queries for each of these pillars. This will create a diverse dataset perfect for finding non-obvious connections.
    </thinking>

    VC Persona: "{vc_persona}"

    Based on this persona, generate 5 diverse, high-level search queries for a news API. These queries should be designed to scan the entire market for early signals of technological and economic shifts. Use boolean operators (AND, OR, NOT) to make the queries precise.

    Return only the 5 search queries, one per line.
    """
    print("Step 1: Generating broad market scanning strategy...")
    strategy_response = model.generate_content(strategy_prompt)
    market_scan_queries = [q.strip() for q in strategy_response.text.strip().split('\n') if q.strip()]

    if not market_scan_queries:
        return "Error: Could not generate a market scanning strategy."

    print(f"Strategy Generated. Scanning the following sectors:\n- " + "\n- ".join(market_scan_queries))

    # === STEP 2: DIVERSE DATA COLLECTION ===
    # The agent executes the broad strategy, collecting headlines from each pillar.
    all_headlines = []
    print("\nStep 2: Collecting market signals from diverse sectors...")
    for query in market_scan_queries:
        print(f"  -> Scanning sector with query: '{query}'")
        raw_data, error = fetch_news_from_sector(query, 75) # Fetch 75 headlines per sector
        if error:
            print(f"     Error: {error}")
            continue
        if raw_data:
            parsed_data = parse_articles_for_synthesis(raw_data)
            # Add sector context to each headline for the model
            for headline in parsed_data:
                headline['sector_query'] = query
            all_headlines.extend(parsed_data)
            print(f"     Collected {len(parsed_data)} signals.")

    if not all_headlines:
        return "Analysis failed: No market signals could be collected."

    print(f"\nTotal unique signals collected for synthesis: {len(all_headlines)}")

    # === STEP 3: CROSS-DOMAIN SYNTHESIS & TREND DISCOVERY ===
    # This is the core reasoning step. The model analyzes the entire, diverse
    # dataset to find connections *between* the sectors.
    analysis_prompt = f"""
    <thinking>
    I am a top-tier VC analyst. I have just received a raw feed of {len(all_headlines)} headlines from across the entire market (tech, bio, finance, energy, etc.). My task is not to summarize each sector, but to find the *hidden connections between them*.
    1.  First, I will scan all headlines and mentally cluster them by underlying technology or concept, regardless of the sector they came from. For example, 'AI', 'genomics', 'decentralization', 'new materials'.
    2.  Next, I will look for the most interesting *intersections* of these clusters. Where is a concept from one cluster starting to appear in another? (e.g., AI headlines showing up in the 'genomics' cluster). These intersections are the source of new trends.
    3.  I must filter out the noise. I will IGNORE well-established mega-trends (e.g., "AI is growing", "EVs are popular"). I am looking for what's *next*.
    4.  For each potential trend, I will ask: "Is this specific, is it new, and does it have the potential for venture-scale returns?"
    5.  I will then synthesize my findings into a concise, actionable briefing for my partners, focusing on the "alpha" - the information that other VCs might have missed.
    </thinking>

    VC Analyst Persona: "{vc_persona}"

    Analyze this raw feed of market signals from multiple sectors to identify the top 3 most promising, under-the-radar, and investable trends.

    Raw Market Signals (Headlines):
    {json.dumps(all_headlines, indent=2)}

    For each of the 3 trends you identify, structure your analysis as follows:

    **Trend:** A concise, descriptive name for the trend (e.g., "Generative AI for Physical Engineering").
    
    **The Signal:** Explain the pattern you detected across the different news sectors. What is the core insight? What pieces of evidence from the headlines point to this emerging intersection? Be specific.
    
    **Why It Matters (The VC Angle):** Explain why this is a compelling trend for an early-stage VC. What is the potential market size or disruption? What old industries could be upended?
    
    **Early Indicators & Key Players:** Mention any companies or types of technologies from the headlines that are early indicators of this trend taking hold.
    """

    print("\nStep 3: Performing cross-domain synthesis to discover emerging trends... (this may take a minute or two)")
    analysis_response = model.generate_content(analysis_prompt)
    return analysis_response.text

# --- Main Execution Block ---
if __name__ == "__main__":
    if not NEWS_API_KEY:
        print("="*60)
        print("!!! SETUP REQUIRED !!!")
        print("Please get a free API key from https://newsapi.org")
        print("Then set it as an environment variable named 'NEWS_API_KEY'.")
        print("="*60)
    else:
        # Define the persona of the VC. The agent will tailor its search and analysis to this.
        vc_persona = """
        Early-stage, deep-tech venture capital firm. We invest in foundational technologies
        that can create new markets or radically disrupt existing ones. We are comfortable
        with technical risk and long development cycles. We look for defensible 'moats'
        built on novel science or engineering. We are particularly interested in the
        intersections of software (AI/ML), biology, and advanced materials.
        """

        print("="*60)
        print("=== AI MARKET TREND DISCOVERY AGENT (for VCs) ===")
        print("Using Gemini 2.5 Pro for broad market scanning and synthesis...")
        print("="*60)

        # Run the agent
        result = discover_market_trends(vc_persona)

        print("\n" + "="*60)
        print("EMERGING TRENDS BRIEFING:")
        print("="*60)
        print(result)