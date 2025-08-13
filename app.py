from flask import Flask, render_template, request, session, redirect, url_for
import pickle
from googletrans import Translator

# Load model
with open("model.pkl", "rb") as f:
    vectorizer, model, intents = pickle.load(f)

app = Flask(__name__)
app.secret_key = 'open any way'

translator = Translator()

# ------------------- Chatbot Logic -------------------
def get_response(user_input, target_lang='en'):
    X_test = vectorizer.transform([user_input])
    tag = model.predict(X_test)[0]
    response = "Sorry, I didn't understand."

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            response = intent["responses"][0]
            break

    # 🌍 Translate response
    if target_lang != "en":
        try:
            translated = translator.translate(response, dest=target_lang).text
            return translated
        except:
            return "Translation error. Please try again."

    return response

# ------------------- Routes -------------------
@app.route("/")
def index():
    return render_template("mgsuchatbot.html")


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot_ui():
    if "chat_history" not in session:
        session["chat_history"] = []
    if "last_message" not in session:
        session["last_message"] = "" 

    bot_response = ""
    last_message = session["last_message"]  # default me pichla message

    if request.method == "POST":
        user_input = request.form["message"]
        lang = request.form.get("lang", "en")  # default English

        bot_response = get_response(user_input, lang)

        session["chat_history"].append({"user": user_input, "bot": bot_response})
        session["last_message"] = user_input  # ✅ last typed message save
        last_message = user_input
        session.modified = True

    return render_template("chat.html", bot_response=bot_response, last_message=last_message)

        

    return render_template("chat.html", bot_response=bot_response ,last_message=last_message )

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_panel"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")

@app.route("/admin")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    
    history = session.get("chat_history", [])
    return render_template("admin.html", history=history)

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(debug=True, port=5050)
