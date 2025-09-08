import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import requests
import xml.etree.ElementTree as ET
import time

# Initialize Vertex AI with the latest model
project_id = "tum-cdtm25mun-8789"  
location = "global"
vertexai.init(project=project_id, location=location)

# Use Gemini 2.5 Pro - the latest reasoning model
generation_config = GenerationConfig(
    temperature=0.7,  # Encourage creative thinking
    top_p=0.95,
    max_output_tokens=8192,  # Allow longer responses
)

model = GenerativeModel(
    "gemini-2.5-pro",
    generation_config=generation_config
)

def search_arxiv_broad(query, max_results=1000):
    """Search arXiv with larger result sets"""
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    url = base_url + '&'.join([f"{k}={v}" for k, v in params.items()])
    response = requests.get(url)
    time.sleep(1)  # Be respectful to arXiv API
    return response.text

def discover_vc_trends(vc_context):
    """Main function: takes VC context, discovers unknown trends"""
    
    # Step 1: Generate discovery strategy based on VC context
    strategy_prompt = f"""
    <thinking>
    I need to carefully analyze this VC's investment thesis and portfolio to understand:
    1. What sectors they focus on
    2. What stage companies they target
    3. What problems they're trying to solve
    4. What adjacent areas might be emerging that they haven't considered yet
    
    Let me think about what research areas might reveal early signals of opportunities in their space.
    I should look beyond obvious categories and think about interdisciplinary combinations.
    </thinking>
    
    VC Context: {vc_context}
    
    Based on this VC's investment focus, generate a comprehensive research discovery strategy.
    
    Create:
    1. 5 broad arxiv search categories (like 'cat:cs.AI' or 'cat:physics.bio-ph') 
    2. 3 keyword patterns that might reveal adjacent/emerging fields
    3. 2 interdisciplinary combinations the VC might not have considered
    
    Focus on finding early research signals that could become commercial opportunities.
    Return only the search queries, one per line.
    """
    
    print("Generating discovery strategy...")
    strategy = model.generate_content(strategy_prompt)
    search_queries = [q.strip() for q in strategy.text.strip().split('\n') if q.strip()]
    
    print(f"Discovery strategy: {search_queries}")
    
    # Step 2: Massive data collection
    all_papers = []
    for query in search_queries[:3]:  # Limit to avoid timeout
        print(f"Collecting papers for: {query}")
        xml_data = search_arxiv_broad(query, 500)  # Much larger dataset
        papers = parse_papers_detailed(xml_data)
        all_papers.extend(papers)
    
    print(f"Collected {len(all_papers)} papers for analysis")
    
    # Step 3: Deep pattern discovery analysis with enhanced reasoning
    analysis_prompt = f"""
    <thinking>
    I need to deeply analyze this research data to find truly emerging trends. Let me think through this systematically:

    1. Pattern Recognition: What new research combinations are appearing that weren't common before?
    2. Cross-Disciplinary Bridges: What fields are starting to intersect in novel ways?
    3. Problem-Solution Evolution: What new approaches to old problems are emerging?
    4. Commercial Potential: Which research directions could realistically become businesses this VC would invest in?
    5. Timing Analysis: What seems to be gaining momentum recently vs. established trends?

    I should look for:
    - Sudden clusters of papers around new methodologies
    - Researchers from different fields collaborating on similar problems
    - New technical approaches that solve practical business problems
    - Early-stage research that could become mainstream in 2-3 years

    Let me carefully examine the data for these signals before providing insights.
    </thinking>
    
    VC Investment Context: {vc_context}
    
    Analyze these {len(all_papers)} recent research papers to discover UNKNOWN emerging trends that could become major investment opportunities.
    
    Research Papers Data: {str(all_papers[:200])}  # Send subset to avoid token limits
    
    Take your time to identify patterns that indicate:
    1. Completely new research combinations appearing frequently
    2. Sudden increases in specific technical approaches
    3. Cross-disciplinary bridges forming between previously separate fields
    4. Technologies solving practical problems this VC's portfolio companies face
    5. Early signals of what could become billion-dollar markets
    
    IGNORE well-known trends like "AI in general" or "quantum computing". 
    FOCUS on granular, specific emerging patterns that most VCs haven't noticed yet.
    
    For each trend you identify:
    - Provide concrete evidence from the research data
    - Explain why this VC should care specifically
    - Estimate timeline to commercial viability
    - Rate investment opportunity (1-10) with reasoning
    
    Return your top 3 most compelling discovery insights.
    """
    
    print("Performing deep trend analysis... (this may take 2-3 minutes)")
    analysis = model.generate_content(analysis_prompt)
    return analysis.text

def parse_papers_detailed(xml_data):
    """Extract paper details including categories and dates"""
    try:
        root = ET.fromstring(xml_data)
        papers = []
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip()
            published = entry.find('atom:published', ns).text[:10]
            
            # Get categories
            categories = []
            for cat in entry.findall('atom:category', ns):
                categories.append(cat.get('term'))
            
            papers.append({
                'title': title,
                'date': published,
                'categories': categories
            })
        
        return papers
    except Exception as e:
        print(f"Parse error: {e}")
        return []

# Test with VC context
vc_context = """
Early-stage VC focused on B2B SaaS and enterprise automation.
Portfolio: Slack, Notion, Zapier-like workflow tools.
Investment thesis: Tools that make knowledge workers 10x more productive.
Avoiding: Consumer apps, crypto, heavy hardware.
Sweet spot: $1M-$10M Series A rounds.
Looking for: Next generation of work tools, AI-assisted productivity.
"""

print("=== ENHANCED DISCOVERY-BASED VC TREND ANALYSIS ===")
print("Using Gemini 2.5 Pro with deep reasoning capabilities...")
result = discover_vc_trends(vc_context)
print("\n" + "="*60)
print("TREND DISCOVERY RESULTS:")
print("="*60)
print(result)