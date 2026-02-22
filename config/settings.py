import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Model Configurations
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# RAG Configurations
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RETRIEVAL = 4

# LLM Generation Configurations
LLM_TEMPERATURE = 0.3
LLM_MAX_NEW_TOKENS = 512
