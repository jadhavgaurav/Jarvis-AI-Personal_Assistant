# skills/open_app.py

import os
import psutil
from skills.base import BaseSkill

class OpenAppSkill(BaseSkill):
    def __init__(self):
        self.alias_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "edge": "msedge.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "visual studio": "code.exe",
            "vs code": "code.exe",
            "vscode": "code.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "paint": "mspaint.exe"
        }

    def can_handle(self, intent: str) -> bool:
        return intent in ["open_app", "close_app"]

    def handle(self, query: str) -> str:
        query = query.lower()
        if "open" in query:
            return self._open_app(query)
        elif any(cmd in query for cmd in ["close", "kill"]):
            return self._close_app(query)
        else:
            return "Please specify whether to open or close the application."

    def _extract_app_name(self, query: str, action_keywords: list) -> str:
        for keyword in action_keywords:
            if keyword in query:
                return query.split(keyword, 1)[1].strip()
        return ""

    def _resolve_exe_name(self, app_name: str) -> str | None:
        for alias, exe in self.alias_map.items():
            if alias in app_name:
                return exe
        return None

    def _open_app(self, query: str) -> str:
        app_name = self._extract_app_name(query, ["open"])
        if not app_name:
            return "Please mention the app you want to open."

        exe_name = self._resolve_exe_name(app_name)
        if not exe_name:
            return f"Could not find a known app for '{app_name}'."

        try:
            os.startfile(exe_name)
            return f"Opening {app_name}."
        except FileNotFoundError:
            return f"'{exe_name}' not found. Make sure it's installed and in your system PATH."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

    def _close_app(self, query: str) -> str:
        app_name = self._extract_app_name(query, ["close", "exit", "kill"])
        if not app_name:
            return "Please mention the app you want to close."

        exe_name = self._resolve_exe_name(app_name)
        if not exe_name:
            return f"Could not find a known app for '{app_name}'."

        try:
            found = False
            for proc in psutil.process_iter(['name']):
                if exe_name.lower() == proc.info['name'].lower():
                    proc.terminate()
                    found = True
            return f"Closed {app_name}." if found else f"{app_name} is not currently running."
        except Exception as e:
            return f"Failed to close {app_name}: {str(e)}"
