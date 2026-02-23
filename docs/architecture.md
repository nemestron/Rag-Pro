# System Architecture

## Overview
RAG Pro utilizes a modular Retrieval-Augmented Generation pipeline designed for high accuracy and zero hallucination. The architecture strictly separates the data ingestion plane from the inference plane.

## Data Ingestion Plane (Phases 2 & 3)
1. **Loaders (`ingestion/loaders.py`)**: Normalizes URLs, PDFs, DOCX, TXT, and Raw Text into LangChain `Document` objects containing `page_content` and `metadata`.
2. **Chunker (`rag/chunker.py`)**: Implements `RecursiveCharacterTextSplitter`. Optimized to 1500 character chunks with 300 character overlaps to preserve semantic context across paragraph boundaries.
3. **Embedder (`rag/embedder.py`)**: Utilizes local `sentence-transformers/all-MiniLM-L6-v2`. By running embeddings locally on the CPU, we eliminate API latency and costs during the indexing phase.
4. **Vector Store**: FAISS (Facebook AI Similarity Search) is used for in-memory, highly efficient L2 distance nearest-neighbor retrieval. Indexes are persisted to disk to avoid redundant embedding costs.

## Inference Plane (Phase 4)
1. **Retriever**: Exposed via FAISS, configured to fetch the top `k=4` most semantically relevant chunks.
2. **LLM (`rag/chain.py`)**: Connects to `Meta-Llama-3-8B-Instruct` via the Hugging Face Inference API. Temperature is locked at 0.3 for deterministic, factual outputs.
3. **LCEL Chain**: Uses LangChain Expression Language to pipe the user query to the retriever, format the returned documents into the context variable, and execute the strict grounding prompt.

## State Management (Phase 5)
The Streamlit frontend utilizes `st.session_state` to cache the FAISS vector store in memory across user interactions, preventing the application from reprocessing documents on every chat rerun.
