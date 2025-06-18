# 🤖 JarvisAI-Pro

**JarvisAI-Pro** is a hybrid offline+online personal AI assistant powered by:
- ✨ Voice control (STT + TTS + Wake Word)
- 🧠 Intent classification (ML) + Generative LLMs (LLaMA 3 Q4)
- 🕵️ Agentic AI (LangChain Agents / LangGraph)
- 📄 Local document Q&A, system tasks, web integration
- 🐳 Containerized deployment (Docker-ready)

---

### 🔧 Core Technologies
- Python, Vosk, Porcupine, scikit-learn, LangChain, Ollama (LLaMA 3 Q4)
- ChromaDB, LangGraph, pyttsx3, Streamlit/Tkinter

---

### 🚀 Project Structure
```plaintext
core/       → Wake word, STT, TTS, intent router
skills/     → Modular tasks (weather, time, etc.)
agents/     → LangChain/LangGraph agent + tools
data/       → Documents, embeddings, training data
ui/         → Optional desktop app / tray
main.py     → Entry point
