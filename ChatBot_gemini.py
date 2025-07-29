from flask import Flask, render_template, request, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key

# Configure the API key
genai.configure(api_key="your_gemini_API")

def generate_text(prompt):
    """Generates text using Gemini 1.5 Flash."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/", methods=["GET", "POST"])
def chat():
    """Handles the chatbot conversation."""
    if "chat_history" not in session:
        session["chat_history"] = []  # Initialize if missing

    if request.method == "POST":
        user_input = request.form["user_input"]
        response = generate_text(user_input)

        # Append new input and output to the existing history
        session["chat_history"].append({"user": user_input, "bot": response})
        session.modified = True  # Ensure session updates are saved

    return render_template("chat.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True)
