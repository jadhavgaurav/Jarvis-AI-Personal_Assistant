# core/router.py

import importlib
import os
import traceback
from skills.base import BaseSkill

class SkillRouter:
    def __init__(self, skills_folder='skills'):
        self.skills = self.load_skills(skills_folder)

    def load_skills(self, folder):
        skills = []
        for file in os.listdir(folder):
            if file.endswith('.py') and file not in ('base.py', '__init__.py'):
                module_name = f"{folder}.{file[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, BaseSkill) and attr is not BaseSkill:
                            skill_instance = attr()
                            skills.append(skill_instance)
                            print(f"[🧠] Loaded skill: {attr.__name__}")
                except Exception as e:
                    print(f"[⚠️] Failed to load skill from {module_name}: {e}")
                    traceback.print_exc()
        return skills

    def route(self, intent, query):
        for skill in self.skills:
            if hasattr(skill, "can_handle") and skill.can_handle(intent):
                return skill.handle(query)
        return "Sorry, I don't have a skill for that yet."
