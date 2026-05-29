"""API routes for the AI Fiction Co-author application."""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


# Request/Response Models
class LoreRequest(BaseModel):
    """Request model for adding lore."""
    content: str = Field(..., min_length=1, description="The lore text content")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Optional metadata for the lore entry"
    )


class LoreResponse(BaseModel):
    """Response model for lore operations."""
    status: str
    id: str


class GenerationParameters(BaseModel):
    """Generation parameters for LLM."""
    temperature: Optional[float] = Field(
        0.7, ge=0.0, le=2.0, description="Sampling temperature"
    )
    top_p: Optional[float] = Field(
        0.9, ge=0.0, le=1.0, description="Nucleus sampling parameter"
    )
    repeat_penalty: Optional[float] = Field(
        1.1, ge=1.0, description="Repeat penalty"
    )
    num_predict: Optional[int] = Field(
        500, ge=1, description="Number of tokens to predict"
    )


class GenerateRequest(BaseModel):
    """Request model for story generation."""
    prompt: str = Field(..., min_length=1, description="The user's creative prompt")
    parameters: Optional[GenerationParameters] = None


class GenerateResponse(BaseModel):
    """Response model for story generation."""
    story_segment: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    message: str


def create_routes(rag_service) -> APIRouter:
    """Create API routes with RAG service dependency.
    
    Args:
        rag_service: The RAG service instance.
        
    Returns:
        The configured API router.
    """
    router = APIRouter()

    @router.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        try:
            is_healthy = rag_service.is_healthy()
            if is_healthy:
                return HealthResponse(
                    status="healthy",
                    message="Application is running and services are available",
                )
            else:
                return HealthResponse(
                    status="degraded",
                    message="Application is running but some services may be unavailable",
                )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(
                status_code=503,
                detail="Service unavailable"
            )

    @router.post("/api/lore", response_model=LoreResponse, status_code=201)
    async def add_lore(request: LoreRequest):
        """Add a new lore entry to the lorebook.
        
        This endpoint accepts a text snippet, generates an embedding using
        Sentence-Transformers, and stores it in ChromaDB for later retrieval.
        """
        try:
            logger.info(f"Adding lore: {request.content[:50]}...")
            
            lore_id = rag_service.add_lore(
                content=request.content,
                metadata=request.metadata,
            )
            
            return LoreResponse(status="success", id=lore_id)
        except Exception as e:
            logger.error(f"Failed to add lore: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to add lore: {str(e)}"
            )

    @router.post("/api/generate", response_model=GenerateResponse)
    async def generate_story(request: GenerateRequest):
        """Generate a story segment using the RAG pipeline.
        
        This endpoint:
        1. Takes a user prompt
        2. Retrieves relevant lore from ChromaDB
        3. Constructs a prompt with persona + context + user input
        4. Generates text using Ollama
        5. Returns the generated story segment
        """
        try:
            logger.info(f"Generating story: {request.prompt[:50]}...")
            
            params = request.parameters or GenerationParameters()
            
            story_segment = rag_service.generate_story(
                prompt=request.prompt,
                temperature=params.temperature,
                top_p=params.top_p,
                repeat_penalty=params.repeat_penalty,
                num_predict=params.num_predict,
            )
            
            return GenerateResponse(story_segment=story_segment)
        except Exception as e:
            logger.error(f"Failed to generate story: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate story: {str(e)}"
            )

    return router
