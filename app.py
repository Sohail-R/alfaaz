import os
from flask import Flask, render_template, request, jsonify
from database import init_db, save_word, get_all_words, save_poem_history, get_poem_history
from scraper import scrape_poem
from translator import translate_word_in_context, transliterate

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/read")
def read():
    url = request.args.get("url", "")
    poem = None
    error = None
    if url:
        poem = scrape_poem(url)
        if poem:
            save_poem_history(poem["title"], poem["poet"], url, len(poem["lines"]))
        else:
            error = "Couldn't load that poem. Check the URL and try again."
    return render_template("read.html", poem=poem, error=error, url=url)


@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    urdu_word  = data.get("word")
    context_line = data.get("line")
    poem_title = data.get("title")
    if not urdu_word:
        return jsonify({"error": "No word provided"}), 400
    translation = translate_word_in_context(urdu_word, context_line)
    if translation:
        save_word(urdu_word, translation, poem_title, context_line)
        return jsonify({"word": urdu_word, "translation": translation})
    return jsonify({"error": "Translation failed"}), 500


@app.route("/transliterate", methods=["POST"])
def transliterate_lines():
    data = request.get_json()
    lines = data.get("lines", [])
    combined = "\n".join(lines)
    result = transliterate(combined)
    parts = result.split("\n") if result else []
    while len(parts) < len(lines):
        parts.append("")
    return jsonify({"lines": parts})


@app.route("/vocab")
def vocab():
    words = get_all_words()
    return render_template("vocab.html", words=words)


@app.route("/flashcards")
def flashcards():
    from database import get_smart_deck
    deck = get_smart_deck()
    return render_template("flashcards.html", deck=deck)


@app.route("/review", methods=["POST"])
def review():
    from database import update_review
    data = request.get_json()
    update_review(data.get("word"), data.get("correct"))
    return jsonify({"ok": True})


@app.route("/history")
def history():
    poems = get_poem_history()
    return render_template("history.html", poems=poems)


@app.route("/translate-lines", methods=["POST"])
def translate_poem_lines():
    from deep_translator import GoogleTranslator
    data = request.get_json()
    lines = data.get("lines", [])
    translations = []
    for line in lines:
        try:
            if line.strip():
                t = GoogleTranslator(source="ur", target="en").translate(line)
                translations.append(t or "")
            else:
                translations.append("")
        except Exception as e:
            print(f"Translation error: {e}")
            translations.append("")
    return jsonify({"translations": translations})


if __name__ == "__main__":
    app.run(debug=True)