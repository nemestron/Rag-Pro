# API Reference

This document outlines the core internal APIs of the RAG Pro backend modules.

## Module: `ingestion.loaders`
* `load_urls(urls: List[str]) -> List[Document]`: Scrapes web content using `WebBaseLoader`.
* `load_pdf(uploaded_file) -> List[Document]`: Extracts text from PDF byte streams using `pypdf`.
* `load_docx(uploaded_file) -> List[Document]`: Extracts paragraphs from Word documents using `python-docx`.
* `load_txt(uploaded_file) -> List[Document]`: Decodes raw text files, falling back to Latin-1 if UTF-8 fails.
* `load_all_sources(...) -> List[Document]`: Master orchestrator. Merges all inputs into a single list of `Document` objects.

## Module: `rag.chunker`
* `chunk_documents(documents: List[Document], chunk_size: int = 1500, chunk_overlap: int = 300) -> List[Document]`: Splits normalized documents into overlapping semantic chunks.

## Module: `rag.embedder`
* `build_vector_store(chunks: List[Document], embedding_model) -> FAISS`: Computes vectors and builds the index.
* `save_vector_store(vector_store: FAISS, save_path: str)`: Persists index to disk.
* `get_retriever(vector_store: FAISS, k: int = 4)`: Returns the LangChain retriever interface.

## Module: `rag.chain`
* `ask_question(question: str, retriever) -> str`: Executes the LCEL RAG chain and returns the grounded LLM response.
