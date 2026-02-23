import time
import logging
import os
import sys

# Ensure project root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ingestion.loaders import load_urls
from rag.chunker import chunk_documents
from rag.embedder import get_embedding_model, build_vector_store, get_retriever

# Suppress debug logs for cleaner output
logging.getLogger("ingestion").setLevel(logging.WARNING)
logging.getLogger("rag").setLevel(logging.WARNING)


def run_benchmark():
    print("\n" + "=" * 60)
    print("--- RAG PRO: CHUNKING OPTIMIZATION BENCHMARK ---")
    print("=" * 60)

    # 1. Fetch Test Data
    print(
        "\n[1/3] Fetching test document (Wikipedia: Retrieval-augmented generation)..."
    )
    url = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    docs = load_urls([url])

    if not docs:
        print("Failed to load URL. Please check your internet connection.")
        return

    print(
        f"Document loaded successfully. Total length: {len(docs[0].page_content)} characters."
    )

    # 2. Load Embedder once
    print("[2/3] Loading embedding model into memory...")
    embedding_model = get_embedding_model()

    # 3. Configurations to test
    configs = [
        {"size": 500, "overlap": 100},
        {"size": 1000, "overlap": 200},
        {"size": 1500, "overlap": 300},
    ]

    test_query = "What are the primary benefits of RAG?"

    print("\n[3/3] Running configurations...")

    for config in configs:
        print("\n" + "-" * 50)
        print(
            f"TESTING CONFIG: Chunk Size = {config['size']}, Overlap = {config['overlap']}"
        )
        print("-" * 50)

        # Measure Chunking
        start_chunk = time.time()
        chunks = chunk_documents(
            docs, chunk_size=config["size"], chunk_overlap=config["overlap"]
        )
        chunk_time = time.time() - start_chunk

        # Measure Embedding
        start_embed = time.time()
        vector_store = build_vector_store(chunks, embedding_model)
        embed_time = time.time() - start_embed

        print(f"Total Chunks Generated: {len(chunks)}")
        print(f"Chunking Time:          {chunk_time:.4f} seconds")
        print(f"FAISS Embedding Time:   {embed_time:.4f} seconds")

        # Test Retrieval
        retriever = get_retriever(vector_store, k=3)
        retrieved_docs = retriever.invoke(test_query)

        print(
            "\nRetrieval Sample (Top Result Length):",
            len(retrieved_docs[0].page_content),
            "characters",
        )
        print("Retrieval Snippet:", repr(retrieved_docs[0].page_content[:100] + "..."))


if __name__ == "__main__":
    run_benchmark()
