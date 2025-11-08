
from pydantic import BaseModel, Field
from typing import List
from app06.types.NewsStory import NewsStory

class AINewsReport(BaseModel):
    """A structured report of the latest AI news."""
    title: str = Field(default="AI Research Report", description="The main title of the report.")
    report_summary: str = Field(description="A brief, high-level summary of the key findings in the report.")
    stories: List[NewsStory] = Field(description="A list of the individual news stories found.")
