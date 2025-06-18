import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util


class IntentClassifier:
    def __init__(self, threshold=0.6):
        self.intents_path = "data/intents.json"
        self.model_name = "all-MiniLM-L6-v2"
        self.threshold = threshold

        # Load sentence transformer
        self.encoder = SentenceTransformer(self.model_name)

        # Load intents and prepare embeddings
        self.intents, self.intent_embeddings = self._load_intents()

    def _load_intents(self):
        if not os.path.exists(self.intents_path):
            raise FileNotFoundError(f"[❌] Missing intents file: {self.intents_path}")

        with open(self.intents_path, "r", encoding="utf-8") as f:
            raw_intents = json.load(f)

        intents = {}
        all_sentences = []
        for intent, data in raw_intents.items():
            examples = data.get("examples", [])
            intents[intent] = examples
            all_sentences.extend(examples)

        embeddings = self.encoder.encode(all_sentences, convert_to_tensor=True)

        # Map sentence idx → intent
        sentence_to_intent = []
        for intent, examples in intents.items():
            sentence_to_intent.extend([intent] * len(examples))

        return sentence_to_intent, embeddings

    def predict(self, query: str) -> str:
        query_embedding = self.encoder.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, self.intent_embeddings)[0]  # shape: (n_examples,)
        best_score = float(scores.max())
        best_index = int(scores.argmax())
        predicted_intent = self.intents[best_index]

        print(f"[🔍] Predicted Intent: {predicted_intent} (Confidence: {best_score:.2f})")

        if best_score < self.threshold:
            return "unknown"

        return predicted_intent
