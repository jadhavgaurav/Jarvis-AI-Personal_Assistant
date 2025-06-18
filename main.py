from core.wake_word import listen_for_wake_word
from core.speech_to_text import transcribe
from core.intent_classifier import IntentClassifier
from core.router import SkillRouter
from core.tts import speak
from core.llm_engine import LLMEngine
from core.logger import setup_logger

logger = setup_logger(__name__)

def main():
    logger.info("\n[🧠 JARVIS AI-PRO OFFLINE MODE]")
    logger.info("[🔄 Ready to activate via wake word...]")

    # Initialize core components
    intent_classifier = IntentClassifier()
    skill_router = SkillRouter()
    llm = LLMEngine().llm  # ✅ LLM engine (e.g., Ollama, GPT)

    while True:
        try:
            # 🔊 Step 1: Wake word detection (blocking call)
            listen_for_wake_word()
            logger.info("[🎤] Wake word detected. Listening for your command...")

            # 🎙️ Step 2: Speech to Text
            query = transcribe()
            if not query:
                continue
            logger.info(f"[🎧] You said: {query}")

            # 🧠 Step 3: Predict Intent
            intent = intent_classifier.predict(query)
            logger.info(f"[🔍] Predicted Intent: {intent}")

            # 🛠️ Step 4: Route to Skill or fallback
            response = skill_router.route(intent, query)
            logger.info(f"[🤖] Jarvis Response: {response}")

            # 🧠 Step 5: Fallback to LLM if no proper skill handled it
            if intent == "unknown" or "don't have a skill" in response.lower():
                logger.warning("[⚠️] No skill handled the intent. Falling back to LLM...")
                response = llm.invoke(query)

            # 🗣️ Step 6: Speak Response
            speak(response)

        except KeyboardInterrupt:
            logger.info("\n[❌] Terminated by user.")
            speak("Goodbye!")
            break

        except Exception as e:
            logger.exception(f"[⚠️] Unhandled exception occurred: {str(e)}")
            speak("Sorry, something went wrong.")

if __name__ == "__main__":
    main()
