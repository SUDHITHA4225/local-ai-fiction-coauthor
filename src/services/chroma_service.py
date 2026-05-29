"""ChromaDB vector database service."""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import logging
import uuid

logger = logging.getLogger(__name__)


class ChromaDBService:
    """Service for interacting with ChromaDB vector database."""

    def __init__(
        self,
        host: str = "chromadb",
        port: int = 8000,
        collection_name: str = "story_lore",
    ):
        """Initialize ChromaDB service.
        
        Args:
            host: ChromaDB host.
            port: ChromaDB port.
            collection_name: Name of the collection to use.
        """
        try:
            # Connect to ChromaDB server
            self.client = chromadb.HttpClient(host=host, port=port)
            self.collection_name = collection_name
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Connected to ChromaDB and collection '{collection_name}'")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def add_lore(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> str:
        """Add a lore entry to the vector database.
        
        Args:
            content: The lore text content.
            metadata: Optional metadata dictionary.
            embedding: Optional pre-computed embedding.
            
        Returns:
            The ID of the added lore entry.
        """
        try:
            lore_id = str(uuid.uuid4())
            
            if metadata is None:
                metadata = {}
            
            # Add to collection
            if embedding is not None:
                self.collection.add(
                    ids=[lore_id],
                    documents=[content],
                    embeddings=[embedding],
                    metadatas=[metadata],
                )
            else:
                self.collection.add(
                    ids=[lore_id],
                    documents=[content],
                    metadatas=[metadata],
                )
            
            logger.info(f"Added lore entry: {lore_id}")
            return lore_id
        except Exception as e:
            logger.error(f"Failed to add lore: {e}")
            raise

    def query_lore(
        self,
        query_embedding: List[float],
        top_k: int = 3,
    ) -> tuple[List[str], List[List[float]], List[Dict[str, Any]]]:
        """Query the lore database for similar entries.
        
        Args:
            query_embedding: The embedding to query with.
            top_k: Number of top results to return.
            
        Returns:
            Tuple of (documents, embeddings, metadatas).
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
            )
            
            documents = results.get("documents", [[]])[0]
            embeddings = results.get("embeddings", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            
            logger.info(f"Retrieved {len(documents)} lore entries")
            return documents, embeddings, metadatas
        except Exception as e:
            logger.error(f"Failed to query lore: {e}")
            raise

    def get_all_lore(self) -> tuple[List[str], List[str], List[Dict[str, Any]]]:
        """Get all lore entries from the collection.
        
        Returns:
            Tuple of (ids, documents, metadatas).
        """
        try:
            results = self.collection.get()
            
            ids = results.get("ids", [])
            documents = results.get("documents", [])
            metadatas = results.get("metadatas", [])
            
            logger.info(f"Retrieved {len(documents)} total lore entries")
            return ids, documents, metadatas
        except Exception as e:
            logger.error(f"Failed to get all lore: {e}")
            raise

    def clear_collection(self) -> None:
        """Clear all entries from the collection."""
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Cleared collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise
