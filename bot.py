import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from llm.router import summarize
import time

LAST_CALL = {}
COOLDOWN = 5  # seconds

from crypto_utils import decrypt_data
from manual_loader import load_all_manuals, chunk_text , summarize_manual
from semantic_search import SemanticSearch
from llm.llm_summarizer import summarize_with_llm
#from intent_detector import IntentDetector
from llm.intent_router import classify_intent

#intent_detector = IntentDetector()


import asyncio
from functools import partial

async def run_blocking(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args))

load_dotenv()

# Load encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()

# Decrypt Discord token
with open("secrets.enc", "rb") as f:
    encrypted_token = f.read()

DISCORD_TOKEN = decrypt_data(encrypted_token, ENCRYPTION_KEY)

# Discord setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)



manual_text = load_all_manuals()
chunks = chunk_text(manual_text)

if not chunks:
    raise RuntimeError(
        "No manual content found. "
        "Ensure manuals contain readable text."
    )

semantic_search = SemanticSearch(chunks)

DISCORD_LIMIT = 2000

def safe_reply(text):
    if len(text) <= DISCORD_LIMIT:
        return text
    return text[:DISCORD_LIMIT - 20] + "\n\n…(truncated)"

def is_bot_mentioned(message, bot):
    content = message.content.lower()

    # 1️⃣ Proper Discord mention (best)
    if bot.user in message.mentions:
        return True

    # 2️⃣ Raw mention formats
    mention_1 = f"<@{bot.user.id}>"
    mention_2 = f"<@!{bot.user.id}>"

    if mention_1 in message.content or mention_2 in message.content:
        return True

    # 3️⃣ Fallback: name text
    if "maxx" in content:
        return True

    return False


@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")

DISCORD_LIMIT = 2000


def safe_reply(text):
    """Ensure reply fits Discord message limit."""
    if len(text) <= DISCORD_LIMIT:
        return text
    return text[:DISCORD_LIMIT - 20] + "\n\n…(truncated)"


def brief_text(text, max_lines=5):
    """Return a concise version of retrieved context."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines[:max_lines])
SUMMARY_KEYWORDS = {
    "brief", "summarize", "summary", "overview", "explain the manual", "about the manual"
}

def is_summary_request(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in SUMMARY_KEYWORDS)





@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not is_bot_mentioned(message, bot):
        return

    await message.add_reaction("🤖")

    user_text = message.content.strip()
    #intent = classify_intent(user_text)
    intent = await run_blocking(classify_intent, user_text)
    now = time.time()
    last = LAST_CALL.get(message.author.id, 0)

    if now - last < COOLDOWN:
        await message.reply("⏳ Please wait a moment before asking again.")
        return

    LAST_CALL[message.author.id] = now


    # 1️⃣ Greeting
    if intent == "GREETING":
        await message.reply(
            "Hey 👋\n"
            "I can answer questions, explain logic, or summarize the manual.\n\n"
            "Try:\n"
            "• `@Maxx please brief the manual`\n"
            "• `@Maxx explain instruction retention`\n"
            "• `@Maxx is this logic correct?`"
        )
        return

    # 2️⃣ Manual summary
    if intent == "MANUAL_SUMMARY":
        text_for_summary = "\n\n".join(chunks[:5])
        reply = safe_reply(summarize(text_for_summary))
        await message.reply(reply)
        return

    # 3️⃣ Manual question
    if intent == "MANUAL_QUESTION":
        results = semantic_search.search(user_text)

        if not results:
            await message.reply("❌ This information is not available in the manuals.")
        else:
            reply = safe_reply(brief_text("\n\n".join(results[:2])))
            await message.reply(reply)
        return

    # 4️⃣ Logic / reasoning
    if intent == "LOGIC_REASONING":
        await message.reply(
            "Let me reason through this step by step.\n\n"
            "Failing the testing axis is a hard reject.\n"
            "Quality checks never override axis failure.\n\n"
            "Correct logic:\n"
            "• Failed axis → REJECT\n"
            "• Passed axis → ACCEPT (quality affects score, not decision)"
        )
        return
    if intent == "FALLBACK":
        await message.reply(
        "⚠️ I’m a bit busy right now.\n"
        "Please try again in a few seconds."
    )
        return

    # 5️⃣ Unknown
    await message.reply(
        "🤔 I understand your message, but I’m not sure how to help yet.\n"
        "You can ask about the manual, request a summary, or ask for reasoning."
    )








manual_text = load_all_manuals()
print("🔹 manual_text length:", len(manual_text))

chunks = chunk_text(manual_text)
print("🔹 chunks count:", len(chunks))


bot.run(DISCORD_TOKEN)
