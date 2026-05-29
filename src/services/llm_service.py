"""LLM service for interacting with Ollama."""

import requests
import logging
from typing import Optional, Generator

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Ollama LLM."""

    def __init__(
        self,
        base_url: str = "http://ollama:11434",
        model: str = "llama3.1:8b",
        timeout: int = 300,
    ):
        """Initialize LLM service.
        
        Args:
            base_url: Base URL for Ollama API.
            model: Model name to use.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        
        # Test connection
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            logger.info(f"Connected to Ollama at {self.base_url}")
        except Exception as e:
            logger.warning(f"Could not verify Ollama connection: {e}")

    def is_healthy(self) -> bool:
        """Check if Ollama is healthy."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        repeat_penalty: float = 1.1,
        num_predict: int = 500,
    ) -> str:
        """Generate text using Ollama.
        
        Args:
            prompt: The input prompt.
            temperature: Sampling temperature (0.0 to 2.0).
            top_p: Nucleus sampling parameter (0.0 to 1.0).
            repeat_penalty: Repeat penalty (>= 1.0).
            num_predict: Number of tokens to predict.
            
        Returns:
            The generated text.
        """
        try:
            url = f"{self.base_url}/api/generate"
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "top_p": top_p,
                "repeat_penalty": repeat_penalty,
                "num_predict": num_predict,
            }
            
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("response", "")
            
            logger.info(f"Generated text (length: {len(generated_text)} chars)")
            return generated_text
        except Exception as e:
            logger.error(f"Failed to generate text: {e}")
            raise

    def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        repeat_penalty: float = 1.1,
        num_predict: int = 500,
    ) -> Generator[str, None, None]:
        """Generate text using Ollama with streaming.
        
        Args:
            prompt: The input prompt.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            repeat_penalty: Repeat penalty.
            num_predict: Number of tokens to predict.
            
        Yields:
            Chunks of generated text.
        """
        try:
            url = f"{self.base_url}/api/generate"
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "temperature": temperature,
                "top_p": top_p,
                "repeat_penalty": repeat_penalty,
                "num_predict": num_predict,
            }
            
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    import json
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            yield token
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            logger.error(f"Failed to generate text (streaming): {e}")
            raise
