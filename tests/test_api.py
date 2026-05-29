"""Integration tests for the AI Fiction Co-author API."""

import pytest
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from src.main import app
from src.services.embedding_service import EmbeddingService
from src.services.chroma_service import ChromaDBService
from src.utils.prompts import load_persona_prompt, create_generation_prompt, chunk_text


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_lore():
    """Sample lore for testing."""
    return {
        "content": "The ancient sword 'Aethelgard' glows with a faint blue light and is said to grant its wielder visions of the future.",
        "metadata": {"category": "item", "rarity": "legendary"}
    }


class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Health check should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_format(self, client):
        """Health check response should have expected format."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert data["status"] in ["healthy", "degraded"]


class TestLoreEndpoint:
    """Test the /api/lore endpoint."""

    def test_add_lore_returns_201(self, client, sample_lore):
        """Adding lore should return 201 Created."""
        response = client.post("/api/lore", json=sample_lore)
        assert response.status_code == 201

    def test_add_lore_response_format(self, client, sample_lore):
        """Lore response should have status and id."""
        response = client.post("/api/lore", json=sample_lore)
        data = response.json()
        assert data["status"] == "success"
        assert "id" in data
        assert isinstance(data["id"], str)
        assert len(data["id"]) > 0

    def test_add_lore_with_metadata(self, client):
        """Adding lore with metadata should work."""
        lore = {
            "content": "The Dragon Queen rules from her crystalline throne.",
            "metadata": {
                "category": "character",
                "character_name": "Dragon Queen",
                "power_level": "god-like"
            }
        }
        response = client.post("/api/lore", json=lore)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"

    def test_add_lore_without_metadata(self, client):
        """Adding lore without metadata should work."""
        lore = {
            "content": "The city of Silvathel stands at the peaks of crystalline mountains."
        }
        response = client.post("/api/lore", json=lore)
        assert response.status_code == 201
        assert response.json()["status"] == "success"

    def test_add_lore_empty_content_fails(self, client):
        """Empty lore content should fail."""
        response = client.post("/api/lore", json={"content": ""})
        assert response.status_code == 422  # Validation error

    def test_add_lore_missing_content_fails(self, client):
        """Missing content field should fail."""
        response = client.post("/api/lore", json={})
        assert response.status_code == 422  # Validation error


class TestGenerateEndpoint:
    """Test the /api/generate endpoint."""

    def test_generate_returns_200(self, client):
        """Generate endpoint should return 200."""
        response = client.post(
            "/api/generate",
            json={"prompt": "The hero enters the tavern."}
        )
        assert response.status_code == 200

    def test_generate_response_format(self, client):
        """Generate response should have story_segment."""
        response = client.post(
            "/api/generate",
            json={"prompt": "The hero enters the tavern."}
        )
        data = response.json()
        assert "story_segment" in data
        assert isinstance(data["story_segment"], str)

    def test_generate_with_default_parameters(self, client):
        """Generate with default parameters should work."""
        response = client.post(
            "/api/generate",
            json={"prompt": "A wizard casts a spell."}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["story_segment"]) > 0

    def test_generate_with_custom_temperature(self, client):
        """Generate with custom temperature should work."""
        response = client.post(
            "/api/generate",
            json={
                "prompt": "Describe the sunset.",
                "parameters": {"temperature": 0.5}
            }
        )
        assert response.status_code == 200

    def test_generate_with_custom_top_p(self, client):
        """Generate with custom top_p should work."""
        response = client.post(
            "/api/generate",
            json={
                "prompt": "Describe the sunset.",
                "parameters": {"top_p": 0.8}
            }
        )
        assert response.status_code == 200

    def test_generate_with_custom_repeat_penalty(self, client):
        """Generate with custom repeat_penalty should work."""
        response = client.post(
            "/api/generate",
            json={
                "prompt": "Describe the sunset.",
                "parameters": {"repeat_penalty": 1.2}
            }
        )
        assert response.status_code == 200

    def test_generate_with_all_parameters(self, client):
        """Generate with all custom parameters should work."""
        response = client.post(
            "/api/generate",
            json={
                "prompt": "Describe the sunset.",
                "parameters": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1,
                    "num_predict": 300
                }
            }
        )
        assert response.status_code == 200

    def test_generate_empty_prompt_fails(self, client):
        """Empty prompt should fail."""
        response = client.post(
            "/api/generate",
            json={"prompt": ""}
        )
        assert response.status_code == 422  # Validation error

    def test_generate_missing_prompt_fails(self, client):
        """Missing prompt should fail."""
        response = client.post("/api/generate", json={})
        assert response.status_code == 422  # Validation error

    def test_generate_temperature_validation(self, client):
        """Invalid temperature should fail validation."""
        # Temperature should be 0.0-2.0, so 3.0 should fail
        response = client.post(
            "/api/generate",
            json={
                "prompt": "Test.",
                "parameters": {"temperature": 3.0}
            }
        )
        assert response.status_code == 422  # Validation error

    def test_generate_top_p_validation(self, client):
        """Invalid top_p should fail validation."""
        # Top_p should be 0.0-1.0, so 1.5 should fail
        response = client.post(
            "/api/generate",
            json={
                "prompt": "Test.",
                "parameters": {"top_p": 1.5}
            }
        )
        assert response.status_code == 422  # Validation error


class TestRAGPipeline:
    """Test RAG pipeline integration."""

    def test_rag_with_retrieved_context(self, client, sample_lore):
        """RAG should retrieve and use context from lore."""
        # Add lore
        lore_response = client.post("/api/lore", json=sample_lore)
        assert lore_response.status_code == 201

        # Generate with related prompt
        generate_response = client.post(
            "/api/generate",
            json={"prompt": "The hero unsheathes his glowing blade."}
        )
        assert generate_response.status_code == 200
        # Response should be generated successfully


class TestUtilityFunctions:
    """Test utility functions."""

    def test_chunk_text_basic(self):
        """Chunk text should split correctly."""
        text = "A" * 1000
        chunks = chunk_text(text, chunk_size=200, overlap=50)
        assert len(chunks) > 1
        assert all(len(c) <= 200 for c in chunks)

    def test_chunk_text_with_small_text(self):
        """Small text should return single chunk."""
        text = "Short text."
        chunks = chunk_text(text, chunk_size=100)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_create_generation_prompt(self):
        """Generation prompt creation should work."""
        persona = "You are a writer."
        lore = ["Detail 1", "Detail 2"]
        user_prompt = "Write about a knight."
        
        full_prompt = create_generation_prompt(persona, lore, user_prompt)
        
        assert persona in full_prompt
        assert "Detail 1" in full_prompt
        assert "Detail 2" in full_prompt
        assert user_prompt in full_prompt

    def test_create_generation_prompt_empty_lore(self):
        """Generation prompt with empty lore should work."""
        persona = "You are a writer."
        lore = []
        user_prompt = "Write about a knight."
        
        full_prompt = create_generation_prompt(persona, lore, user_prompt)
        
        assert persona in full_prompt
        assert user_prompt in full_prompt


class TestEmbeddingService:
    """Test embedding service."""

    def test_embedding_service_initialization(self):
        """Embedding service should initialize."""
        service = EmbeddingService("all-MiniLM-L6-v2")
        assert service.model is not None

    def test_embed_single_text(self):
        """Embedding a single text should work."""
        service = EmbeddingService("all-MiniLM-L6-v2")
        embedding = service.embed_text("The knight enters the tavern.")
        assert isinstance(embedding, list)
        assert len(embedding) == 384  # MiniLM produces 384-dimensional embeddings

    def test_embed_multiple_texts(self):
        """Embedding multiple texts should work."""
        service = EmbeddingService("all-MiniLM-L6-v2")
        texts = [
            "The knight enters the tavern.",
            "The wizard casts a spell.",
            "The dragon soars through the sky."
        ]
        embeddings = service.embed_texts(texts)
        assert len(embeddings) == 3
        assert all(len(e) == 384 for e in embeddings)


class TestPersonaPrompt:
    """Test persona prompt loading."""

    def test_persona_prompt_exists(self):
        """Persona prompt file should exist."""
        # This test assumes prompts/persona.md exists
        # In CI/CD, ensure the file is present
        try:
            persona = load_persona_prompt("prompts/persona.md")
            assert len(persona) >= 100
        except FileNotFoundError:
            pytest.skip("Persona file not found (expected in CI environment)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
