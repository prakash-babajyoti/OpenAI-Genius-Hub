from flask import Blueprint, request, jsonify
import logging
from src.services.openai_client import OpenAIGeniusClient
from src.services.text_translator_service import TextTranslator

# Initialize logger
logger = logging.getLogger(__name__)

# Define the Blueprint for the translation endpoints
translate_bp = Blueprint('translate', __name__)


@translate_bp.route('/translate', methods=['POST'])
def translate_text():
    """
    A Flask API endpoint that translates text from one language to another using OpenAI.

    Expects a JSON payload with 'api_key', 'source_lang', 'target_lang', and 'text' fields.
    """
    try:
        data = request.get_json()

        # Extract required fields from the request
        api_key = data.get("api_key")
        source_lang = data.get("source_lang")
        target_lang = data.get("target_lang")
        text = data.get("text")

        # Validate input
        if not api_key or not source_lang or not target_lang or not text:
            logger.error("Missing fields: api_key, source_lang, target_lang, and text are required.")
            return jsonify({"error": "api_key, source_lang, target_lang, and text are required"}), 400

        # Initialize OpenAIGeniusClient with the API key
        client = OpenAIGeniusClient(api_key, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000)

        # Create TextTranslator instance
        translator = TextTranslator(source_lang, target_lang, text)

        # Perform translation
        translation, tokens_used = translator.execute(client)

        # Respond with the translation result
        logger.info(f"Translation successful. Tokens used: {tokens_used}")
        return jsonify({
            "translation": translation,
            "tokens_used": tokens_used
        }), 200

    except Exception as e:
        logger.error(f"Error during translation: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
