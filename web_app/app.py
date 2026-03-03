from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja"
}
@app.route("/translate", methods=["POST"])
def translate_api():
    data = request.json
    text = data["text"]
    lang = data["language"]

    translated = translator.translate(text, dest=lang)

    return {"translated_text": translated.text}
@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = ""
    selected_language = "en"

    if request.method == "POST":
        text = request.form["text"]
        selected_language = request.form["language"]

        if text.strip():
            translated = translator.translate(text, dest=selected_language)
            translated_text = translated.text

    return render_template(
        "index.html",
        translated_text=translated_text,
        languages=languages,
        selected_language=selected_language
    )

if __name__ == "__main__":
    app.run(debug=True)