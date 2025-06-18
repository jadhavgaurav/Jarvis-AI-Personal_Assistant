from skills.base import BaseSkill

class GreetSkill(BaseSkill):

    def can_handle(self, intent: str) -> bool:
        return intent == "greet"
    
    def handle(self, query: str) -> str:
        return "Hello! How can I assist you today?"
