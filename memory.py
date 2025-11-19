from collections import deque
from typing import Deque, Dict, List

class ConversationMemory:
    def __init__(self, max_messages: int = 12):
        self.memory: Deque[Dict[str, str]] = deque(maxlen=max_messages)
        
    def add_user_message(self, content: str):
        self.memory.append({"role": "user", "parts": content})
        
    def add_model(self, content: str):
        self.memory.append({"role": "model", "parts": content})
        
    def get(self) -> List[Dict[str, str]]:
        return list(self.memory)
    
    def clear(self):
        self.memory.clear()
