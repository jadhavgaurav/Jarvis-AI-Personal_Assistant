# skills/doc_qa_skill.py

from skills.base import BaseSkill
from core.doc_qa_rag import RAGDocumentQA
from core.global_memory import global_memory
from core.logger import setup_logger

logger = setup_logger(__name__)


class DocQASkill(BaseSkill):
    def __init__(self):
        # Initialize the RAGDocumentQA with global memory for long-term retention
        self.rag_qa = RAGDocumentQA(
            doc_path="data/documents/Gaurav_resume demo.pdf",
            memory=global_memory
        )

    def can_handle(self, intent: str) -> bool:
        return intent.lower().strip() == "doc_qa"

    def handle(self, query: str) -> str:
        if not query.strip():
            return "Please ask a specific question about the document."

        try:
            response = self.rag_qa.ask(query)
            if not response or "couldn't retrieve" in response.lower():
                return "I'm unable to answer that from the document right now."
            return response
        except Exception as e:
            logger.error(f"[❌] Document QA failed: {e}", exc_info=True)
            return "Something went wrong while answering your question."
