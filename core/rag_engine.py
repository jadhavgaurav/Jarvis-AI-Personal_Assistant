
import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from core.llm_engine import LLMEngine

class RAGEngine:
    def __init__(self, persist_dir="data/chroma_db", model_name="all-MiniLM-L6-v2"):
        self.persist_dir = persist_dir
        self.embedding_model = SentenceTransformerEmbeddings(model_name=model_name)
        self.vectorstore = None
        self.retriever = None
        self.llm = LLMEngine().llm

    def load_documents(self, folder_path: str):
        print("[📄] Loading documents...")
        documents = []
        for filename in os.listdir(folder_path):
            path = os.path.join(folder_path, filename)
            if filename.endswith(".txt"):
                documents.extend(TextLoader(path).load())
            elif filename.endswith(".pdf"):
                documents.extend(PyPDFLoader(path).load())
        return documents

    def split_documents(self, documents, chunk_size=500, chunk_overlap=50):
        print("[✂️] Splitting documents...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_documents(documents)

    def create_vectorstore(self, docs):
        print("[📦] Creating vectorstore...")
        self.vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding_model,
            persist_directory=self.persist_dir
        )
        self.vectorstore.persist()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    def load_vectorstore(self):
        print("[📥] Loading existing vectorstore...")
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embedding_model
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    def ask(self, query: str) -> str:
        if not self.retriever:
            self.load_vectorstore()
        print("[🧠] Running RAG QA Chain...")
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True
        )
        result = qa_chain.invoke({"query": query})
        return result["result"]
