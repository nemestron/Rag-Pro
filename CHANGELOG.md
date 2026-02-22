# Changelog

## [v0.3-phase3-embeddings]
### Added
- Document chunking implementation using RecursiveCharacterTextSplitter.
- Hugging Face semantic embeddings using sentence-transformers/all-MiniLM-L6-v2.
- FAISS vector store creation, local disk persistence, and retrieval interface.
- End-to-end embedding pipeline validation script.

## [v0.2-phase2-ingestion]
### Added
- Document ingestion system with loaders for URL, PDF, DOCX, TXT, and raw text.
- Master orchestrator function `load_all_sources` with temporary file handling for Streamlit compatibility.
- Sample documents and validation script for testing and reproducibility.

## [v0.1-phase1-setup]
### Added
- Project initialization, environment setup, folder structure, configurations, and initial documentation.
