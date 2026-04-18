import os
import streamlit as st
import warnings

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", message=".*unauthenticated.*")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(ROOT_DIR, "chroma_db")
DATA_FILE = os.path.join(ROOT_DIR, "data", "retention_knowledge_base.pdf")

_VECTOR_DB = None
_EMBEDDINGS = None

@st.cache_resource
def get_vector_db():
    global _VECTOR_DB, _EMBEDDINGS
    
    if _VECTOR_DB is not None:
        return _VECTOR_DB

    if _EMBEDDINGS is None:
        _EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # If the database already exists, load it
    if os.path.exists(DB_DIR):
        print("Loading existing Chroma database...")
        _VECTOR_DB = Chroma(persist_directory=DB_DIR, embedding_function=_EMBEDDINGS)
        return _VECTOR_DB

    # Otherwise, create it
    print("Creating new Chroma database...")
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Knowledge base file not found at {DATA_FILE}")

    loader = PyPDFLoader(DATA_FILE)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n## ", "\n---", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(documents)

    _VECTOR_DB = Chroma.from_documents(
        documents=docs, 
        embedding=_EMBEDDINGS, 
        persist_directory=DB_DIR
    )
    
    return _VECTOR_DB

def get_relevant_strategies(customer_profile_str, churn_reason=""):
    """
    Retrieves the most relevant strategies from the knowledge base.
    """
    db = get_vector_db()
    
    # Formulate a search query
    query = f"Customer Profile: {customer_profile_str}\n"
    if churn_reason:
         query += f"Potential Churn Reason: {churn_reason}\n"
    query += "Find relevant retention strategies."

    results = db.similarity_search(query, k=2)
    
    context = "\n\n".join([doc.page_content for doc in results])
    return context

if __name__ == "__main__":
    # Test initialization
    print("Initializing Vector DB...")
    db = get_vector_db()
    print("DB Initialized.")
    
    print("\nTesting Retrieval...")
    strategies = get_relevant_strategies(
        "Age 22, student, mobile device user", 
        "Low watch hours and high price sensitivity"
    )
    print("Retrieved Strategies:\n")
    print(strategies)
