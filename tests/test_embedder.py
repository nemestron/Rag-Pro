import pytest
import os
import tempfile
from langchain_core.documents import Document
from rag.embedder import (
    get_embedding_model,
    build_vector_store,
    save_vector_store,
    load_vector_store,
    get_retriever,
)

# --- Fixtures ---


@pytest.fixture(scope="module")
def embedding_model():
    """
    Initialize the embedding model once for the entire test module to save execution time.
    """
    return get_embedding_model()


@pytest.fixture
def sample_chunks():
    """Provide a small set of semantically distinct document chunks."""
    return [
        Document(
            page_content="Python is a highly popular programming language.",
            metadata={"id": 1},
        ),
        Document(page_content="The capital of France is Paris.", metadata={"id": 2}),
        Document(
            page_content="Photosynthesis is the process used by plants to make food.",
            metadata={"id": 3},
        ),
    ]


# --- Test Cases ---


def test_get_embedding_model(embedding_model):
    """Verify the embedding model loads and initializes without errors."""
    assert embedding_model is not None
    assert hasattr(embedding_model, "embed_documents")


def test_build_vector_store(sample_chunks, embedding_model):
    """Verify a FAISS vector store is successfully created from chunks."""
    vector_store = build_vector_store(sample_chunks, embedding_model)
    assert vector_store is not None
    assert hasattr(vector_store, "docstore")


def test_build_vector_store_empty(embedding_model):
    """Verify building a vector store with an empty chunks list raises the correct error."""
    with pytest.raises(ValueError, match="Cannot build vector store"):
        build_vector_store([], embedding_model)


def test_save_and_load_vector_store(sample_chunks, embedding_model):
    """Verify the vector store can be saved to and correctly loaded from the disk."""
    original_store = build_vector_store(sample_chunks, embedding_model)

    # Use a temporary directory to avoid polluting the workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        save_path = os.path.join(temp_dir, "test_faiss_index")

        # Test Saving
        save_vector_store(original_store, save_path)
        assert os.path.exists(save_path)

        # Test Loading
        loaded_store = load_vector_store(save_path, embedding_model)
        assert loaded_store is not None
        assert hasattr(loaded_store, "docstore")


def test_get_retriever(sample_chunks, embedding_model):
    """Verify the retriever is created and respects the top_k parameter."""
    vector_store = build_vector_store(sample_chunks, embedding_model)
    retriever = get_retriever(vector_store, k=2)

    results = retriever.invoke("Tell me about Python.")
    # Should retrieve exactly 2 chunks based on k=2
    assert len(results) == 2


def test_retrieval_relevance(sample_chunks, embedding_model):
    """Verify retrieved chunks are semantically relevant to the user query."""
    vector_store = build_vector_store(sample_chunks, embedding_model)
    # Set k=1 to force it to return only the single most relevant chunk
    retriever = get_retriever(vector_store, k=1)

    # Query specifically about France/Paris
    results = retriever.invoke("What city is the capital of France?")

    assert len(results) == 1
    assert "Paris" in results[0].page_content
