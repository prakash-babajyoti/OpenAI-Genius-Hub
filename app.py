import streamlit as st
import logging

from src.components.opeai_client_config import initialize_openai_client
from src.components.sidebar import configure_sidebar
from src.config.logging_config import setup_logging
from src.pages.chat_ui import chat_app
from src.pages.prompt_generator_ui import prompt_generator_ui
from src.pages.text_translator_ui import text_translator_ui
from src.rest_service.flask_server import start_flask_in_thread


def main():
    """Main function to run the AI Assistant Streamlit app."""
    setup_logging()  # Set up logging configuration
    logger = logging.getLogger(__name__)

    # Configure the Streamlit page
    st.set_page_config(page_title="AI Assistant", page_icon="🤖")
    logger.info("Streamlit page configured.")

    # Start Flask server in a separate thread
    logger.info("Starting Flask server...")
    start_flask_in_thread()  # This starts Flask in a separate thread

    # Configure the sidebar and get user input
    sidebar_config = configure_sidebar()

    # Check for OpenAI API key
    api_key = sidebar_config["api_key"]
    if not api_key:
        st.error("Please provide an OpenAI API key to use this application.")
        logger.error("No OpenAI API key provided.")
        st.stop()

    # Initialize OpenAI client
    client = initialize_openai_client(api_key, sidebar_config["model"], sidebar_config["temperature"], sidebar_config["max_tokens"])

    # Load the selected app mode
    app_mode = sidebar_config["app_mode"]
    logger.info(f"App mode selected: {app_mode}")

    if app_mode == "Chat":
        chat_app(client)
    elif app_mode == "Text Translator":
        text_translator_ui(client)
    elif app_mode == "Prompt Engineering Assistant":
        prompt_generator_ui(client)
    else:
        logger.warning(f"Unknown app mode selected: {app_mode}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("An error occurred while running the application.")
