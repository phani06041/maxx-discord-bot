import requests

def summarize_with_ollama(text: str) -> str | None:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"""
Summarize the following manual clearly.
Use headings and bullet points.
Do not add external information.

TEXT:
{text}
""",
                "stream": False
            },
            timeout=30
        )
        return response.json()["response"].strip()
    except Exception as e:
        print(f"⚠️ Ollama failed: {e}")
        return None
