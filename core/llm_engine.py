# core/llm_engine.py

from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class LLMEngine:
    def __init__(self, model_name: str = "llama3"):
        try:
            self.llm = Ollama(model=model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load LLaMA model via Ollama: {e}")

        self.default_prompt = PromptTemplate(
            input_variables=["query"],
            template="You are a helpful assistant. Answer the following:\n\n{query}"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.default_prompt)

    def ask(self, query: str) -> str:
        try:
            response = self.chain.run(query)
            return response.strip()
        except Exception as e:
            return f"Error in LLM response: {str(e)}"
