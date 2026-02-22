# RAG Pro

**Production-Grade Retrieval-Augmented Generation Q&A System**

A Retrieval-Augmented Generation (RAG) Q&A web application that enables users to upload documents (URLs, PDFs, DOCX, TXT, or raw text), ask questions, and receive accurate answers grounded strictly in those documents using vector similarity search and large language models.

**Repository:** [https://github.com/nemestron/Rag-Pro](https://github.com/nemestron/Rag-Pro)

## Key Features
* **Multi-Format Ingestion:** Seamlessly process URLs, PDFs, Word Documents (DOCX), plain text (TXT), and raw text input.
* **Strict Grounding:** Explicitly handles out-of-context questions by refusing to hallucinate answers, ensuring high reliability.
* **Local Vector Search:** Utilizes FAISS and local Sentence-Transformer embeddings for secure, low-latency semantic retrieval.
* **Production Architecture:** Features persistent session state management, comprehensive error handling, and a modular design.

## Technology Stack
* **UI Framework:** Streamlit
* **Orchestration:** LangChain
* **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
* **Vector Store:** FAISS (faiss-cpu)
* **LLM:** Meta-Llama-3-8B-Instruct (via Hugging Face Inference API)

## Installation & Setup
*(Detailed instructions will be provided in Phase 7)*

## Usage
*(Usage guidelines and demo links will be provided in Phase 7)*

## Project Structure
The repository follows a modular, production-ready structure separating ingestion, chunking, retrieval, and application logic. Refer to the `docs/` folder for deeper architectural guidelines.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
