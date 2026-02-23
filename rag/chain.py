import os
import logging
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Configure module-level logger
logger = logging.getLogger(__name__)

def init_llm():
    """
    Initializes the Hugging Face LLM endpoint wrapped for conversational tasks.
    """
    logger.info("Initializing Meta-Llama-3-8B-Instruct via HuggingFaceEndpoint...")
    
    try:
        base_llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            temperature=0.3,
            max_new_tokens=512
        )
        chat_model = ChatHuggingFace(llm=base_llm)
        logger.info("LLM initialization successful.")
        return chat_model
        
    except Exception as e:
        error_msg = f"Failed to initialize Hugging Face LLM. Details: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

def create_prompt_template():
    """
    Creates the strict grounding ChatPromptTemplate for the RAG chain.
    """
    logger.info("Creating grounding ChatPromptTemplate...")
    
    system_instruction = (
        "You are a helpful assistant. "
        "Answer the question based ONLY on the following context. "
        "If the answer is not in the context, say 'I don't have enough information to answer this question.' "
        "Do not make up information or use external knowledge."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])
    
    return prompt

def format_docs(docs):
    """
    Extracts and joins the text content from a list of LangChain Document objects.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain(retriever):
    """
    Assembles the complete RAG chain using LangChain Expression Language (LCEL).
    """
    logger.info("Assembling LCEL RAG chain...")
    
    llm = init_llm()
    prompt = create_prompt_template()
    
    rag_chain = (
        {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    logger.info("RAG chain assembled successfully.")
    return rag_chain

def ask_question(question: str, retriever) -> str:
    """
    Master function to process a user question through the RAG pipeline.
    
    Args:
        question: The user's input query.
        retriever: The configured vector store retriever.
        
    Returns:
        str: The generated answer or a fallback error message.
    """
    if not retriever:
        logger.warning("Query attempted without an active retriever.")
        return "Please upload and process documents before asking a question."
        
    logger.info(f"Processing question: '{question}'")
    
    try:
        # Build the chain using the provided retriever
        chain = build_rag_chain(retriever)
        
        # Invoke the chain and capture the response
        answer = chain.invoke(question)
        
        logger.info(f"Answer generated successfully: '{answer}'")
        return answer
        
    except Exception as e:
        error_msg = f"An error occurred while generating the answer: {str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    from dotenv import load_dotenv
    from langchain_core.documents import Document
    
    # Configure logging to see the outputs in the terminal
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    load_dotenv()
    
    try:
        test_retriever = RunnableLambda(
            lambda query: [Document(page_content="Retrieval-Augmented Generation bridges the gap between static LLMs and external knowledge bases.")]
        )
        
        print("\n" + "="*50)
        print("--- Testing Master Query Function ---")
        
        # Test 1: Valid Query
        print("\n[Test 1: Valid Query]")
        valid_answer = ask_question("What does RAG bridge the gap between?", test_retriever)
        print(f"Output: {valid_answer}")
        
        # Test 2: No Retriever Error Handling
        print("\n[Test 2: Missing Documents Error Handling]")
        error_answer = ask_question("What is RAG?", None)
        print(f"Output: {error_answer}")
        
        print("\n" + "="*50 + "\n")
        
    except Exception as err:
        print(f"\n[FAILED] Verification Failed: {err}")
