"""RAG (Retrieval-Augmented Generation) service."""

from typing import List, Optional, Dict, Any
import logging
from .embedding_service import EmbeddingService
from .chroma_service import ChromaDBService
from .llm_service import LLMService
from ..utils.prompts import load_persona_prompt, create_generation_prompt

logger = logging.getLogger(__name__)


class RAGService:
    """Service that orchestrates RAG pipeline."""

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        chroma_host: str = "chromadb",
        chroma_port: int = 8000,
        chroma_collection: str = "story_lore",
        ollama_url: str = "http://ollama:11434",
        ollama_model: str = "llama3.1:8b",
        persona_file: str = "prompts/persona.md",
        top_k: int = 3,
    ):
        """Initialize RAG service.
        
        Args:
            embedding_model: Name of embedding model.
            chroma_host: ChromaDB host.
            chroma_port: ChromaDB port.
            chroma_collection: ChromaDB collection name.
            ollama_url: Ollama API URL.
            ollama_model: Ollama model name.
            persona_file: Path to persona prompt file.
            top_k: Number of documents to retrieve.
        """
        self.embedding_service = EmbeddingService(embedding_model)
        self.chroma_service = ChromaDBService(chroma_host, chroma_port, chroma_collection)
        self.llm_service = LLMService(ollama_url, ollama_model)
        self.persona_file = persona_file
        self.top_k = top_k
        
        # Load persona once
        try:
            self.persona = load_persona_prompt(persona_file)
            logger.info("Loaded persona prompt")
        except FileNotFoundError as e:
            logger.warning(f"Persona file not found: {e}, using empty persona")
            self.persona = ""

    def add_lore(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Add lore to the knowledge base.
        
        Args:
            content: The lore text.
            metadata: Optional metadata.
            
        Returns:
            The ID of the added lore.
        """
        # Generate embedding
        embedding = self.embedding_service.embed_text(content)
        
        # Add to ChromaDB
        lore_id = self.chroma_service.add_lore(content, metadata, embedding)
        
        return lore_id

    def retrieve_context(self, query: str, top_k: Optional[int] = None) -> List[str]:
        """Retrieve relevant context from the knowledge base.
        
        Args:
            query: The query string.
            top_k: Number of results to retrieve (uses default if not specified).
            
        Returns:
            List of relevant lore snippets.
        """
        if top_k is None:
            top_k = self.top_k
        
        # Generate embedding for query
        query_embedding = self.embedding_service.embed_text(query)
        
        # Query ChromaDB
        documents, _, _ = self.chroma_service.query_lore(query_embedding, top_k)
        
        return documents

    def generate_story(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        repeat_penalty: float = 1.1,
        num_predict: int = 500,
        top_k: Optional[int] = None,
    ) -> str:
        """Generate a story segment using RAG.
        
        Args:
            prompt: The user's creative prompt.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            repeat_penalty: Repeat penalty.
            num_predict: Number of tokens to predict.
            top_k: Number of context documents to retrieve.
            
        Returns:
            The generated story segment.
        """
        # Retrieve relevant context
        context = self.retrieve_context(prompt, top_k)
        
        # Create the full prompt
        full_prompt = create_generation_prompt(self.persona, context, prompt)
        
        logger.info(f"Generating with {len(context)} context documents")
        
        # Generate using LLM
        generated_text = self.llm_service.generate(
            full_prompt,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
            num_predict=num_predict,
        )
        
        return generated_text

    def is_healthy(self) -> bool:
        """Check if all services are healthy."""
        try:
            ollama_healthy = self.llm_service.is_healthy()
            logger.info(f"Ollama health: {ollama_healthy}")
            return ollama_healthy
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
