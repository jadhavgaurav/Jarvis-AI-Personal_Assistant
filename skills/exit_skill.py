import sys

from skills.base import BaseSkill

class ExitSkill(BaseSkill):

    def can_handle(self, intent):
        return intent == "exit" or intent == "shutdown"

    def handle(self, query: str) -> str:
        print("[🛑] Assistant shutting down...")
        sys.exit(0)
