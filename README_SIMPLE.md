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
- **Detailed Guide**: See full README.md
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
