# core/doc_qa_rag.py

import os
import faiss
import pickle
import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub

from core.logger import setup_logger
logger = setup_logger(__name__)

class RAGDocumentQA:
    def __init__(self, doc_path: str = "data/docs/sample.pdf"):
        self.doc_path = doc_path
        self.db_path = "data/vectorstore/faiss_index"
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.retriever = self._prepare_retriever()
        self.qa_chain = self._build_qa_chain()

    def _load_and_split_docs(self):
        ext = os.path.splitext(self.doc_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(self.doc_path)
        elif ext in [".txt", ".md"]:
            loader = TextLoader(self.doc_path)
        else:
            raise ValueError("Unsupported document format.")

        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        logger.info(f"📄 Loaded {len(chunks)} document chunks from {self.doc_path}")
        return chunks

    def _prepare_retriever(self):
        if not os.path.exists(self.db_path):
            os.makedirs("data/vectorstore", exist_ok=True)
            chunks = self._load_and_split_docs()
            embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
            db = FAISS.from_documents(chunks, embeddings)
            db.save_local(self.db_path)
            logger.info("✅ FAISS index created and saved.")
        else:
            db = FAISS.load_local(self.db_path, HuggingFaceEmbeddings(model_name=self.embedding_model))
            logger.info("🔄 Loaded existing FAISS index.")

        return db.as_retriever()

    def _build_qa_chain(self):
        llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.2, "max_length": 512})
        return RetrievalQA.from_chain_type(llm=llm, retriever=self.retriever)

    def ask(self, query: str) -> str:
        try:
            result = self.qa_chain.run(query)
            logger.info(f"✅ Answered query: {query}")
            return result
        except Exception as e:
            logger.error(f"❌ Failed to answer query: {e}")
            return "Sorry, I couldn't retrieve an answer from the document."


if __name__ == "__main__":
    rag = RAGDocumentQA("data/docs/sample.pdf")
    while True:
        q = input("Ask a document question: ")
        if q.lower() in ("exit", "quit"): break
        print("Answer:", rag.ask(q))
