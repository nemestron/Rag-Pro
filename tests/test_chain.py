import pytest
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document
from rag.chain import (
    init_llm,
    create_prompt_template,
    build_rag_chain,
    ask_question
)

# --- Test Cases ---

@patch("rag.chain.HuggingFaceEndpoint")
@patch("rag.chain.ChatHuggingFace")
def test_init_llm(mock_chat_hf, mock_hf_endpoint):
    """Verify that the LLM wrapper initializes with the correct class without making an API call."""
    llm = init_llm()
    assert llm is not None
    # Verify our code actually attempted to instantiate both LangChain wrappers
    mock_hf_endpoint.assert_called_once()
    mock_chat_hf.assert_called_once()

def test_create_prompt_template():
    """Verify the prompt template enforces strict grounding and contains required variables."""
    prompt = create_prompt_template()
    assert prompt is not None
    
    # LangChain prompt templates must explicitly expect these input variables
    assert "context" in prompt.input_variables
    assert "question" in prompt.input_variables
    
    # Format the prompt into a string to verify the grounding instruction exists
    formatted_prompt = prompt.format(context="dummy_context", question="dummy_question")
    assert "I don't have enough information" in formatted_prompt

@patch("rag.chain.HuggingFaceEndpoint")
@patch("rag.chain.ChatHuggingFace")
def test_build_rag_chain(mock_chat_hf, mock_hf_endpoint):
    """Verify that the LCEL RAG chain assembles successfully."""
    # Setup mock LLM
    mock_llm_instance = MagicMock()
    mock_chat_hf.return_value = mock_llm_instance
    
    # Setup mock retriever
    mock_retriever = MagicMock()
    
    # Build the chain
    chain = build_rag_chain(mock_retriever)
    
    # If the chain object is returned, LCEL successfully piped the components together
    assert chain is not None

@patch("rag.chain.build_rag_chain")
def test_ask_question_valid(mock_build_chain):
    """Verify the ask_question master function correctly invokes the chain."""
    # Setup a mock chain that returns a predefined answer
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "This is a mocked answer grounded in context."
    mock_build_chain.return_value = mock_chain
    
    # Setup a dummy retriever
    mock_retriever = MagicMock()
    
    answer = ask_question("What is the purpose of this test?", mock_retriever)
    
    assert answer == "This is a mocked answer grounded in context."
    # Verify the chain was actually invoked with the user's question
    mock_chain.invoke.assert_called_once_with("What is the purpose of this test?")

def test_ask_question_missing_retriever():
    """Verify the master function gracefully traps a missing retriever state."""
    # Pass None as the retriever to simulate the user not processing documents yet
    answer = ask_question("What is the capital of France?", None)
    
    assert "Please upload and process documents" in answer
