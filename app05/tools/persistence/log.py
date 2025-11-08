import re
from urllib.parse import urlparse
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Dict, Any, Optional

def initialize_process_log(tool_context: ToolContext):
    """Helper to ensure the process_log list exists in the state."""
    if 'process_log' not in tool_context.state:
        tool_context.state['process_log'] = []


def extract_domains_from_grounding_metadata(response) -> list[str]:
    """
    Extract source domains from grounding metadata in agent response.
    
    Args:
        response: Agent response object with state_delta
        
    Returns:
        List of unique domain names sorted alphabetically
    """
    unique_domains = []
    try:
        if hasattr(response, 'state_delta') and hasattr(response.state_delta, 'temp'):
            metadata = response.state_delta.temp.get("_adk_grounding_metadata", {})
            grounding_chunks = metadata.get("groundingChunks", [])
            
            if grounding_chunks:
                print(f"[DEBUG] Found {len(grounding_chunks)} grounding chunks")
                urls = []
                for chunk in grounding_chunks:
                    if 'web' in chunk and 'uri' in chunk['web']:
                        url = chunk['web']['uri']
                        urls.append(url)
                        print(f"[DEBUG] Extracted URL: {url}")
                
                if urls:
                    domains = []
                    for url in urls:
                        parsed = urlparse(url)
                        if parsed.netloc:
                            domains.append(parsed.netloc)
                    unique_domains = sorted(list(set(domains)))
                    print(f"[DEBUG] Extracted domains: {unique_domains}")
    except Exception as e:
        print(f"[DEBUG] Error extracting domains from grounding metadata: {e}")
    
    return unique_domains


def inject_process_log_after_search(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any):
    """
    Callback: After a successful search, this injects the process_log into the response.
    
    Note: Grounding metadata (source URLs) is added by ADK framework after this callback,
    so we add a placeholder here. Use extract_domains_from_grounding_metadata() on the 
    agent response to get actual source domains.
    """
    print("[CALLBACK-DEBUG] inject_process_log_after_search called.")
    print(f"[CALLBACK-DEBUG] tool.name: {tool.name}, tool_response type: {type(tool_response)}")
    
    if tool.name == "google_search_agent":
        # Add sourcing log entry
        # The actual domains will be extracted from grounding metadata after agent response
        sourcing_log = "Action: Performed web search to source recent AI news articles."
        
        # Add to process log
        current_log = tool_context.state.get('process_log', [])
        tool_context.state['process_log'] = [sourcing_log] + current_log

        final_log = tool_context.state.get('process_log', [])
        print(f"[CALLBACK-DEBUG] Process log: {final_log}")
        
        # Return response with process log injected
        if isinstance(tool_response, str):
            return {
                "search_results": tool_response,
                "process_log": final_log
            }
        elif isinstance(tool_response, dict):
            tool_response['process_log'] = final_log
            return tool_response
            
    return tool_response


def update_process_log_with_domains(agent_response, tool_context: ToolContext):
    """
    Update the process log with actual source domains from grounding metadata.
    Call this after getting the agent response.
    
    Args:
        agent_response: The response object from agent.send_message()
        tool_context: The tool context to update
        
    Returns:
        List of source domains found
    """
    domains = extract_domains_from_grounding_metadata(agent_response)
    
    if domains:
        # Update the process log with actual domains
        current_log = tool_context.state.get('process_log', [])
        
        # Replace the generic sourcing message with specific domains
        if current_log and "Performed web search" in current_log[0]:
            sourcing_log = f"Action: Sourced news from the following domains: {', '.join(domains)}."
            current_log[0] = sourcing_log
            tool_context.state['process_log'] = current_log
            print(f"[DEBUG] Updated process log with domains: {domains}")
    
    return domains