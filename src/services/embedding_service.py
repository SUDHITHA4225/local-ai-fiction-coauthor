"""Embedding service for converting text to vectors."""

from sentence_transformers import SentenceTransformer
from typing import List
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using Sentence-Transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding service.
        
        Args:
            model_name: Name of the Sentence-Transformer model to use.
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model {model_name}: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text.
        
        Args:
            text: The text to embed.
            
        Returns:
            A list of floats representing the embedding.
        """
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Failed to embed text: {e}")
            raise

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed.
            
        Returns:
            List of embeddings.
        """
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Failed to embed texts: {e}")
            raise
