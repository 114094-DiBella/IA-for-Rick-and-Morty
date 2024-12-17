from pydantic import BaseModel
from typing import List, Optional

class Query(BaseModel):
    """
    Data model for incoming questions.
    
    @param question: The question text
    @type question: str
    """
    question: str

class Source(BaseModel):
    """
    Data model for information sources.
    
    @param type: Type of source ("episode" or "character")
    @param id: Unique identifier of the source
    @param title: Title or name of the source
    """
    type: str  # "episode" o "character"
    id: str
    title: str


class Response(BaseModel):
    """
    Data model for API responses.
    
    @param answer: Generated answer text
    @param confidence: Confidence score of the answer
    @param sources: List of sources used to generate the answer
    @param context_used: Optional context information used for generation
    """
    answer: str
    confidence: float
    sources: List[Source]
    context_used: Optional[str] = None