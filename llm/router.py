from .llm_summarizer import summarize_with_llm
from .ollama_summarizer import summarize_with_ollama
from .fallback_summarizer import fallback_summary

def summarize(text: str) -> str:
    # 1️⃣ Try GPT
    gpt = summarize_with_llm(text)
    if gpt:
        return gpt

    # 2️⃣ Try local LLM
    local = summarize_with_ollama(text)
    if local:
        return local

    # 3️⃣ Emergency fallback
    return fallback_summary(text)
