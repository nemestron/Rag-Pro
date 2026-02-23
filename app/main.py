import streamlit as st
import logging
import os
import sys
from dotenv import load_dotenv

# --- PATH RESOLUTION BLOCK ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -----------------------------

try:
    from ingestion.loaders import load_all_sources
    from rag.chunker import chunk_documents
    from rag.embedder import get_embedding_model, build_vector_store, get_retriever
    from rag.chain import ask_question
except ModuleNotFoundError as e:
    st.error(f"Critical Error: Backend modules not found. {str(e)}")
    st.stop()

# Configure module-level logger
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

def initialize_session_state():
    """Initializes persistent variables across Streamlit reruns."""
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "is_processed" not in st.session_state:
        st.session_state.is_processed = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    load_dotenv()
    initialize_session_state()

    # 1. Page Configuration
    st.set_page_config(
        page_title="RAG Pro",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Variables to hold user inputs
    source_type = None
    urls = []
    uploaded_files = None
    raw_text = ""

    # 2. Sidebar Layout (Configuration & Ingestion)
    with st.sidebar:
        st.header("Document Ingestion")
        st.markdown("Configure your data sources below.")
        
        source_type = st.radio(
            "Select Data Source",
            ["URL", "PDF", "DOCX", "TXT", "Raw Text"],
            help="Choose the format of the document you want to ingest."
        )
        
        st.markdown("---")
        
        # Dynamic Input Rendering
        if source_type == "URL":
            url_count = st.number_input("Number of URLs to process", min_value=1, max_value=10, value=1)
            for i in range(url_count):
                url_input = st.text_input(f"URL {i+1}", key=f"url_input_{i}")
                if url_input.strip():
                    urls.append(url_input.strip())
                    
        elif source_type == "PDF":
            uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
            
        elif source_type == "DOCX":
            uploaded_files = st.file_uploader("Upload Word documents", type=["docx"], accept_multiple_files=True)
            
        elif source_type == "TXT":
            uploaded_files = st.file_uploader("Upload Text files", type=["txt"], accept_multiple_files=True)
            
        elif source_type == "Raw Text":
            raw_text = st.text_area("Paste raw text here", height=250, placeholder="Enter text content...")
        
        st.divider()
        
        # Document Processing Logic
        if st.button("Process Documents", type="primary", use_container_width=True):
            if source_type == "URL" and not urls:
                st.error("Please enter at least one valid URL.")
            elif source_type in ["PDF", "DOCX", "TXT"] and not uploaded_files:
                st.error(f"Please upload at least one {source_type} file.")
            elif source_type == "Raw Text" and not raw_text.strip():
                st.error("Please enter some text to process.")
            else:
                with st.spinner("Processing documents..."):
                    try:
                        docs = []
                        if source_type == "URL":
                            docs = load_all_sources(urls=urls)
                        elif source_type == "PDF":
                            docs = load_all_sources(pdf_files=uploaded_files)
                        elif source_type == "DOCX":
                            docs = load_all_sources(docx_files=uploaded_files)
                        elif source_type == "TXT":
                            docs = load_all_sources(txt_files=uploaded_files)
                        elif source_type == "Raw Text":
                            docs = load_all_sources(raw_text=raw_text)

                        chunks = chunk_documents(docs)
                        embedding_model = get_embedding_model()
                        vector_store = build_vector_store(chunks, embedding_model)

                        # Persist state and clear previous chat history for new documents
                        st.session_state.vector_store = vector_store
                        st.session_state.is_processed = True
                        st.session_state.messages = []

                        st.success(f"Successfully processed {len(docs)} documents into {len(chunks)} searchable chunks!")
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

    # 3. Main Area Layout (Interaction & Output)
    st.title("RAG Pro: Intelligence Platform")
    st.markdown("Upload documents in the sidebar and ask questions below.")
    st.divider()
    
    # Interaction zone behavior depends on processing state
    if not st.session_state.is_processed:
        st.info("Please select a data source and click 'Process Documents' in the sidebar to begin.")
        st.chat_input("Ask a question about your documents...", disabled=True)
    else:
        # Render existing chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # If the message is from the assistant and has context, render the expander
                if message["role"] == "assistant" and "context" in message:
                    with st.expander("View Retrieved Context"):
                        for i, chunk in enumerate(message["context"]):
                            st.markdown(f"**Chunk {i+1} (Source: {chunk.metadata.get('source_name', 'Unknown')})**")
                            st.text(chunk.page_content)
                            st.markdown("---")

        # Accept new user input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Display user message immediately
            with st.chat_message("user"):
                st.markdown(prompt)
            # Add user message to state
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing documents and generating answer..."):
                    try:
                        retriever = get_retriever(st.session_state.vector_store)
                        
                        # Fetch answer and context
                        answer = ask_question(prompt, retriever)
                        retrieved_docs = retriever.invoke(prompt)
                        
                        st.markdown(answer)
                        
                        with st.expander("View Retrieved Context"):
                            for i, doc in enumerate(retrieved_docs):
                                st.markdown(f"**Chunk {i+1} (Source: {doc.metadata.get('source_name', 'Unknown')})**")
                                st.text(doc.page_content)
                                st.markdown("---")
                                
                        # Add assistant response and context to state
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer,
                            "context": retrieved_docs
                        })
                        
                    except Exception as e:
                        st.error(f"An error occurred while generating the answer: {str(e)}")

if __name__ == "__main__":
    main()
