from typing import Dict, List
import yfinance as yf

def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """
    Fetches the current stock price and daily change for a list of stock tickers
    using the yfinance library.

    Args:
        tickers: A list of stock market tickers (e.g., ["GOOG", "NVDA"]).

    Returns:
        A dictionary mapping each ticker to its formatted financial data string.
    """
    financial_data: Dict[str, str] = {}
    for ticker_symbol in tickers:
        try:
            # Create a Ticker object
            stock = yf.Ticker(ticker_symbol)

            # Fetch the info dictionary
            info = stock.info

            # Safely access the required data points
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")

            if price is not None and change_percent is not None:
                # Format the percentage and the final string
                change_str = f"{change_percent:+.2f}%"
                financial_data[ticker_symbol] = f"${price:.2f} ({change_str})"
            else:
                # Handle cases where the ticker is valid but data is missing
                financial_data[ticker_symbol] = "Price data not available."

        except Exception:
            # This handles invalid tickers or other yfinance errors gracefully
            financial_data[ticker_symbol] = "Invalid Ticker or Data Error"

    return financial_data