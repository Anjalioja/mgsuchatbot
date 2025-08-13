import pickle

# Load the model safely
with open("model.pkl", "rb") as f:
    vectorizer, model, data = pickle.load(f)

# Function to get bot response
def get_response(msg):
    X_test = vectorizer.transform([msg])
    tag = model.predict(X_test)[0]
    for intent in data["intents"]:
        if intent["tag"] == tag:
            return intent["responses"][0]
    return "Sorry, mujhe samajh nahi aaya. Please try again."

# Run a test chat
while True:
    msg = input("You: ")
    if msg.lower() == "quit":
        break
    print("Bot:", get_response(msg))

