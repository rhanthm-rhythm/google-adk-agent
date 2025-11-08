from typing import Dict, List
import requests
import os

def get_company_info(tickers: List[str]) -> Dict[str, str]:
    """
    Fetches company information including headquarters, CEO, and employee count
    for a list of stock tickers using the Alpha Vantage API.

    Args:
        tickers: A list of stock market tickers (e.g., ["GOOG", "NVDA"]).

    Returns:
        A dictionary mapping each ticker to its formatted company information string.
    """
    company_data: Dict[str, str] = {}
    
    # Get API key from environment variable
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    if not api_key:
        # Return error message for all tickers if no API key
        for ticker_symbol in tickers:
            company_data[ticker_symbol] = "API key not configured. Please set ALPHA_VANTAGE_API_KEY environment variable."
        return company_data
    
    for ticker_symbol in tickers:
        try:
            # Alpha Vantage Company Overview endpoint
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "OVERVIEW",
                "symbol": ticker_symbol,
                "apikey": api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if we got valid data (Alpha Vantage returns error messages in the response)
            if "Error Message" in data or "Note" in data or not data.get("Name"):
                company_data[ticker_symbol] = "Company data not available or invalid ticker."
                continue
            
            # Extract relevant information
            company_name = data.get("Name", "N/A")
            headquarters = data.get("Address", "N/A")
            sector = data.get("Sector", "N/A")
            industry = data.get("Industry", "N/A")
            employees = data.get("FullTimeEmployees", "N/A")
            description = data.get("Description", "")
            
            # Format employee count with commas if it's a number
            if employees != "N/A" and employees.isdigit():
                employees = f"{int(employees):,}"
            
            # Create formatted string with available information
            info_parts = []
            info_parts.append(f"Company: {company_name}")
            
            if headquarters != "N/A":
                info_parts.append(f"HQ: {headquarters}")
            
            if sector != "N/A":
                info_parts.append(f"Sector: {sector}")
                
            if industry != "N/A":
                info_parts.append(f"Industry: {industry}")
            
            if employees != "N/A":
                info_parts.append(f"Employees: {employees}")
            
            # Join all parts with " | " separator
            company_data[ticker_symbol] = " | ".join(info_parts)
            
        except requests.exceptions.Timeout:
            company_data[ticker_symbol] = "Request timeout - please try again."
        except requests.exceptions.RequestException:
            company_data[ticker_symbol] = "Network error - unable to fetch company data."
        except Exception:
            # Handle any other unexpected errors gracefully
            company_data[ticker_symbol] = "Error retrieving company information."
    
    return company_data