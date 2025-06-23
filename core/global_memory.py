import pickle
import os
from langchain.memory import ConversationBufferMemory

MEMORY_PATH = "data/global_memory.pkl"

def load_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "rb") as f:
            return pickle.load(f)
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def save_memory(memory):
    with open(MEMORY_PATH, "wb") as f:
        pickle.dump(memory, f)

global_memory = load_memory()
