import logging
from langchain_core.documents import Document
from rag.chunker import chunk_documents

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_chunker_validation():
    print("\n--- Generating Sample Text ---")
    # Create a sample text long enough to force multiple chunks (approx 3800 chars)
    base_paragraph = (
        "This is a sample paragraph designed to test the chunking capabilities of our RAG pipeline. "
        "It contains multiple sentences to allow the recursive splitter to find natural boundary points. "
        "We need to ensure that the chunker respects these boundaries rather than cutting words in half. "
    )
    sample_text = base_paragraph * 15
    
    doc = Document(
        page_content=sample_text,
        metadata={
            "source_type": "generated_test", 
            "source_name": "validation_script"
        }
    )
    
    print(f"Original Document Length: {len(sample_text)} characters")
    
    print("\n--- Executing Chunker ---")
    # Using the default parameters specified in the architecture (1000 size, 200 overlap)
    chunks = chunk_documents([doc], chunk_size=1000, chunk_overlap=200)
    
    print(f"\nSUCCESS: Split 1 document into {len(chunks)} chunks.")
    
    print("\n--- Visual Inspection of Chunks ---")
    for i, chunk in enumerate(chunks):
        content = chunk.page_content
        print(f"\nChunk {i+1}:")
        print(f"Length: {len(content)} characters")
        print(f"Metadata: {chunk.metadata}")
        
        # Print the first and last 80 characters to inspect boundaries and overlap
        if len(content) > 160:
            preview = f"{content[:80]}\n  [...]\n  {content[-80:]}"
        else:
            preview = content
            
        print(f"Content Preview:\n  {preview}")

if __name__ == "__main__":
    run_chunker_validation()
