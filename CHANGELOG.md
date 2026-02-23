# Changelog

All notable changes to this project will be documented in this file.

## [v0.4] - Phase 4 Complete: LLM Integration & RAG Chain
- Verified Hugging Face Inference API access.
- Initialized Meta-Llama-3-8B-Instruct wrapped in `ChatHuggingFace`.
- Created strict grounding `ChatPromptTemplate` to prevent hallucinations.
- Assembled the complete RAG pipeline using LangChain Expression Language (LCEL).
- Implemented `ask_question` master query function with retriever validation.
- Successfully passed end-to-end integration and grounding tests.

## [v0.3] - Phase 3 Complete: Text Chunking & Embeddings
- Implemented `RecursiveCharacterTextSplitter` (1000 size / 200 overlap).
- Initialized `sentence-transformers/all-MiniLM-L6-v2` embedding model.
- Built and validated FAISS vector store with local save/load persistence.
- Created `get_retriever` interface.

## [v0.2] - Phase 2 Complete: Document Ingestion
- Implemented `WebBaseLoader` for URLs.
- Implemented `PyPDFLoader` with temporary file handling.
- Implemented `python-docx` manual text extraction.
- Implemented native TXT and raw text input handlers.
- Created master orchestrator `load_all_sources`.

## [v0.1] - Phase 1 Complete: Project Initialization
- Established VS Code environment, virtual environment, and dependencies.
- Created complete directory structure.
- Initialized Git repository and connected to GitHub.
- Created `.env` and `config/settings.py` architecture.
