# Fetches weather information
# skills/weather_skill.py

from skills.base import BaseSkill
import requests

class WeatherSkill(BaseSkill):
    def can_handle(self, intent: str) -> bool:
        return intent == "get_weather"

    def handle(self, query: str) -> str:
        try:
            # Default location (or you can parse from query)
            location = "Mumbai"
            weather = self.get_weather(location)
            return f"The weather in {location} is {weather['temp']}°C with {weather['condition']}."
        except Exception as e:
            return f"Couldn't fetch weather right now: {str(e)}"

    def get_weather(self, location: str) -> dict:
        # You can replace this with any free weather API
        url = f"https://wttr.in/{location}?format=%t+%C"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise Exception("API error")

        data = response.text.strip().split(" ", 1)
        return {
            "temp": data[0].replace("+", "").replace("°C", ""),
            "condition": data[1] if len(data) > 1 else "clear"
        }
