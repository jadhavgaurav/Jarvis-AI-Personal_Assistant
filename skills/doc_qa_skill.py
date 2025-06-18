# skills/doc_qa_skill.py

from skills.base import BaseSkill
from core.doc_qa_rag import RAGDocumentQA

class DocQASkill(BaseSkill):
    def __init__(self):
        self.rag_qa = RAGDocumentQA("data/docs/sample.pdf")  # 🔁 or make dynamic

    def can_handle(self, intent: str) -> bool:
        return intent.lower() in ["doc_qa", "document_qa", "file_question"]

    def handle(self, query: str) -> str:
        return self.rag_qa.ask(query)
