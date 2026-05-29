"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from pathlib import Path

from .config import get_config
from .services.rag_service import RAGService
from .api.routes import create_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

# Get configuration
config = get_config()

# Initialize RAG service
logger.info("Initializing RAG service...")
rag_service = RAGService(
    embedding_model=config.EMBEDDING_MODEL_NAME,
    chroma_host=config.CHROMA_HOST,
    chroma_port=config.CHROMA_PORT,
    chroma_collection=config.CHROMA_COLLECTION_NAME,
    ollama_url=config.OLLAMA_BASE_URL,
    ollama_model=config.OLLAMA_MODEL,
    persona_file=config.PERSONA_PROMPT_FILE,
    top_k=config.TOP_K_RESULTS,
)
logger.info("RAG service initialized")

# Create FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="AI-powered creative writing assistant with local LLM and RAG",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
routes = create_routes(rag_service)
app.include_router(routes)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="info",
    )
