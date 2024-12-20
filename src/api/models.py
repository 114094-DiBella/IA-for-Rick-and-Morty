from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime

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



class ConversationManager:
    def __init__(self, file_path='conversations.json'):
        self.file_path = file_path
        self.conversations = self._load_conversations()

    def _load_conversations(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_conversations(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.conversations, f, indent=2)

    def add_message(self, conversation_id, role, content):
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        self._save_conversations()

    def get_conversation(self, conversation_id):
        return self.conversations.get(conversation_id, [])

    def get_all_conversations(self):
        return self.conversations