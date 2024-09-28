import streamlit as st
import logging
from src.config.logging_config import setup_logging
from src.pages.chat_ui import chat_app
from src.pages.prompt_generator_ui import prompt_generator_ui
from src.pages.text_translator_ui import text_translator_ui
from src.services.openai_client import OpenAIGeniusClient


def main():
    """Main function to run the AI Assistant Streamlit app."""
    setup_logging()  # Set up logging configuration
    logger = logging.getLogger(__name__)  # Get logger instance for this module

    # Configure the Streamlit page
    st.set_page_config(page_title="AI Assistant", page_icon="🤖")
    logger.info("Streamlit page configured.")

    # Input for OpenAI API key
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    st.sidebar.markdown("[Get OpenAI API Key](https://platform.openai.com/account/api-keys)")

    if not api_key:
        st.error("Please provide an OpenAI API key to use this application.")
        logger.error("No OpenAI API key provided.")
        st.stop()

    # Sidebar navigation for selecting the app mode
    st.sidebar.title("Navigation")
    options = [
        "Chat",
        "Text Translator",
        "Prompt Engineering Assistant",
    ]

    # Create selectbox with grouped options
    app_mode = st.sidebar.selectbox("Choose the app mode", options)
    logger.info(f"App mode selected: {app_mode}")

    # Add slider to configure the temperature
    temperature = st.sidebar.slider(
        "Select Temperature (for creativity)",
        min_value=0.0, max_value=1.0, value=0.7, step=0.1,
        help="Controls the creativity/randomness of the response (higher = more random, lower = more focused)"
    )
    logger.info(f"Temperature set to: {temperature}")

    # Dropdown to choose model
    model = st.sidebar.selectbox(
        "Select OpenAI Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"],
        help="Determines the version of GPT you're using (e.g., gpt-3.5-turbo, gpt-4) "
             "with varying capabilities and token limits."
    )
    logger.info(f"Model selected: {model}")

    # Sidebar configuration for max tokens
    max_tokens = st.sidebar.slider("Set max tokens",
                                   min_value=50, max_value=20000, value=50,
                                   help="Represents the units of text processed (input + output), "
                                        "impacting the cost and response length.")
    logger.info(f"Max tokens set to: {max_tokens}")

    # Initialize OpenAI client with selected model and temperature
    client = OpenAIGeniusClient(api_key, model, temperature, max_tokens)
    logger.info("OpenAI client initialized.")

    # Load appropriate app based on mode
    if app_mode == "Chat":
        logger.info("Launching Chat mode.")
        chat_app(client)
    elif app_mode == "Text Translator":
        logger.info("Launching Text Translator mode.")
        text_translator_ui(client)
    elif app_mode == "Prompt Engineering Assistant":
        logger.info("Launching Prompt Generator mode.")
        prompt_generator_ui(client)
    else:
        logger.warning(f"Unknown app mode selected: {app_mode}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("An error occurred while running the application.")
