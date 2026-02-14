# import numpy as np
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity


# class IntentDetector:
#     def __init__(self):
#         # Use the SAME model you already rely on
#         self.model = SentenceTransformer("all-MiniLM-L6-v2")

#         # Intent definitions (meaning-based, not keywords)
#         self.intents = {
#             "GREETING": "User is greeting the assistant",
#             "SUMMARY": "User wants a brief overview or summary of the manual",
#             "QUESTION": "User is asking a specific question about the manual content",
#             "REASONING": "User is asking whether a logical rule, decision flow, or evaluation logic is correct",
#         }

#         # Precompute embeddings for intent descriptions
#         self.intent_names = list(self.intents.keys())
#         self.intent_embeddings = self.model.encode(
#             list(self.intents.values()),
#             convert_to_numpy=True
#         )

#     def detect_intent(self, text: str, threshold: float = 0.35) -> str | None:
#         clean = text.lower().strip()

#         # 🔹 Guard 1: very short messages → greeting
#         if len(clean.split()) <= 2:
#             return "GREETING"

#         text_embedding = self.model.encode([text], convert_to_numpy=True)

#         similarities = cosine_similarity(
#             text_embedding, self.intent_embeddings
#         )[0]

#         best_idx = int(np.argmax(similarities))
#         best_score = similarities[best_idx]

#         if best_score < threshold:
#             return None

#         return self.intent_names[best_idx]

