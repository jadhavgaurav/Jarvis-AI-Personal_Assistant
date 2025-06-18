import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.rag_engine import RAGEngine


from core.rag_engine import RAGEngine

rag_engine = RAGEngine()

def run_doc_qa(query: str) -> str:
    """Run document-based QA using the RAG engine."""
    try:
        result = rag_engine.query(query)
        return result
    except Exception as e:
        return f"[RAG Error] {str(e)}"


response = run_doc_qa("Summarize my resume")
print(response)