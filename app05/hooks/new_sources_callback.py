
BLOCKED_DOMAINS = [
    "wikipedia.org",      # General info, not latest news
    "reddit.com",         # Discussion forums, not primary news
    "youtube.com",        # Video content not useful for text processing
    "medium.com",         # Blog platform with variable quality
    "investopedia.com",   # Financial definitions, not tech news
    "quora.com",          # Q&A site, opinions not reports
    "tsttechnology.io",
    "crescendo.ai",
    "medium.com",
]

def filter_news_sources_callback(tool, args, tool_context):
    """
    Callback: Blocks search requests that target certain domains which are not necessarily news sources.
    Demonstrates content quality enforcement through request blocking.
    """
    if tool.name == "google_search_agent":
        print("[CALLBACK-DEBUG] filter_news_sources_callback called.")
        query = args.get("request", "").lower()
        print(f"[CALLBACK-DEBUG] Original query: '{query}'")
        # Check if query explicitly targets blocked domains
        for domain in BLOCKED_DOMAINS:
            if f"site:{domain}" in query or domain.replace(".org", "").replace(".com", "") in query:
                print(f"BLOCKED: Domains from blocked list detected: '{query}'")
                return {
                    "error": "blocked_source",
                    "reason": f"Searches targeting {domain} or similar are not allowed. Please search for professional news sources."
                }

        print(f"ALLOWED: Professional source query: '{query}'")
        return None
