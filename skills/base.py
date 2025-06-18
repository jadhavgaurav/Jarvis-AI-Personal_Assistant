# Abstract base class for all skill modules

class BaseSkill:
    def __init__(self):
        self.name = self.__class__.__name__

    def can_handle(self, intent: str) -> bool:
        raise NotImplementedError

    def handle(self, query: str) -> str:
        raise NotImplementedError
