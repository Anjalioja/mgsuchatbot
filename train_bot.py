import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load data
with open("intents.json") as f:
    data = json.load(f)

X = []
y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        X.append(pattern)
        y.append(intent["tag"])

# Vectorization
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X_vectorized, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump((vectorizer, model, data), f)

print("Model trained and saved.")
