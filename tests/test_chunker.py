import pytest
from langchain_core.documents import Document
from rag.chunker import chunk_documents


# --- Fixtures for Deterministic Testing ---
@pytest.fixture
def empty_document():
    return [Document(page_content="", metadata={"source": "empty.txt"})]


@pytest.fixture
def short_document():
    # 45 characters long
    return [
        Document(
            page_content="This is a short document that fits in a chunk.",
            metadata={"source": "short.txt"},
        )
    ]


@pytest.fixture
def long_document():
    # 300 characters long, designed to force multiple splits
    text = (
        "Retrieval-Augmented Generation (RAG) is a technique that bridges the gap "
        "between static large language models and dynamic, external knowledge bases. "
        "By chunking text and storing it in a vector database, systems can retrieve "
        "only the most relevant semantic context to ground the final generation."
    )
    return [
        Document(
            page_content=text, metadata={"source": "long.txt", "author": "Engineer"}
        )
    ]


# --- Test Cases ---


def test_chunk_empty_document(empty_document):
    """Verify empty document returns an empty list without crashing."""
    chunks = chunk_documents(empty_document, chunk_size=100, chunk_overlap=20)
    assert len(chunks) == 0


def test_chunk_short_document(short_document):
    """Verify a document shorter than chunk_size returns exactly one chunk."""
    chunks = chunk_documents(short_document, chunk_size=100, chunk_overlap=20)
    assert len(chunks) == 1
    assert chunks[0].page_content == short_document[0].page_content


def test_chunk_count_increases_with_size(long_document):
    """Verify that larger documents produce multiple chunks."""
    chunks = chunk_documents(long_document, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1


def test_chunk_target_size(long_document):
    """Verify chunks roughly adhere to the specified chunk_size."""
    chunk_size = 100
    chunks = chunk_documents(long_document, chunk_size=chunk_size, chunk_overlap=20)

    for chunk in chunks:
        # LangChain's splitter might occasionally exceed by a few chars depending on word boundaries,
        # but it should firmly be around the target size. We test that it doesn't grossly exceed it.
        assert len(chunk.page_content) <= chunk_size + 20


def test_chunk_overlap_exists(long_document):
    """Verify that adjacent chunks share overlapping text to preserve context."""
    chunks = chunk_documents(long_document, chunk_size=100, chunk_overlap=30)

    assert len(chunks) >= 2
    chunk1_text = chunks[0].page_content
    chunk2_text = chunks[1].page_content

    # Extract the end of chunk 1 and see if it appears at the beginning of chunk 2
    # We take the last 15 characters to avoid splitting words exactly at the boundary
    overlap_snippet = chunk1_text[-15:]
    assert overlap_snippet in chunk2_text


def test_metadata_is_preserved(long_document):
    """Verify that every chunk retains the metadata of its parent document."""
    chunks = chunk_documents(long_document, chunk_size=100, chunk_overlap=20)

    assert len(chunks) > 0
    for chunk in chunks:
        assert "source" in chunk.metadata
        assert chunk.metadata["source"] == "long.txt"
        assert "author" in chunk.metadata
        assert chunk.metadata["author"] == "Engineer"
