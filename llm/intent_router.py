import requests

PROMPT = """
You are an intent classifier for a Discord assistant.

Classify the user's message into ONE of the following labels:

- GREETING
- MANUAL_SUMMARY
- MANUAL_QUESTION
- LOGIC_REASONING
- GENERAL_QUESTION
- UNKNOWN

User message:
\"\"\"{text}\"\"\"

Respond with ONLY the label.
"""

def classify_intent(text: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": PROMPT.format(text=text[:2000]),
                "stream": False
            },
            timeout=45  # hard cap
        )

        label = response.json()["response"].strip().upper()
        return label

    except Exception as e:
        print("⚠️ Intent router failed:", e)
        return "FALLBACK"


    except Exception as e:
        print("⚠️ Intent router failed:", e)
        return "UNKNOWN"
