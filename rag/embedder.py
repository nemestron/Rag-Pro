import os
import logging
from typing import List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)

def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    """
    Initializes and returns the Hugging Face embedding model.
    Downloads the model weights on the first run.
    """
    try:
        logger.info(f"Initializing embedding model: {model_name}")
        # Using CPU by default; HuggingFaceEmbeddings handles device placement automatically
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {str(e)}")
        raise

def build_vector_store(chunks: List[Document], embedding_model: HuggingFaceEmbeddings) -> FAISS:
    """
    Builds a FAISS vector store from a list of Document chunks.
    """
    if not chunks:
        raise ValueError("Cannot build vector store: No document chunks provided.")
        
    try:
        logger.info(f"Building FAISS vector store for {len(chunks)} chunks...")
        vector_store = FAISS.from_documents(chunks, embedding_model)
        logger.info("Successfully built FAISS vector store.")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to build vector store: {str(e)}")
        raise

def save_vector_store(vector_store: FAISS, save_path: str) -> None:
    """
    Saves the FAISS vector store to disk for persistence.
    """
    try:
        # Ensure the directory exists
        os.makedirs(save_path, exist_ok=True)
        logger.info(f"Saving vector store to {save_path}...")
        vector_store.save_local(save_path)
        logger.info("Vector store successfully saved to disk.")
    except Exception as e:
        logger.error(f"Failed to save vector store: {str(e)}")
        raise

def load_vector_store(load_path: str, embedding_model: HuggingFaceEmbeddings) -> FAISS:
    """
    Loads a FAISS vector store from disk.
    Requires allow_dangerous_deserialization=True as we trust our own local files.
    """
    if not os.path.exists(load_path):
        raise FileNotFoundError(f"Vector store path does not exist: {load_path}")
        
    try:
        logger.info(f"Loading vector store from {load_path}...")
        vector_store = FAISS.load_local(
            folder_path=load_path, 
            embeddings=embedding_model, 
            allow_dangerous_deserialization=True
        )
        logger.info("Vector store successfully loaded from disk.")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to load vector store from {load_path}: {str(e)}")
        raise

def get_retriever(vector_store: FAISS, k: int = 4):
    """
    Exposes the vector store as a LangChain retriever interface.
    
    Args:
        vector_store: The instantiated FAISS vector store.
        k: The number of top chunks to retrieve.
    """
    try:
        logger.info(f"Creating retriever with top_k={k}")
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        return retriever
    except Exception as e:
        logger.error(f"Failed to create retriever: {str(e)}")
        raise
