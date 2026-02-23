import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage

def test_hf_access():
    print("--- Starting Hugging Face Access Verification ---")
    load_dotenv()
    
    if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        print("ERROR: HUGGINGFACEHUB_API_TOKEN is missing from .env file.")
        return

    print("INFO: Token found in environment. Initializing LLM endpoint...")
    
    try:
        # 1. Initialize the base endpoint without forcing the 'text-generation' task
        base_llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            temperature=0.3,
            max_new_tokens=512
        )
        
        # 2. Wrap the endpoint in ChatHuggingFace to utilize the "conversational" API route
        chat_model = ChatHuggingFace(llm=base_llm)
        
        print("INFO: Endpoint initialized successfully. Sending test prompt...")
        
        # 3. Format the prompt as a HumanMessage, expected by chat models
        messages = [
            HumanMessage(content="Explain the concept of Retrieval-Augmented Generation (RAG) in exactly one sentence.")
        ]
        
        response = chat_model.invoke(messages)
        
        print("\n[SUCCESS] Received response:\n")
        print(response.content)
        
    except Exception as e:
        print("\n[FAILED] Could not access the model.")
        print(f"Error Details: {str(e)}")

if __name__ == "__main__":
    test_hf_access()
