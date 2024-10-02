from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields
import logging
from src.services.openai_client import OpenAIGeniusClient
from src.services.text_translator_service import TextTranslator

# Initialize logger
logger = logging.getLogger(__name__)

# Define the Blueprint for the translation endpoints
translate_bp = Blueprint('translate', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# Initialize Flask-RESTX API with Blueprint
api = Api(
    translate_bp,
    version='1.0',
    title='Translation API',
    description='API for translating text using OpenAI',
    doc='/docs',
    authorizations=authorizations,
    security='apikey'
)

# Define the request model for input validation
translate_model = api.model('Translate', {
    'source_lang': fields.String(required=True, description='Source language of the text'),
    'target_lang': fields.String(required=True, description='Target language for the translation'),
    'text': fields.String(required=True, description='Text to translate')
})

# Define the resource for translation
@api.route('/translate')
class TranslateText(Resource):
    @api.doc('translate_text')
    @api.expect(translate_model, validate=True)
    @api.header('Authorization', 'API key for OpenAI', required=True)
    @api.response(200, 'Translation successful', model=api.model('TranslationResponse', {
        'translation': fields.String(description='Translated text'),
        'tokens_used': fields.Integer(description='Number of tokens used')
    }))
    @api.response(400, 'Bad Request')
    @api.response(401, 'Unauthorized')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """
        Translates text from one language to another using OpenAI.

        Expects the 'Authorization' header with the API key.
        """
        try:
            # Extract the API key from the Authorization header
            api_key = request.headers.get("Authorization")

            if not api_key:
                logger.error("API key missing in Authorization header.")
                return {"error": "API key is required"}, 401

            # Extract required fields from the request JSON
            data = request.get_json()
            source_lang = data.get("source_lang")
            target_lang = data.get("target_lang")
            text = data.get("text")

            if not source_lang or not target_lang or not text:
                logger.error("Missing fields: source_lang, target_lang, and text are required.")
                return jsonify({"error": "source_lang, target_lang, and text are required"}), 400

            # Initialize OpenAIGeniusClient with the API key
            client = OpenAIGeniusClient(api_key, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000)

            # Create TextTranslator instance
            translator = TextTranslator(source_lang, target_lang, text)

            # Perform translation
            translation, tokens_used = translator.execute(client)

            logger.info(f"Translation successful. Tokens used: {tokens_used}")
            return {
                "translation": translation,
                "tokens_used": tokens_used
            }, 200

        except Exception as e:
            logger.error(f"Error during translation: {str(e)}", exc_info=True)
            return {"error": str(e)}, 500
