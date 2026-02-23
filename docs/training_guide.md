# Training & Reproduction Guide

This guide is for developers who wish to reproduce or extend the RAG Pro architecture from scratch.

## Project Philosophy
RAG Pro was built using a **First Principles** engineering approach:
1. **Modularity**: Every component (Ingestion, Chunking, Embedding, Generation) was built in isolation and rigorously unit-tested before UI integration.
2. **Defensive Programming**: The system assumes external APIs might fail and users might upload corrupt files. Error handling is built deeply into `loaders.py` and `chain.py`.
3. **Hallucination Prevention over helpfulness**: The prompt template strictly prohibits the LLM from relying on its parametric memory.

## Development Workflow
If extending the project, follow this validation loop:
1. **Modify Backend**: Make changes to `rag/` or `ingestion/`.
2. **Run Unit Tests**: Execute `pytest tests/ -v`. Do not proceed if tests fail.
3. **Benchmark**: If modifying chunk sizes or embedding models, run `python scripts/benchmark_chunking.py` to mathematically verify the performance impact.
4. **UI Integration**: Only after passing the backend tests, link the new features to `app/main.py`.

## Future Enhancements to Consider
* Implementing a dynamic chunk size slider in the Streamlit sidebar.
* Adding a secondary fallback LLM in `chain.py` if the primary Hugging Face endpoint times out.
* Integrating OCR (e.g., Tesseract) into the PDF loader to support scanned documents.
