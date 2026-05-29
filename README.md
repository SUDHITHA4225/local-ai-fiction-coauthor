# AI Fiction Co-author

Local AI writing assistant with context-aware story generation.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- 8-16 GB RAM
- 10 GB disk space

### Setup (3 Steps)

```bash
# 1. Create environment file
cp .env.example .env

# 2. Start all services
docker-compose up --build

# 3. Wait 2-3 minutes for services to be ready
```

## API Usage

### Add Story Context
```bash
curl -X POST http://localhost:8000/api/lore \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The hero is a brave knight named Aldrin."
  }'
```

### Generate Story
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Aldrin enters the tavern looking for the informant.",
    "parameters": {
      "temperature": 0.7
    }
  }'
```

### Check Health
```bash
curl http://localhost:8000/health
```

## What It Does

1. **Add Lore** - Store story context (characters, locations, events)
2. **Retrieve Context** - Automatically find relevant lore for new scenes
3. **Generate Stories** - Use LLM + context to write story segments
4. **Control Creativity** - Adjust temperature, top_p, repeat_penalty

## Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| temperature | 0.0-2.0 | Higher = more creative |
| top_p | 0.0-1.0 | Higher = more diverse |
| repeat_penalty | ≥1.0 | Higher = less repetitive |

## Features

✅ Local LLM (no API costs, no data sharing)
✅ Vector database for persistent context
✅ RAG pipeline for smart retrieval
✅ Customizable AI persona
✅ Docker-based deployment
✅ REST API

## Files

```
├── docker-compose.yml     # Service setup
├── Dockerfile            # App container
├── .env.example          # Configuration
├── src/                  # Application code
├── prompts/persona.md    # AI writing style
├── docs/parameter_effects.md # Parameter guide
└── tests/               # Test cases
```

## Documentation

- **Setup**: Follow Quick Start above
- **Detailed Guide**: See DETAILED_README.md
- **Evaluation**: See EVALUATION_GUIDE.md
- **Parameters**: See docs/parameter_effects.md

## Stopping Services

```bash
docker-compose down
```

## Troubleshooting

**Services not starting?**
- Check Docker is running
- Check disk space
- Wait longer (model download on first run)

**Poor generation quality?**
- Improve persona.md
- Add better lore entries
- Adjust temperature

---

Ready to generate stories! 🚀

1. **Local LLM Deployment**: Using Ollama, run open-source models like Llama 3.1 or Mistral on your machine with no external API calls
2. **Retrieval-Augmented Generation (RAG)**: Maintain a vector-indexed "lorebook" of story context that's automatically retrieved and injected into prompts
3. **Persona Control**: Define your AI's writing voice through a detailed system prompt, ensuring consistent tone and style
4. **Generation Parameter Control**: Fine-tune creativity vs. coherence through temperature, nucleus sampling, and penalty parameters

### Why Local AI?

- **Privacy**: Your story ideas never leave your machine
- **No API Costs**: Run unlimited generations without paying per token
- **Full Customization**: Modify models, system prompts, and generation parameters
- **Offline Capable**: Once downloaded, the LLM runs without internet
- **True Collaboration**: Co-author with a model you fully control

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   FastAPI Application                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ POST /api/lore      - Add story context to lorebook   │  │
│  │ POST /api/generate  - Generate story with RAG context │  │
│  │ GET /health         - Health check endpoint           │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
         ↓                              ↓                  ↓
    ┌────────────┐            ┌─────────────────┐   ┌──────────┐
    │ Embedding  │            │   LLM Service   │   │  Persona │
    │ Service    │            │   (Ollama)      │   │  Prompt  │
    │(Sentence   │            │                 │   └──────────┘
    │Transformers)            │ • Llama 3.1     │
    └────────────┘            │ • Mistral       │
         ↓                     │ • Others        │
    ┌────────────┐            └─────────────────┘
    │ ChromaDB   │
    │ Vector DB  │
    │ (Lorebook) │
    └────────────┘
```

## Quick Start

### Prerequisites

- **Docker & Docker Compose**: [Install](https://docs.docker.com/compose/install/)
- **8-16GB RAM**: Required for running the LLM locally
- **5-10GB Disk Space**: For model weights and vector database
- **Stable Internet**: For initial model download (~5-10 GB depending on model)

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd local-ai-fiction-coauthor
   ```

2. **Create Environment File**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if you need to customize:
   - `OLLAMA_MODEL`: Choose a model (default: `llama3.1:8b`)
   - `TOP_K_RESULTS`: Number of lorebook entries to retrieve (default: 3)
   - Generation parameters for fine-tuning output

3. **Start the Application**
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the FastAPI application container
   - Pull and start the Ollama LLM service
   - Pull and start the ChromaDB vector database
   - Perform health checks on all services
   - Download the specified LLM model (~5-10 minutes on first run)

4. **Verify Everything is Running**
   ```bash
   # Check service status
   docker-compose ps

   # Test the health endpoint
   curl http://localhost:8000/health
   ```

### First Story Generation

```bash
# Step 1: Add a lore entry to establish context
curl -X POST http://localhost:8000/api/lore \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The protagonist is a seasoned knight named Aldrin who once served the Dragon Queen. He now seeks redemption for past sins.",
    "metadata": {"category": "character", "character": "Aldrin"}
  }'

# Step 2: Generate a story segment
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Aldrin enters a mystical tavern seeking information about an ancient artifact.",
    "parameters": {
      "temperature": 0.7,
      "top_p": 0.9,
      "repeat_penalty": 1.1
    }
  }'
```

## API Reference

### Health Check

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "message": "Application is running and services are available"
}
```

### Add Lore Entry

**Endpoint**: `POST /api/lore`

**Request**:
```json
{
  "content": "string (The lore text)",
  "metadata": {
    "category": "character|location|item|event",
    "optional_field": "any value"
  }
}
```

**Response** (201 Created):
```json
{
  "status": "success",
  "id": "uuid-string"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/lore \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The Crystal of Eternal Starlight grants visions of the future but drains the user'\''s memories in exchange.",
    "metadata": {"category": "item", "rarity": "legendary"}
  }'
```

### Generate Story

**Endpoint**: `POST /api/generate`

**Request**:
```json
{
  "prompt": "string (The creative prompt)",
  "parameters": {
    "temperature": 0.7,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
    "num_predict": 500
  }
}
```

**Response** (200 OK):
```json
{
  "story_segment": "Generated narrative text..."
}
```

**Parameters Explained**:
- **temperature** (0.0-2.0): Controls randomness. 0.1=deterministic, 0.7=balanced, 1.5+=creative
- **top_p** (0.0-1.0): Nucleus sampling. 0.3=conservative, 0.9=balanced, 1.0=unrestricted
- **repeat_penalty** (≥1.0): Discourages repetition. 1.0=no penalty, 1.5=strong
- **num_predict** (≥1): Maximum tokens to generate

**Example**:
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The ancient tower begins to crumble. Dust falls like snow.",
    "parameters": {
      "temperature": 0.8,
      "top_p": 0.95,
      "repeat_penalty": 1.2,
      "num_predict": 600
    }
  }'
```

## Workflow Examples

### Example 1: Building a Fantasy Novel

```bash
# Add world-building lore
curl -X POST http://localhost:8000/api/lore \
  -d '{"content": "The Kingdom of Aethermoor was built upon ancient elven ruins. Its capital, Silvathel, rises from the Crystalline Peaks."}' 

# Add character profiles
curl -X POST http://localhost:8000/api/lore \
  -d '{"content": "Lady Vex is a master strategist and secretly commands a network of spies."}'

# Add plot elements
curl -X POST http://localhost:8000/api/lore \
  -d '{"content": "The Void Stones are artifacts of immense power, one for each cardinal direction. Their alignment was broken 300 years ago."}'

# Generate opening scene
curl -X POST http://localhost:8000/api/generate \
  -d '{"prompt": "A messenger arrives with urgent news about the North Stone."}'

# Generate next scene with different tone
curl -X POST http://localhost:8000/api/generate \
  -d '{
    "prompt": "Lady Vex considers her options in the throne room.",
    "parameters": {"temperature": 0.5}
  }'
```

### Example 2: Experimenting with Writing Styles

```bash
# Fast-paced action (low temp, high repeat penalty)
curl -X POST http://localhost:8000/api/generate \
  -d '{"prompt": "Combat erupts in the marketplace.", "parameters": {"temperature": 0.4, "repeat_penalty": 1.5}}'

# Atmospheric description (moderate temp, high top_p)
curl -X POST http://localhost:8000/api/generate \
  -d '{"prompt": "The haunted mansion awaits at midnight.", "parameters": {"temperature": 0.8, "top_p": 0.95}}'

# Experimental/surreal (high temp, high top_p)
curl -X POST http://localhost:8000/api/generate \
  -d '{"prompt": "Reality fragments around the ritual site.", "parameters": {"temperature": 1.4, "top_p": 1.0}}'
```

## Configuration

### Environment Variables

All configuration is managed via `.env`:

```bash
# API Settings
DEBUG=False                          # Enable debug logging
API_PORT=8000                        # FastAPI port
API_HOST=0.0.0.0                    # Bind to all interfaces

# Ollama (LLM)
OLLAMA_BASE_URL=http://ollama:11434 # Ollama API endpoint
OLLAMA_MODEL=llama3.1:8b             # Model to use
OLLAMA_TIMEOUT=300                   # Generation timeout (seconds)

# ChromaDB (Vector Database)
CHROMA_HOST=chromadb                 # ChromaDB host
CHROMA_PORT=8000                     # ChromaDB port
CHROMA_COLLECTION_NAME=story_lore   # Collection name

# Embeddings
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2  # Sentence-Transformer model

# RAG
TOP_K_RESULTS=3                      # Documents to retrieve
CHUNK_SIZE=500                       # Text chunk size
CHUNK_OVERLAP=50                     # Chunk overlap

# Generation Defaults
DEFAULT_TEMPERATURE=0.7              # Default temperature
DEFAULT_TOP_P=0.9                    # Default top_p
DEFAULT_REPEAT_PENALTY=1.1           # Default repeat penalty
DEFAULT_NUM_PREDICT=500              # Default token count

# Persona
PERSONA_PROMPT_FILE=prompts/persona.md
```

### Model Selection

Popular models for creative writing:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `mistral:7b` | 4GB | ⚡⚡⚡ | 🌟🌟 | Quick generation, general use |
| `llama3.1:8b` | 5GB | ⚡⚡ | 🌟🌟🌟 | Balanced, high quality |
| `neural-chat:7b` | 4GB | ⚡⚡⚡ | 🌟🌟 | Dialogue and conversation |
| `nous-hermes2:10.7b` | 6GB | ⚡⚡ | 🌟🌟🌟 | Creative and imaginative |

Change in `.env`:
```bash
OLLAMA_MODEL=mistral:7b  # Faster
OLLAMA_MODEL=llama3.1:8b  # More capable
```

## Project Structure

```
local-ai-fiction-coauthor/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── api/
│   │   └── routes.py           # API endpoint definitions
│   ├── services/
│   │   ├── embedding_service.py    # Sentence-Transformers wrapper
│   │   ├── chroma_service.py       # ChromaDB interactions
│   │   ├── llm_service.py          # Ollama integration
│   │   └── rag_service.py          # RAG pipeline orchestration
│   └── utils/
│       └── prompts.py          # Prompt loading and templates
├── prompts/
│   └── persona.md              # AI writing persona definition
├── docs/
│   └── parameter_effects.md    # Generation parameter analysis
├── tests/
│   └── test_api.py             # API integration tests
├── docker-compose.yml          # Multi-service orchestration
├── Dockerfile                  # Application container
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## Understanding RAG (Retrieval-Augmented Generation)

The core innovation of this system is the RAG pipeline:

### Problem
Standard LLMs have limited context windows (typically 8K-128K tokens). A novel has far more content than fits in memory. Without external context, the AI might contradict established plot points or forget character details.

### Solution: RAG Pipeline

1. **User provides prompt**: "Aldrin enters the tavern seeking the informant."

2. **Embedding**: The prompt is converted to a vector using Sentence-Transformers:
   ```
   "Aldrin enters the tavern seeking the informant."
   ↓
   [0.143, -0.521, 0.872, ..., 0.201]  (384-dimensional vector)
   ```

3. **Retrieval**: This vector is compared against all vectors in ChromaDB using cosine similarity. The 3 most similar lore entries are retrieved:
   ```
   1. "Aldrin is a seasoned knight seeking redemption..."
   2. "The tavern is located in the market district, known for intrigue..."
   3. "The informant goes by the name 'Shadow,' a mysterious figure..."
   ```

4. **Context Injection**: Retrieved lore is injected into the prompt sent to Ollama:
   ```
   [Persona system prompt]
   
   Relevant context:
   - Aldrin is a seasoned knight seeking redemption...
   - The tavern is located in the market district...
   - The informant goes by the name 'Shadow'...
   
   User prompt: "Aldrin enters the tavern seeking the informant."
   ```

5. **Generation**: Ollama generates a coherent continuation that respects both the persona and the retrieved context.

This ensures the AI "remembers" your world and characters even across a long narrative.

## Advanced Usage

### Custom Persona

Edit `prompts/persona.md` to define your AI's writing voice:

```markdown
# My Custom Persona

You are a master of noir detective fiction. Your prose is:
- Hard-boiled and cynical
- Heavy on sensory details
- Featuring unreliable narrators
- Set in 1940s urban environments

...
```

Restart the application for changes to take effect:
```bash
docker-compose restart app
```

### Fine-Tuning Generation Parameters

For **descriptive, atmospheric scenes**:
```bash
curl -X POST http://localhost:8000/api/generate \
  -d '{
    "prompt": "Describe the haunted mansion.",
    "parameters": {
      "temperature": 0.8,
      "top_p": 0.95,
      "repeat_penalty": 1.2,
      "num_predict": 800
    }
  }'
```

For **snappy dialogue**:
```bash
curl -X POST http://localhost:8000/api/generate \
  -d '{
    "prompt": "\"Let'\''s cut to the chase,\" said Vex.",
    "parameters": {
      "temperature": 0.5,
      "top_p": 0.8,
      "repeat_penalty": 1.3,
      "num_predict": 300
    }
  }'
```

See `docs/parameter_effects.md` for detailed analysis of each parameter's effects.

### Batch Lore Import

Create a Python script to import large documents:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

with open("my_novel_notes.txt") as f:
    chapters = f.read().split("---")

for i, chapter_notes in enumerate(chapters):
    response = requests.post(
        f"{BASE_URL}/api/lore",
        json={"content": chapter_notes, "metadata": {"chapter": i}}
    )
    print(f"Chapter {i}: {response.json()['id']}")
```

## Troubleshooting

### Services Not Starting

**Issue**: `docker-compose up` hangs or services fail to start.

**Solution**:
```bash
# Check logs
docker-compose logs ollama
docker-compose logs chromadb
docker-compose logs app

# Verify Docker has enough resources
docker stats

# If OOM errors, increase Docker memory allocation in Docker Desktop settings
```

### Ollama Model Download Too Slow

**Issue**: Model download is taking hours or stalling.

**Solutions**:
- Check internet connection: `ping github.com`
- Try a smaller model: Change `OLLAMA_MODEL` to `mistral:7b` (4GB)
- Monitor download: `docker-compose logs -f ollama | grep download`

### Poor Generation Quality

**Issue**: Generated text is incoherent or repetitive.

**Solutions**:
1. **Improve persona prompt** (`prompts/persona.md`): Be more specific about desired style
2. **Improve lore quality**: Add detailed, well-written context
3. **Adjust parameters**:
   - Lower temperature: `0.5` instead of `0.7` (more coherent)
   - Raise repeat_penalty: `1.3` instead of `1.1` (less repetitive)
4. **Try a different model**: Some models are better for creative writing
   - Good: `llama3.1:8b`, `nous-hermes2:10.7b`
   - Less ideal: Very small models like `phi:2b`

### RAG Not Working (Lore Not Used)

**Issue**: Generated text ignores the lore you added.

**Debugging**:
```bash
# 1. Verify lore was added
curl http://localhost:8000/api/lore -d '{"content": "Test lore about a blue dragon"}'
# Should return an ID

# 2. Generate with very specific query
curl http://localhost:8000/api/generate \
  -d '{"prompt": "The blue dragon descended from the sky."}'

# 3. Check app logs
docker-compose logs app

# Common fixes:
# - Ensure ChromaDB is healthy: docker-compose ps
# - Restart services: docker-compose restart
# - Clear and re-add lore
```

### Out of Memory

**Issue**: `docker-compose up` crashes with OOM error.

**Solutions**:
1. **Switch to smaller model**:
   ```bash
   # In .env
   OLLAMA_MODEL=mistral:7b  # Instead of llama3.1:8b
   ```

2. **Reduce Docker memory limit** or increase host memory

3. **Use quantized models** (lower precision = less memory):
   ```bash
   OLLAMA_MODEL=mistral:7b-q4_K_M  # 4-bit quantized
   ```

## Performance Considerations

| Component | Hardware Impact | Optimization |
|-----------|-----------------|--------------|
| Ollama LLM | CPU+GPU intensive | Use GPU if available; choose smaller model |
| ChromaDB | Low memory footprint | Minimal impact |
| Embeddings | CPU bound, fast | Minimal impact |
| API | Minimal | Handles high concurrent load |

**Estimated Resource Usage**:
- Ollama (llama3.1:8b): 6-8 GB RAM, high CPU
- ChromaDB: 100 MB RAM minimum
- FastAPI app: 200 MB RAM
- Total: ~7-9 GB with all services running

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r requirements.txt pytest pytest-asyncio

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_api.py::test_health_check -v
```

## Model Licenses & Acknowledgments

- **Ollama**: Open-source, MIT license
- **ChromaDB**: Apache 2.0 license
- **Sentence-Transformers**: Apache 2.0 license
- **Llama 3.1**: Meta AI, subject to acceptable use policy
- **Mistral**: Mistral AI, open license
- **FastAPI**: MIT license

Ensure you comply with model licenses when deploying commercially.

## Contributing

To improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests: `pytest tests/`
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Roadmap

- [ ] Web UI dashboard for managing lore and generating stories
- [ ] Export stories to markdown/PDF
- [ ] Story statistics (word count, character frequency, theme analysis)
- [ ] Multi-user collaboration features
- [ ] Integration with popular writing software (Scrivener, Google Docs)
- [ ] Advanced RAG with semantic metadata filtering
- [ ] Fine-tuned models specifically for creative writing
- [ ] Streaming generation for real-time feedback

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support & Community

- **Issues**: Found a bug? [Open an issue](./issues)
- **Discussions**: Have a question? Check [discussions](./discussions)
- **Documentation**: See [docs/](./docs/) for detailed guides

## Citation

If you use this project in research or writing, please cite:

```bibtex
@software{ai_fiction_coauthor,
  title={AI Fiction Co-author: Local LLM-Powered Creative Writing Assistant},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/local-ai-fiction-coauthor}
}
```

---

**Happy co-authoring!** 📖✨

Built with ❤️ for writers everywhere.
