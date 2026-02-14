import os
from openai import OpenAI
from dotenv import load_dotenv
from openai import RateLimitError, APIError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a technical documentation assistant.

Summarize the provided manual content clearly and briefly.
Use headings and bullet points.
Do NOT add information not present in the text.
"""

def summarize_with_llm(text: str) -> str | None:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()

    except RateLimitError:
        print("⚠️ OpenAI quota exceeded — falling back to manual summary")
        return None

    except APIError as e:
        print(f"⚠️ OpenAI API error: {e}")
        return None
