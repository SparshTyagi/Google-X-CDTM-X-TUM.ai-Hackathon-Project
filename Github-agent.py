#
# An AI Agent for Discovering Emerging Technical Trends on GitHub
#
# This agent identifies nascent trends by:
# 1. Strategizing technical keywords for a given area of interest.
# 2. Searching GitHub for NEW repositories that are rapidly gaining traction.
# 3. Synthesizing the findings to identify patterns and new software categories.
#

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import requests
import json
import os
from datetime import datetime, timedelta
from secretsfile import GITHUB_TOKEN

# --- Configuration ---

# 1. Google Cloud & Vertex AI Configuration
PROJECT_ID = "tum-cdtm25mun-8789"  # Your Google Cloud project ID
LOCATION = "global"             # The location for Vertex AI

# 2. GitHub API Configuration
# CRITICAL: Generate a Personal Access Token (PAT) with `public_repo` scope
# and set it as an environment variable.

# Trend Discovery Parameters
DAYS_AGO = 90  # Look for repos created in the last 90 days
MIN_STARS = 25 # Minimum stars to be considered "gaining traction" and not "garbage"

# --- Initialization ---

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Configure the Gemini 2.5 Pro model for technical analysis
generation_config = GenerationConfig(
    temperature=0.6, # A bit more deterministic for technical analysis
    top_p=0.95,
    max_output_tokens=8192,
)

model = GenerativeModel(
    "gemini-2.5-pro",
    generation_config=generation_config
)

# --- Core Functions ---

def search_github_repositories(query, days_ago, min_stars):
    """
    Searches GitHub for repositories matching specific criteria.
    Focuses on finding newly created repos with early signs of traction.
    """
    if not GITHUB_TOKEN:
        return None, "GITHUB_TOKEN environment variable is not set."

    # Calculate the date to search from
    date_threshold = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    # Construct a precise search query for the GitHub API
    # We are looking for repos with the keyword, created after our date, with a minimum number of stars.
    # We sort by stars to see the fastest-growing ones first.
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
        "per_page": 50 # Get up to 50 repos per query
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"GitHub API request failed: {e}"

def parse_github_repos(api_response):
    """
    Parses the GitHub API response to extract only the essential information
    for the LLM analysis. The README/description is the most valuable text.
    """
    if not api_response or 'items' not in api_response:
        return []
    
    repos = []
    for item in api_response['items']:
        repos.append({
            'name': item.get('full_name'),
            'stars': item.get('stargazers_count'),
            'language': item.get('language', 'N/A'),
            'description': item.get('description', 'No description provided.'),
            'url': item.get('html_url')
        })
    return repos

def discover_github_trends(area_of_interest):
    """
    Main agent function: Takes a high-level area of interest and discovers
    emerging open-source trends within it.
    """
    # === STEP 1: GENERATE TECHNICAL SEARCH STRATEGY ===
    # The agent brainstorms specific, technical sub-topics to find precise signals.
    strategy_prompt = f"""
    <thinking>
    My goal is to find emerging open-source projects on GitHub. A broad search for "{area_of_interest}" will be too noisy, filled with tutorials and old libraries.
    1. I need to break down the user's interest into specific, cutting-edge technical concepts, tools, and acronyms.
    2. What are the hot sub-fields right now? What new problems are developers trying to solve in this space?
    3. I should think about the entire lifecycle: development, deployment, observability, and tooling.
    4. I will create a list of precise search keywords that will likely surface new, high-quality projects.
    </thinking>

    Area of Interest: "{area_of_interest}"

    Based on this, generate a list of 5-7 specific, technical search queries to use with the GitHub API. These should target nascent technologies and concepts.

    Return only the search queries, one per line.
    """
    print("Step 1: Generating a technical discovery strategy for GitHub...")
    strategy_response = model.generate_content(strategy_prompt)
    search_queries = [q.strip() for q in strategy_response.text.strip().split('\n') if q.strip()]

    if not search_queries:
        return "Error: Could not generate a search strategy."

    print(f"Strategy Generated. Scanning for projects related to:\n- " + "\n- ".join(search_queries))

    # === STEP 2: DATA COLLECTION FROM GITHUB ===
    all_repos = []
    print("\nStep 2: Collecting data on emerging repositories from GitHub...")
    for query in search_queries:
        print(f"  -> Searching for: '{query}'")
        raw_data, error = search_github_repositories(query, DAYS_AGO, MIN_STARS)
        if error:
            print(f"     Error: {error}")
            continue
        if raw_data:
            parsed_data = parse_github_repos(raw_data)
            all_repos.extend(parsed_data)
            print(f"     Found {len(parsed_data)} relevant new repositories.")

    if not all_repos:
        return "Analysis failed: No emerging repositories matching the criteria were found."
    
    # De-duplicate repositories that might have been found by multiple queries
    unique_repos = list({repo['name']: repo for repo in all_repos}.values())
    print(f"\nTotal unique emerging repositories collected for analysis: {len(unique_repos)}")

    # === STEP 3: SYNTHESIS & TREND IDENTIFICATION ===
    analysis_prompt = f"""
    <thinking>
    I am a Principal Engineer analyzing a curated list of {len(unique_repos)} new, fast-growing GitHub repositories. My task is to identify the underlying technical trends.
    1. I will not just list the most popular repos. I'm looking for *patterns*.
    2. I'll scan all the repository descriptions and categorize them. Are multiple new tools solving the same emerging problem? (e.g., several new projects for 'LLM guardrails' or 'local RAG pipelines'). This signals a new category is forming.
    3. I'll look at the languages and frameworks being used. Is there a shift? (e.g., a lot of new AI tooling suddenly being written in Rust).
    4. I'll ask "Why now?". What recent advancement (e.g., release of a new AI model, a new platform feature) is causing this explosion of new tools?
    5. I will synthesize these observations into a high-level briefing for a CTO, highlighting the most actionable trends.
    </thinking>

    Original Area of Interest: "{area_of_interest}"

    Analyze this list of emerging GitHub repositories to identify the top 2-3 most significant technical trends.

    Repository Data:
    {json.dumps(unique_repos, indent=2)}

    For each trend, provide the following:
    
    **Trend:** A concise name for the emerging technical trend. (e.g., "The Rise of Specialized, Self-Hosted Vector Databases").
    
    **The Signal:** Explain the pattern you observed in the data. What problem are developers suddenly building tools for? What evidence (keywords, project descriptions) points to this?
    
    **Why It's Gaining Traction:** Explain the "why now." What is the underlying driver for this trend? Is it a reaction to the cost of existing tools, a new capability, or a common developer pain point?
    
    **Key Repositories as Evidence:** List 2-3 of the most representative repositories from the data that exemplify this trend, including their star count.
    """

    print("\nStep 3: Synthesizing data to identify emerging technical trends... (this may take a minute)")
    analysis_response = model.generate_content(analysis_prompt)
    return analysis_response.text

# --- Main Execution Block ---
if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("="*60)
        print("!!! GITHUB TOKEN REQUIRED !!!")
        print("Please generate a GitHub Personal Access Token with `public_repo` scope.")
        print("Then set it as an environment variable named 'GITHUB_TOKEN'.")
        print("="*60)
    else:
        # Define the high-level technical area you want the agent to investigate
        # Good examples: "AI Agent Frameworks", "WebAssembly tooling", "Local LLM Infrastructure", "Developer Productivity AI"
        interest_area = "The emerging stack for building and deploying AI Agents"

        print("="*60)
        print("=== AI GITHUB TREND DISCOVERY AGENT ===")
        print(f"Starting analysis for area: '{interest_area}'")
        print(f"Searching for repos created in the last {DAYS_AGO} days with >{MIN_STARS} stars.")
        print("="*60)

        # Run the agent
        result = discover_github_trends(interest_area)

        print("\n" + "="*60)
        print("EMERGING GITHUB TRENDS REPORT:")
        print("="*60)
        print(result)