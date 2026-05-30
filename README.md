# Local AI Fiction Co-Author

A local AI-powered fiction writing assistant using **RAG (Retrieval-Augmented Generation)** to maintain story consistency through a lorebook.

## Features

* Add story lore (characters, places, events)
* Context-aware story generation
* Local LLM using Ollama
* Vector database using ChromaDB
* Adjustable creativity parameters (temperature, top_p)

## Tech Stack

* Python
* FastAPI
* Ollama
* ChromaDB
* Sentence Transformers
* Docker

## Setup

### 1. Clone Repository

```bash
git clone <repo-url>
cd local-ai-fiction-coauthor
```

### 2. Create Environment File

```bash
cp .env.example .env
```

### 3. Run the Project

```bash
docker-compose up --build
```

## API Endpoints

### Add Lore

**POST** `/api/lore`

Example:

```json
{
  "content": "The hero carries a glowing sword named Aethelgard."
}
```

### Generate Story

**POST** `/api/generate`

Example:

```json
{
  "prompt": "The hero enters the tavern.",
  "parameters": {
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

## Health Check

```bash
curl http://localhost:8000/health
```

## Project Structure

```text
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── src/
├── prompts/persona.md
├── docs/parameter_effects.md
└── README.md
```

## Purpose

This project helps writers generate fiction while maintaining story consistency using a lorebook and RAG pipeline.

## Conclusion

This project demonstrates how a local AI-powered fiction assistant can generate context-aware stories using **RAG**, **vector databases**, and **LLMs**. By combining **Ollama**, **ChromaDB**, and **FastAPI**, the system maintains story consistency through a lorebook while allowing creative and customizable story generation. The project provides a practical foundation for building private, intelligent, and context-aware AI writing assistants.

