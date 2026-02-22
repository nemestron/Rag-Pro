import os
import time
import logging

from ingestion.loaders import load_raw_text
from rag.chunker import chunk_documents
from rag.embedder import (
    get_embedding_model,
    build_vector_store,
    save_vector_store,
    load_vector_store,
    get_retriever
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def run_end_to_end_test():
    print("\n--- Starting End-to-End Embedding Test ---")
    
    # 1. Create Sample Data
    test_content = (
        "Quantum computing is a rapidly-emerging technology that harnesses the laws of quantum mechanics "
        "to solve problems too complex for classical computers. " * 10 + "\n\n" +
        "The capital of France is Paris. It is known for the Eiffel Tower and the Louvre Museum. " * 5 + "\n\n" +
        "Photosynthesis is a process used by plants and other organisms to convert light energy into "
        "chemical energy that, through cellular respiration, can later be released to fuel the organism's activities." * 10
    )
    
    print("\n[Step 1] Loading Document...")
    t0 = time.time()
    documents = load_raw_text(test_content)
    t1 = time.time()
    print(f"Loaded {len(documents)} document(s) in {t1-t0:.4f} seconds.")
    
    # 2. Chunking
    print("\n[Step 2] Chunking Document...")
    t2 = time.time()
    chunks = chunk_documents(documents, chunk_size=300, chunk_overlap=50)
    t3 = time.time()
    print(f"Generated {len(chunks)} chunks in {t3-t2:.4f} seconds.")
    
    # 3. Initialize Embedding Model
    print("\n[Step 3] Initializing Embedding Model...")
    t4 = time.time()
    model = get_embedding_model()
    t5 = time.time()
    print(f"Model initialized in {t5-t4:.4f} seconds. (Note: First run may take longer due to download).")
    
    # 4. Build Vector Store
    print("\n[Step 4] Building FAISS Vector Store...")
    t6 = time.time()
    vector_store = build_vector_store(chunks, model)
    t7 = time.time()
    print(f"Vector store built in {t7-t6:.4f} seconds.")
    
    # 5. Persist to Disk
    print("\n[Step 5] Saving Vector Store to Disk...")
    save_dir = os.path.join("data", "vector_stores", "test_index")
    t8 = time.time()
    save_vector_store(vector_store, save_dir)
    t9 = time.time()
    print(f"Vector store saved in {t9-t8:.4f} seconds.")
    
    # Check disk size
    size_bytes = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                     for dirpath, _, filenames in os.walk(save_dir) 
                     for filename in filenames)
    print(f"Index size on disk: {size_bytes / 1024:.2f} KB")
    
    # 6. Load from Disk
    print("\n[Step 6] Loading Vector Store from Disk...")
    t10 = time.time()
    loaded_vector_store = load_vector_store(save_dir, model)
    t11 = time.time()
    print(f"Vector store loaded in {t11-t10:.4f} seconds.")
    
    # 7. Semantic Retrieval Test
    print("\n[Step 7] Testing Semantic Retrieval...")
    query = "What city is known for the Louvre?"
    print(f"Query: '{query}'")
    
    retriever = get_retriever(loaded_vector_store, k=2)
    
    t12 = time.time()
    retrieved_docs = retriever.invoke(query)
    t13 = time.time()
    
    print(f"Retrieved {len(retrieved_docs)} chunks in {t13-t12:.4f} seconds.")
    print("\n--- Retrieval Results ---")
    for i, doc in enumerate(retrieved_docs):
        print(f"\nResult {i+1} (Metadata: {doc.metadata}):")
        print(f"Content: {doc.page_content.strip()}")
        
    print("\n--- End-to-End Test Complete ---")

if __name__ == "__main__":
    run_end_to_end_test()
