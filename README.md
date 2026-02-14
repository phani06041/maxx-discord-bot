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
