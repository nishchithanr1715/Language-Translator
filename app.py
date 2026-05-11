from flask import Flask, request, jsonify, send_from_directory
from deep_translator import GoogleTranslator
import os

app = Flask(__name__, static_folder='')

# Default target languages
DEFAULT_TARGETS = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru",
    "Korean": "ko",
    "Italian": "it",
    "Turkish": "tr",
}

def translate_text(text: str, source: str = "auto", targets: dict = None):
    """Translate *text* into multiple *targets* using deep-translator.

    Args:
        text: Text to translate.
        source: Source language code ("auto" for detection).
        targets: Mapping name→code. If None, use DEFAULT_TARGETS.
    Returns:
        dict of language name → translated string (or error).
    """
    if targets is None:
        targets = DEFAULT_TARGETS
    results = {}
    for name, code in targets.items():
        try:
            translated = GoogleTranslator(source=source, target=code).translate(text)
            results[name] = translated
        except Exception as e:
            results[name] = f"Error: {e}"
    return results

@app.route("/translate", methods=["POST"])
def translate_endpoint():
    data = request.get_json(force=True)
    text = data.get("text", "")
    source = data.get("source", "auto")
    targets = data.get("targets")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    translations = translate_text(text, source, targets)
    return jsonify({"original": text, "source": source, "translations": translations})

# Serve the UI page
@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(os.getcwd(), "index.html")

if __name__ == "__main__":
    # Development server
    app.run(host="0.0.0.0", port=5000, debug=True)



def translate_to_multiple(text, source='auto', targets=None):
    """Translate a given text into multiple target languages.

    Args:
        text (str): The text to translate.
        source (str): Source language code (default 'auto' for auto‑detect).
        targets (dict): Mapping of language name to language code.
                       If None, a default set of common languages is used.
    Returns:
        dict: Mapping of language name to the translated text.
    """
    if targets is None:
        targets = {
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Hindi': 'hi',
            'Chinese': 'zh-CN',
            'Japanese': 'ja',
            'Arabic': 'ar',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Korean': 'ko',
            'Italian': 'it',
            'Turkish': 'tr',
        }

    results = {}
    for name, code in targets.items():
        try:
            translated = GoogleTranslator(source=source, target=code).translate(text)
            results[name] = translated
        except Exception as e:
            results[name] = f"Error: {e}"
    return results


if __name__ == "__main__":
    # Example usage
    sample_text = "Hello, how are you?"
    translations = translate_to_multiple(sample_text)
    for lang, out in translations.items():
        print(f"{lang}: {out}")
