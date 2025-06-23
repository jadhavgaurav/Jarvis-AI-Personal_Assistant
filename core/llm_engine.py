# core/llm_engine.py

from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from core.global_memory import global_memory

class LLMEngine:
    def __init__(
        self,
        model_name: str = "llama3",
        temperature: float = 0.7,
        base_url: str = "http://localhost:11434",
        streaming: bool = True
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.base_url = base_url
        self.streaming = streaming

        self.llm = self._load_llm()

    def _load_llm(self) -> ConversationChain:
        print(f"[🧠] Connecting to Ollama - Model: {self.model_name}")
        base_llm = Ollama(
            model=self.model_name,
            temperature=self.temperature,
            base_url=self.base_url,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]) if self.streaming else None
        )

        return ConversationChain(
            llm=base_llm,
            memory=global_memory,
            verbose=False
        )
