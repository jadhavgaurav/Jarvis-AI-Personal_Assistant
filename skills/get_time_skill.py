from datetime import datetime
from skills.base import BaseSkill

class GetTimeSkill(BaseSkill):

    def can_handle(self, intent: str) -> bool:
        return intent == "get_time"

    def handle(self, query: str) -> str:
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."
