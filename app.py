from flask import Flask, request, jsonify, send_from_directory
from deep_translator import GoogleTranslator
import os

app = Flask(__name__, static_folder='')

# Fetch supported languages once
SUPPORTED_LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)

def translate_text(text: str, source: str = "auto", targets: dict = None):
    """Translate *text* into multiple *targets* using deep-translator."""
    if not targets:
        return {}
    
    results = {}
    for name, code in targets.items():
        try:
            translated = GoogleTranslator(source=source, target=code).translate(text)
            results[name] = translated
        except Exception as e:
            results[name] = f"Error: {e}"
    return results

@app.route("/languages", methods=["GET"])
def get_languages():
    """Return all supported languages."""
    return jsonify(SUPPORTED_LANGUAGES)

@app.route("/translate", methods=["POST"])
def translate_endpoint():
    data = request.get_json(force=True)
    text = data.get("text", "")
    targets = data.get("targets")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    if not targets:
        return jsonify({"error": "No target languages selected"}), 400
        
    translations = translate_text(text, source="auto", targets=targets)
    return jsonify({"original": text, "translations": translations})

@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(os.getcwd(), "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
