from typing import Dict, List, Tuple
import re
from collections import Counter

def track_ai_trends(headlines: List[str]) -> Dict[str, int]:
    """
    Tracks mentions of specific AI technologies in news headlines.
    
    Args:
        headlines: A list of news headlines to analyze.
    
    Returns:
        A dictionary mapping AI technology categories to their mention counts.
    """
    trend_data: Dict[str, int] = {}
    
    # Define AI technology keywords and categories
    ai_categories = {
        "Large Language Models": [
            "llm", "large language model", "language model", "gpt", "claude", "gemini", 
            "chatgpt", "chat-gpt", "transformer", "bert", "generative ai", "gen ai",
            "conversational ai", "natural language processing", "nlp"
        ],
        "Computer Vision": [
            "computer vision", "cv", "image recognition", "facial recognition", 
            "object detection", "image processing", "visual ai", "opencv", 
            "image classification", "pattern recognition", "visual recognition"
        ],
        "Robotics": [
            "robot", "robotics", "autonomous", "drone", "automation", "robotic", 
            "humanoid", "industrial robot", "service robot", "robotic process automation",
            "rpa", "automated", "self-driving", "autonomous vehicle"
        ],
        "Machine Learning": [
            "machine learning", "ml", "deep learning", "neural network", "ai model",
            "artificial intelligence", "predictive analytics", "data science",
            "algorithm", "training data", "model training"
        ],
        "AI Hardware": [
            "gpu", "tpu", "ai chip", "neural processing unit", "npu", "ai accelerator",
            "nvidia", "tensor", "cuda", "ai infrastructure", "computing power"
        ],
        "AI Applications": [
            "ai assistant", "virtual assistant", "recommendation system", "fraud detection",
            "sentiment analysis", "speech recognition", "voice ai", "ai analytics",
            "predictive maintenance", "ai-powered", "ai-driven"
        ]
    }
    
    # Initialize counters for each category
    for category in ai_categories.keys():
        trend_data[category] = 0
    
    for headline in headlines:
        try:
            # Convert to lowercase for analysis
            headline_lower = headline.lower()
            
            # Count mentions for each AI category
            for category, keywords in ai_categories.items():
                for keyword in keywords:
                    # Use word boundaries to avoid partial matches
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    matches = len(re.findall(pattern, headline_lower))
                    trend_data[category] += matches
                    
        except Exception:
            # Handle any unexpected errors gracefully
            continue
    
    return trend_data


def format_ai_trends_summary(trend_data: Dict[str, int]) -> str:
    """
    Formats the AI trends data into a readable summary string.
    
    Args:
        trend_data: Dictionary mapping AI categories to mention counts.
    
    Returns:
        A formatted string summarizing the AI trends.
    """
    try:
        # Filter out categories with zero mentions
        active_trends = {k: v for k, v in trend_data.items() if v > 0}
        
        if not active_trends:
            return "📊 **AI Trends Analysis**: No specific AI technology mentions detected in current headlines."
        
        # Sort by mention count (descending)
        sorted_trends = sorted(active_trends.items(), key=lambda x: x[1], reverse=True)
        
        summary_parts = ["📊 **AI Trends Analysis**:"]
        
        for category, count in sorted_trends:
            # Add emoji indicators based on category
            emoji = {
                "Large Language Models": "🤖",
                "Computer Vision": "👁️",
                "Robotics": "🦾",
                "Machine Learning": "🧠",
                "AI Hardware": "💻",
                "AI Applications": "⚡"
            }.get(category, "🔹")
            
            mention_text = "mention" if count == 1 else "mentions"
            summary_parts.append(f"  {emoji} **{category}**: {count} {mention_text}")
        
        return "\n".join(summary_parts)
        
    except Exception:
        return "📊 **AI Trends Analysis**: Error analyzing trends."