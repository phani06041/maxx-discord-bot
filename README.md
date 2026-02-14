# Maxx – Context-Aware Discord Bot

Maxx is a Discord bot that:
- Answers questions from instruction manuals (PDF, text)
- Uses semantic search (Sentence Transformers)
- Supports summaries and reasoning
- Uses local LLMs (Ollama) with safe fallbacks

## Features
- Manual-based Q&A (no hallucination)
- Context-aware semantic search
- LLM-powered summaries (OpenAI / Ollama)
- Intent routing
- Safe secret handling

## Setup

### 1. Clone repo
git clone <your-repo-url>  
cd maxx  

### 2. Create virtual environment
python -m venv venv  
source venv/bin/activate  

### 3. Install dependencies
pip install -r requirements.txt  

### 4. Environment variables
Create a `.env` file with the following:

DISCORD_TOKEN=your_token  
OPENAI_API_KEY=optional  

### 5. Run Ollama (optional but recommended)
ollama serve  
ollama pull llama3  

### 6. Run bot
python bot.py






## Project Structure

```text
Maxx/
├── bot.py                     # Discord bot entry point
├── manual_loader.py           # Loads manuals (PDF, text, pages)
├── semantic_search.py         # Embedding-based semantic search over manuals
├── intent_detector.py         # Lightweight intent detection (fallback logic)
├── crypto_utils.py            # Encryption / decryption utilities
├── encrypt.py                 # Script to encrypt secrets into secrets.enc
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore rules (secrets, venv, cache)
│
├── Manuals/                   # Instruction manuals (local or demo data)
│   ├── multichallenge.pdf
│   └── multichallenge.pages
│
└── llm/                       # LLM-related logic
    ├── __init__.py
    ├── router.py              # Routes between summarizers / LLM backends
    ├── intent_router.py       # LLM-based intent classification (Ollama)
    ├── llm_summarizer.py      # OpenAI-based summarization
    ├── ollama_summarizer.py   # Local Ollama-based summarization
    └── fallback_summarizer.py # Non-LLM fallback summarizer
```
### Architecture Overview

- The bot uses **semantic search** to answer questions strictly from manuals.
- **LLM usage is optional** and routed safely:
  - Ollama (local) for intent detection and summaries
  - OpenAI only if configured
- Encryption utilities ensure secrets are never committed to GitHub.
- Heavy LLM calls are isolated to avoid blocking the Discord event loop.



---
Made with ❤️ and an obsession by Phanindra
