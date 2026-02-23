import os
import logging
from dotenv import load_dotenv

# Import custom modules
from ingestion.loaders import load_all_sources
from rag.chunker import chunk_documents
from rag.embedder import get_embedding_model, build_vector_store, get_retriever
from rag.chain import ask_question

# Configure logging for the test script
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

def run_end_to_end_test():
    load_dotenv()
    
    print("\n" + "="*60)
    print("--- STARTING END-TO-END RAG PIPELINE TEST ---")
    print("="*60 + "\n")
    
    # 1. Simulate Document Ingestion
    test_text = (
        "EquipMe is a next-generation Generative AI product designed to create "
        "highly optimized product bundles based on specific user goals. "
        "Conceptualized in early 2026, it utilizes dynamic matching algorithms "
        "to suggest equipment loadouts rather than individual, disconnected items. "
        "The architecture relies heavily on AI agents to evaluate cross-product compatibility."
    )
    print("[Phase 2 Component] Loading document...")
    documents = load_all_sources(raw_text=test_text)
    
    # 2. Chunking
    print("\n[Phase 3 Component] Chunking document...")
    # Using small chunk sizes for this short test text to ensure it splits
    chunks = chunk_documents(documents, chunk_size=150, chunk_overlap=20)
    
    # 3. Embedding & Vector Store
    print("\n[Phase 3 Component] Initializing embedder and building vector store...")
    embedding_model = get_embedding_model()
    vector_store = build_vector_store(chunks, embedding_model)
    
    # 4. Retrieval Interface
    print("\n[Phase 3 Component] Creating retriever...")
    retriever = get_retriever(vector_store, k=2)
    
    # 5. Question Answering (LLM Chain)
    print("\n[Phase 4 Component] Testing LLM Generation...")
    
    print("\n--- Test A: In-Context Question ---")
    q1 = "What is the core purpose of EquipMe and when was it conceptualized?"
    print(f"Question: {q1}")
    ans1 = ask_question(q1, retriever)
    print(f"Answer: {ans1}")
    
    print("\n--- Test B: Out-of-Context Question (Grounding Test) ---")
    q2 = "Who is the CEO of OpenAI?"
    print(f"Question: {q2}")
    ans2 = ask_question(q2, retriever)
    print(f"Answer: {ans2}")
    
    print("\n" + "="*60)
    print("--- END-TO-END TEST COMPLETE ---")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_end_to_end_test()
