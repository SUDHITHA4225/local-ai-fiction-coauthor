"""Utilities for managing prompts and templates."""

from pathlib import Path
from typing import List, Optional
import os


def load_persona_prompt(persona_file: str = "prompts/persona.md") -> str:
    """Load the persona prompt from file.
    
    Args:
        persona_file: Path to the persona prompt file.
        
    Returns:
        The content of the persona prompt file.
        
    Raises:
        FileNotFoundError: If the persona file doesn't exist.
    """
    # Handle both absolute and relative paths
    if os.path.isabs(persona_file):
        path = Path(persona_file)
    else:
        # Try from current directory first
        path = Path(persona_file)
        if not path.exists():
            # Try from project root
            project_root = Path(__file__).parent.parent.parent
            path = project_root / persona_file
    
    if not path.exists():
        raise FileNotFoundError(f"Persona prompt file not found at: {path}")
    
    return path.read_text(encoding="utf-8")


def create_generation_prompt(
    persona: str,
    retrieved_lore: List[str],
    user_prompt: str,
) -> str:
    """Create a complete generation prompt with persona, context, and user input.
    
    Args:
        persona: The AI persona/system prompt.
        retrieved_lore: List of relevant lore snippets from ChromaDB.
        user_prompt: The user's creative prompt.
        
    Returns:
        The complete prompt to send to the LLM.
    """
    lore_context = "\n".join([f"- {lore}" for lore in retrieved_lore])
    
    prompt = f"""{persona}

Here is some relevant context from the lorebook:
--- CONTEXT ---
{lore_context if lore_context else "No relevant lore found."}
--- END CONTEXT ---

Now, continue the story based on this user prompt: {user_prompt}"""
    
    return prompt


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks.
    
    Args:
        text: The text to chunk.
        chunk_size: Size of each chunk in characters.
        overlap: Number of characters to overlap between chunks.
        
    Returns:
        List of text chunks.
    """
    chunks = []
    step = chunk_size - overlap
    
    for i in range(0, len(text), step):
        chunk = text[i : i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks
