from core.rag_engine import RAGEngine

rag = RAGEngine()

# First time: embed documents
docs = rag.load_documents("data/documents")
chunks = rag.split_documents(docs)
rag.create_vectorstore(chunks)

# Ask a question
answer = rag.ask("Summarize the document.")
print("[🤖 Answer]:", answer)
