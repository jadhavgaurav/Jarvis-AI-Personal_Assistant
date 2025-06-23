# main.py

import sys
import signal

# Reconfigure encoding for emoji support (fix Windows logging errors on Windows)
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from core.wake_word import listen_for_wake_word
from core.speech_to_text import transcribe
from core.intent_classifier import IntentClassifier
from core.router import SkillRouter
from core.tts import speak
from core.llm_engine import LLMEngine
from core.logger import setup_logger
from core.global_memory import save_memory, global_memory

logger = setup_logger(__name__)

# Set to False for CLI input instead of wake word + mic
use_microphone = False


def shutdown_handler(sig, frame):
    logger.info("[❌] Jarvis terminated by user.")
    speak("Goodbye!")
    save_memory(global_memory)  # Persist memory before exit
    sys.exit(0)


def main():
    logger.info("\n[🧠 JARVIS AI-PRO OFFLINE MODE]")
    logger.info("[🔄 Ready to activate via wake word or text input...]")

    # Initialize components
    intent_classifier = IntentClassifier()
    skill_router = SkillRouter()
    llm_chain = LLMEngine().llm  # LangChain ConversationChain with memory

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, shutdown_handler)

    while True:
        try:
            if use_microphone:
                listen_for_wake_word()
                logger.info("[🎤] Wake word detected. Listening for your command...")
                query = transcribe()
            else:
                query = input("[🧪] Type your query: ")

            query = query.strip()
            if not query:
                continue

            logger.info(f"[🎧] Query: {query}")

            # Step 1: Intent Classification
            intent = intent_classifier.predict(query)
            logger.info(f"[🔍] Predicted Intent: {intent}")

            # Step 2: Skill Routing
            response = skill_router.route(intent, query)
            logger.info(f"[🤖] Jarvis Response: {response}")

            # Step 3: Fallback to LLM with memory if unknown
            if intent == "unknown" or "don't have a skill" in response.lower():
                logger.warning("[⚠️] No skill matched. Using LLM with global memory...")
                response = llm_chain.run(query)

            # Step 4: Speak
            speak(response)

        except Exception as e:
            logger.exception(f"[🚨] Unhandled exception: {e}")
            speak("Sorry, something went wrong.")

if __name__ == "__main__":
    main()
