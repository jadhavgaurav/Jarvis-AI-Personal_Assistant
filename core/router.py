import importlib
import os
import traceback
from skills.base import BaseSkill
from core.llm_engine import LLMEngine  # LLM fallback engine
from core.logger import setup_logger

logger = setup_logger(__name__)

class SkillRouter:
    def __init__(self, skills_folder='skills'):
        self.skills = self.load_skills(skills_folder)
        self.llm = LLMEngine().llm  # Initialize LLM fallback
        logger.info("✅ SkillRouter initialized with LLM fallback support.")

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
                            logger.info(f"[🧠] Loaded skill: {attr.__name__}")
                except Exception as e:
                    logger.error(f"[⚠️] Failed to load skill from {module_name}: {e}", exc_info=True)
        return skills

    def route(self, intent, query):
        logger.info(f"[📍] Routing intent: {intent}")

        # 1. Try handling the intent via skill
        for skill in self.skills:
            if hasattr(skill, "can_handle") and skill.can_handle(intent):
                try:
                    logger.info(f"[✅] Routed to skill: {skill.__class__.__name__}")
                    return skill.handle(query)
                except Exception as e:
                    logger.error(f"[❌] Error in skill {skill.__class__.__name__}: {e}", exc_info=True)
                    return "Something went wrong while handling your request."

        # 2. Fallback to LLM for unmatched intents
        logger.warning("[⚠️] No skill matched. Using LLM fallback...")
        try:
            response = self.llm.invoke(query)
            return response
        except Exception as e:
            logger.critical(f"[❌] LLM fallback failed: {e}", exc_info=True)
            return "Sorry, I couldn't understand your request and no skill is available."
