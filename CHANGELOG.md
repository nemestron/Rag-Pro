# Changelog

All notable changes to this project will be documented in this file.

## [v0.6] - Phase 6 Complete: Testing, Optimization & Validation
- Created comprehensive unit test suite using `pytest` (29 total tests).
- Implemented robust `io.BytesIO` mocking for Streamlit `UploadedFile` behavior.
- Mocked LangChain LLM endpoints and network calls to ensure isolated testing.
- Built `benchmark_chunking.py` to evaluate chunking configurations.
- Optimized default parameters to `CHUNK_SIZE=1500` and `CHUNK_OVERLAP=300`.
- Built `validate_grounding.py` achieving 100% hallucination refusal rate on trick questions.
- Verified completely green end-to-end test execution.

## [v0.5] - Phase 5 Complete: Streamlit UI & Application Integration
- Designed and implemented wide-layout Streamlit interface.
- Built dynamic sidebar for multi-format ingestion (URL, PDF, DOCX, TXT, Raw Text).
- Integrated Phase 2, 3, and 4 backend modules into frontend UI.
- Implemented robust `session_state` management for vector store caching.
- Created continuous chat interface preserving conversation history.
- Added UI transparency by displaying retrieved chunks via expander.
- Implemented comprehensive error handling and UX status indicators.

## [v0.4] - Phase 4 Complete: LLM Integration & RAG Chain
- Verified Hugging Face Inference API access.
- Initialized Meta-Llama-3-8B-Instruct wrapped in `ChatHuggingFace`.
- Created strict grounding `ChatPromptTemplate` to prevent hallucinations.
- Assembled the complete RAG pipeline using LangChain Expression Language (LCEL).
- Implemented `ask_question` master query function with retriever validation.
- Successfully passed end-to-end integration and grounding tests.

## [v0.3] - Phase 3 Complete: Text Chunking & Embeddings
- Implemented `RecursiveCharacterTextSplitter`.
- Initialized `sentence-transformers/all-MiniLM-L6-v2` embedding model.
- Built and validated FAISS vector store with local save/load persistence.
- Created `get_retriever` interface.

## [v0.2] - Phase 2 Complete: Document Ingestion
- Implemented `WebBaseLoader` for URLs.
- Implemented `PyPDFLoader` with temporary file handling (updated to `pypdf`).
- Implemented `python-docx` manual text extraction.
- Implemented native TXT and raw text input handlers.
- Created master orchestrator `load_all_sources`.

## [v0.1] - Phase 1 Complete: Project Initialization
- Established VS Code environment, virtual environment, and dependencies.
- Created complete directory structure.
- Initialized Git repository and connected to GitHub.
- Created `.env` and `config/settings.py` architecture.
