import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Model Configurations
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
TEMPERATURE = 0.3

# RAG Configurations (Optimized based on Phase 6 Benchmarks)
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
TOP_K = 4
