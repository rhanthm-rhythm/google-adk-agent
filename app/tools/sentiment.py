from typing import Dict, List

def analyze_news_sentiment(headlines: List[str]) -> Dict[str, str]:
    """
    Analyzes the sentiment of news headlines using FinBERT sentiment analysis.
    
    Args:
        headlines: A list of news headlines to analyze.
    
    Returns:
        A dictionary mapping each headline to its sentiment (positive/negative/neutral).
    """
    sentiment_data: Dict[str, str] = {}
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
        
        model = "ProsusAI/finbert"
        
        # Initialize the sentiment analysis pipeline
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=model,
            device=-1  # Use CPU (-1), change to 0 for GPU
        )
        
    except ImportError:
        # Fallback if transformers is not installed
        for headline in headlines:
            sentiment_data[headline] = "neutral"
        return sentiment_data
    except Exception:
        # Fallback for any other initialization errors
        for headline in headlines:
            sentiment_data[headline] = "neutral"
        return sentiment_data
    
    for headline in headlines:
        try:
            # Analyze sentiment using FinBERT
            result = sentiment_pipeline(headline)
            
            # FinBERT returns labels: 'positive', 'negative', 'neutral'
            label = result[0]['label'].lower()
            confidence = result[0]['score']
            
            # Only assign sentiment if confidence is above threshold
            if confidence > 0.6:
                sentiment = label
            else:
                sentiment = "neutral"
            
            sentiment_data[headline] = sentiment
            
        except Exception:
            # Handle any unexpected errors gracefully
            sentiment_data[headline] = "neutral"
    
    return sentiment_data


def format_headline_with_sentiment(headline: str, sentiment: str) -> str:
    """
    Formats a headline with color coding based on sentiment.
    
    Args:
        headline: The news headline to format.
        sentiment: The sentiment (positive/negative/neutral).
    
    Returns:
        A formatted string with appropriate color coding.
    """
    if sentiment == "positive":
        return f"🟢 {headline}"
    elif sentiment == "negative":
        return f"🔴 {headline}"
    else:  # neutral
        return f"⚪ {headline}"