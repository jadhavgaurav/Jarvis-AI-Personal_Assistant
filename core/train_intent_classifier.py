import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from pathlib import Path

def load_intents(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    texts = []
    labels = []

    for intent, values in data.items():
        for example in values["examples"]:
            texts.append(example.lower())
            labels.append(intent)

    return texts, labels

def train_and_save_model(intents_path="data/intents.json", out_dir="data/"):
    print("[⚙️] Training intent classifier on full dataset...")

    X, y = load_intents(intents_path)

    # Build pipeline
    vectorizer = TfidfVectorizer()
    classifier = LogisticRegression(max_iter=1000)

    X_vec = vectorizer.fit_transform(X)
    classifier.fit(X_vec, y)

    # Save models
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, f"{out_dir}/tfidf_vectorizer.pkl")
    joblib.dump(classifier, f"{out_dir}/intent_model.pkl")

    print(f"[✅] Trained and saved: {out_dir}/intent_model.pkl & tfidf_vectorizer.pkl")

if __name__ == "__main__":
    train_and_save_model()
