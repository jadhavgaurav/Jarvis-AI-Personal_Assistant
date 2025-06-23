# core/doc_qa_rag.py

import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory

from core.logger import setup_logger
logger = setup_logger(__name__)


class RAGDocumentQA:
    def __init__(self, doc_path: str = "data/documents/Gaurav_resume demo.pdf"):
        self.doc_path = doc_path
        self.persist_dir = "data/chroma_db"
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.retriever = self._prepare_retriever()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.qa_chain = self._build_qa_chain()

    def _load_and_split_docs(self):
        ext = os.path.splitext(self.doc_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(self.doc_path)
        elif ext in [".txt", ".md"]:
            loader = TextLoader(self.doc_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        logger.info(f"📄 Loaded and split {len(chunks)} chunks from {self.doc_path}")
        return chunks

    def _prepare_retriever(self):
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)

        if not os.path.exists(self.persist_dir) or not os.listdir(self.persist_dir):
            os.makedirs(self.persist_dir, exist_ok=True)
            chunks = self._load_and_split_docs()
            vectordb = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=self.persist_dir
            )
            vectordb.persist()
            logger.info("✅ ChromaDB index created and persisted.")
        else:
            vectordb = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=embeddings
            )
            logger.info("🔄 Loaded existing ChromaDB index.")

        return vectordb.as_retriever()

    def _build_qa_chain(self):
        try:
            logger.info("[🧠] Using Ollama with LLaMA3 for RAG + Memory")
            llm = OllamaLLM(model="llama3")
            return ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.retriever,
                memory=self.memory,
                verbose=False
            )
        except Exception as e:
            logger.error(f"❌ Failed to initialize Ollama LLM: {e}")
            raise

    def ask(self, query: str) -> str:
        try:
            result = self.qa_chain.run({"question": query})
            logger.info(f"✅ Answered query: {query}")
            return result
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            return "Sorry, I couldn't retrieve an answer from the document."


if __name__ == "__main__":
    rag = RAGDocumentQA()
    while True:
        q = input("Ask something about your document: ")
        if q.lower() in ("exit", "quit"):
            break
        print("Answer:", rag.ask(q))
