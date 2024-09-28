import streamlit as st
import logging
from src.services.openai_client import OpenAIGeniusClient
from src.services.text_translator_service import TextTranslator

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def text_translator_ui(client: "OpenAIGeniusClient"):
    """
    Renders the Text Translator UI in Streamlit.

    Args:
        client (OpenAIGeniusClient): The OpenAI client instance for performing translations.
    """
    st.header("Text Translator")
    logger.info("Text Translator UI loaded.")

    # Define supported languages
    languages = [
        "English", "Hindi", "Spanish", "French", "German", "Italian",
        "Portuguese", "Russian", "Chinese", "Japanese", "Korean"
    ]

    # User input for source and target languages
    source_lang = st.selectbox("Select source language", languages)
    logger.info(f"Source language selected: {source_lang}")

    target_lang = st.selectbox("Select target language", languages)
    logger.info(f"Target language selected: {target_lang}")

    # User input for the text to be translated
    text_to_translate = st.text_area("Enter text to translate", height=150)
    logger.info(f"Text to translate entered: {text_to_translate[:50]}...")  # Log only first 50 characters

    # Only enable translation if text is provided and source/target languages differ
    if st.button("Translate", disabled=not text_to_translate or source_lang == target_lang):
        logger.info("Translate button clicked.")

        if source_lang == target_lang:
            logger.warning("Source and target languages are the same.")
            st.warning("Source and target languages must be different.")
        else:
            with st.spinner("Translating..."):
                translator = TextTranslator(source_lang, target_lang, text_to_translate)
                try:
                    # Perform translation
                    logger.info("Starting translation...")
                    translation, tokens_used = translator.execute(client)
                    logger.info("Translation successful.")

                    # Display results
                    st.text_area("Translation", translation, height=150)
                    st.caption(f"Tokens used: {tokens_used}")
                    logger.info(f"Translation result: {translation[:50]}... (truncated)")
                    logger.info(f"Tokens used: {tokens_used}")
                except Exception as e:
                    logger.error(f"Error during translation: {str(e)}", exc_info=True)
                    st.error(f"Error during translation: {str(e)}")
