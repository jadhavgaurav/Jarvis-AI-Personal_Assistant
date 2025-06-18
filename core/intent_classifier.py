import os
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class IntentClassifier:
    def __init__(self):
        self.vectorizer_path = "data/tfidf_vectorizer.pkl"
        self.model_path = "data/intent_classifier.pkl"

        self.vectorizer = joblib.load(self.vectorizer_path)
        self.model = joblib.load(self.model_path)

    def predict(self, query: str) -> str:
        X = self.vectorizer.transform([query])
        return self.model.predict(X)[0]

def train_intent_classifier():
    with open("data/intents.json") as f:
        intents = json.load(f)

    X, y = [], []
    for intent, data in intents.items():
        for example in data["examples"]:
            X.append(example.lower())
            y.append(intent)

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    joblib.dump(vectorizer, "data/tfidf_vectorizer.pkl")
    joblib.dump(model, "data/intent_classifier.pkl")
    print("✅ Intent classifier trained and saved to [data/] folder.")


if __name__ == "__main__":
    train_intent_classifier()
