import logging
from typing import Tuple
from src.services.base_operation import OpenAIOperation
from src.utils.load_yaml import load_yaml

# Initialize logger
logger = logging.getLogger(__name__)

class TextTranslator(OpenAIOperation):
    """
    A class that implements the OpenAIOperation interface to handle text translation
    using the OpenAI client. It translates text from one language to another.
    """

    def __init__(self, source_lang: str, target_lang: str, text: str):
        """
        Initializes the TextTranslator with source and target languages, and the text to translate.

        Args:
            source_lang (str): The source language of the text.
            target_lang (str): The target language for translation.
            text (str): The text to be translated.
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.text = text
        logger.info(f"TextTranslator initialized with source_lang: {self.source_lang}, target_lang: {self.target_lang}")

    def execute(self, client) -> Tuple[str, int]:
        """
        Executes the text translation operation using the provided OpenAI client.

        Args:
            client: The OpenAIClientImpl instance used to perform the translation.

        Returns:
            Tuple[str, int]: The translated text and the number of tokens used.

        Raises:
            ValueError: If any of the required parameters are missing or if source
                        and target languages are the same.
        """
        logger.info("Executing text translation.")
        self._validate_input()

        # Load the prompts from a YAML file
        prompts = load_yaml('src/prompts/text_translator.yml')
        logger.info("Loaded translation prompts from YAML.")

        system_msg = prompts['SYSTEM_TRANSLATOR'].format(
            source_lang=self.source_lang,
            target_lang=self.target_lang
        )

        try:
            # Call the OpenAI API to perform the translation
            translated_text, tokens_used = client.call_openai_api(system_msg, self.text)
            logger.info(f"Translation completed. Tokens used: {tokens_used}")
            return translated_text, tokens_used
        except Exception as e:
            logger.error(f"Error during translation: {e}")
            raise

    def _validate_input(self):
        """
        Validates the input data to ensure the text and language information are valid.

        Raises:
            ValueError: If the text, source language, or target language is missing,
                        or if source and target languages are the same.
        """
        if not self.text or not self.source_lang or not self.target_lang:
            logger.error("Validation failed: Text, source language, and target language are required.")
            raise ValueError("Text, source language, and target language are required")
        if self.source_lang == self.target_lang:
            logger.error("Validation failed: Source and target languages must be different.")
            raise ValueError("Source and target languages must be different")
        logger.info("Input validation passed.")
