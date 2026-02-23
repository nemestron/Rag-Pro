import logging
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def chunk_documents(
    documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[Document]:
    """
    Splits a list of LangChain Document objects into smaller semantic chunks.

    Args:
        documents: A list of Document objects to be chunked.
        chunk_size: The maximum number of characters per chunk.
        chunk_overlap: The number of overlapping characters between consecutive chunks.

    Returns:
        A new list of Document objects representing the chunks. Metadata is preserved.
    """
    if not documents:
        logger.warning("No documents provided for chunking. Returning empty list.")
        return []

    try:
        logger.info(
            f"Initializing RecursiveCharacterTextSplitter (size={chunk_size}, overlap={chunk_overlap})."
        )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )

        chunks = splitter.split_documents(documents)

        if not chunks:
            logger.warning(
                "Chunking completed but returned no chunks. Check input document content."
            )
            return []

        logger.info(
            f"Successfully split {len(documents)} source documents into {len(chunks)} chunks."
        )
        return chunks

    except Exception as e:
        logger.error(f"A critical error occurred during document chunking: {str(e)}")
        raise
