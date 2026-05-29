"""Configuration management for the AI Fiction Co-author application."""

import os
from typing import Optional


class Config:
    """Application configuration."""

    # API Configuration
    APP_NAME = "AI Fiction Co-author"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_HOST = os.getenv("API_HOST", "0.0.0.0")

    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "300"))

    # ChromaDB Configuration
    CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
    CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "story_lore")

    # Embedding Configuration
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

    # RAG Configuration
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

    # Generation Parameters (Defaults)
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    DEFAULT_TOP_P = float(os.getenv("DEFAULT_TOP_P", "0.9"))
    DEFAULT_REPEAT_PENALTY = float(os.getenv("DEFAULT_REPEAT_PENALTY", "1.1"))
    DEFAULT_NUM_PREDICT = int(os.getenv("DEFAULT_NUM_PREDICT", "500"))

    # Persona Prompt File
    PERSONA_PROMPT_FILE = os.getenv("PERSONA_PROMPT_FILE", "prompts/persona.md")


def get_config() -> Config:
    """Get the application configuration."""
    return Config()
