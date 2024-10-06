import streamlit as st
import logging


def configure_sidebar():
    """
    Configures the Streamlit sidebar with inputs for API key, app mode, model, and settings.

    Returns:
        dict: A dictionary containing the inputs from the sidebar.
    """
    logger = logging.getLogger(__name__)
    logger.info("Configuring sidebar.")

    # Input for OpenAI API key
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    st.sidebar.markdown("[Get OpenAI API Key](https://platform.openai.com/account/api-keys)")

    # Sidebar navigation for selecting the app mode
    options = ["Chat", "Text Translator", "Prompt Engineering Assistant", "Tell me a joke"]
    app_mode = st.sidebar.selectbox("Choose the app mode", options)

    # Add slider to configure the temperature
    temperature = st.sidebar.slider(
        "Select Temperature (for creativity)", min_value=0.0, max_value=1.0, value=0.7, step=0.1
    )

    # Dropdown to choose model
    model = st.sidebar.selectbox(
        "Select OpenAI Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"]
    )

    # Sidebar configuration for max tokens
    max_tokens = st.sidebar.slider("Set max tokens", min_value=50, max_value=20000, value=50)

    return {
        "api_key": api_key,
        "app_mode": app_mode,
        "temperature": temperature,
        "model": model,
        "max_tokens": max_tokens,
    }
