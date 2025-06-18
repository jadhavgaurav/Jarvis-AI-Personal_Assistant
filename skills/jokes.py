# Tells a joke
import random

class TellJokeSkill:
    def handle(self, query: str) -> str:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "What do you call fake spaghetti? An impasta!",
            "Why did the computer go to therapy? It had a hard drive!"
        ]
        return random.choice(jokes)
