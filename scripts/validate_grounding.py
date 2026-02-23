import os
import sys
import logging
from dotenv import load_dotenv

# --- AUTHENTICATION FIX ---
# Load environment variables so the Hugging Face API token is available
load_dotenv()
# ------------------------

# Ensure project root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ingestion.loaders import load_urls
from rag.chunker import chunk_documents
from rag.embedder import get_embedding_model, build_vector_store, get_retriever
from rag.chain import ask_question

# Suppress debug logs
logging.getLogger("ingestion").setLevel(logging.ERROR)
logging.getLogger("rag").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

def validate_grounding():
    print("\n" + "="*60)
    print("--- RAG PRO: GROUNDING VALIDATION SUITE ---")
    print("="*60)
    
    print("\n[1/3] Preparing Test Environment (Wikipedia: RAG)...")
    url = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    docs = load_urls([url])
    
    if not docs:
        print("Failed to load URL. Check your internet connection.")
        return
        
    chunks = chunk_documents(docs, chunk_size=1500, chunk_overlap=300)
    embedding_model = get_embedding_model()
    vector_store = build_vector_store(chunks, embedding_model)
    retriever = get_retriever(vector_store, k=4)
    
    in_context_qs = [
        "What does RAG stand for?",
        "What are the benefits of using RAG?",
        "Does RAG reduce the need to retrain LLMs?"
    ]
    
    out_of_context_qs = [
        "What is the capital of France?",
        "Who won the World Series in 2005?",
        "How do you bake a chocolate cake?",
        "What is the current stock price of Apple?",
        "What are the symptoms of the flu?"
    ]
    
    print("\n[2/3] Testing In-Context Questions (Should provide factual answers)...")
    for q in in_context_qs:
        ans = ask_question(q, retriever)
        print(f"Q: {q}")
        print(f"A: {ans[:120]}...\n")
        
    print("\n[3/3] Testing Out-Of-Context Questions (Should strictly refuse)...")
    passed_refusals = 0
    
    for q in out_of_context_qs:
        ans = ask_question(q, retriever)
        print(f"Q: {q}")
        # Check if our strict grounding phrase is triggered
        if "I don't have enough information" in ans or "I do not have enough information" in ans:
            print("A: [SUCCESSFUL REFUSAL]")
            passed_refusals += 1
        else:
            print(f"A: [FAILED - HALLUCINATION DETECTED] {ans}")
            
    accuracy = (passed_refusals / len(out_of_context_qs)) * 100
    
    print("\n" + "="*60)
    print(f"GROUNDING ACCURACY: {accuracy}% ({passed_refusals}/{len(out_of_context_qs)} refused correctly)")
    if accuracy >= 90:
        print("STATUS: PASSED (Production Ready)")
    else:
        print("STATUS: FAILED (Prompt requires strengthening)")
    print("="*60 + "\n")

if __name__ == "__main__":
    validate_grounding()
