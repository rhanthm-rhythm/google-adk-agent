# app06/hooks/tool_callbacks.py
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import ToolContext
import re
from urllib.parse import urlparse

WHITELIST_DOMAINS = ["techcrunch.com", "venturebeat.com", "theverge.com", "technologyreview.com", "arstechnica.com"]

def filter_news_sources_callback(tool, args, tool_context):
    """Callback to enforce that google_search queries only use whitelisted domains."""
    if tool.name == "google_search":
        original_query = args.get("query", "")
        if any(f"site:{domain}" in original_query.lower() for domain in WHITELIST_DOMAINS):
            return None
        whitelist_query_part = " OR ".join([f"site:{domain}" for domain in WHITELIST_DOMAINS])
        args['query'] = f"{original_query} {whitelist_query_part}"
        print(f"MODIFIED query to enforce whitelist: '{args['query']}'")
    return None

def enforce_data_freshness_callback(tool, args, tool_context):
    """Callback to add a time filter to search queries to get recent news."""
    if tool.name == "google_search":
        query = args.get("query", "")
        # Adds a Google search parameter to filter results from the last week.
        if "tbs=qdr:w" not in query:
            args['query'] = f"{query} tbs=qdr:w"
            print(f"MODIFIED query for freshness: '{args['query']}'")
    return None


def initialize_process_log(tool_context: ToolContext):
    """Helper to ensure the process_log list exists in the state."""
    if 'process_log' not in tool_context.state:
        tool_context.state['process_log'] = []

def inject_process_log_after_search(tool, args, tool_context, tool_response):
    """
    Callback: After a successful search, this injects the process_log into the response
    and adds a specific note about which domains were sourced. This makes the callbacks'
    actions visible to the LLM.
    """
    if tool.name == "google_search" and isinstance(tool_response, str):
        # Extract source domains from the search results
        urls = re.findall(r'https?://[^\s/]+', tool_response)
        unique_domains = sorted(list(set(urlparse(url).netloc for url in urls)))
        
        if unique_domains:
            sourcing_log = f"Action: Sourced news from the following domains: {', '.join(unique_domains)}."
            # Prepend the new log to the existing one for better readability in the report
            current_log = tool_context.state.get('process_log', [])
            tool_context.state['process_log'] = [sourcing_log] + current_log

        final_log = tool_context.state.get('process_log', [])
        print(f"CALLBACK LOG: Injecting process log into tool response: {final_log}")
        return {
            "search_results": tool_response,
            "process_log": final_log
        }
    return tool_response