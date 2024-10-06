import logging
import streamlit as st

from src.services.joke_service import Joker
from src.services.openai_client import OpenAIGeniusClient

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def tell_joke_ui(client: OpenAIGeniusClient):
    st.title("Tell me a joke")

    # Initialize the joke service once
    if 'joke_service' not in st.session_state:
        st.session_state.joke_service = Joker(client)

    joke_service = st.session_state.joke_service
    joke = st.session_state.get('joke', '')

    st.write("Click the button below to get a random joke:")

    # Button to fetch a new joke
    if st.button("Tell me a joke"):
        joke = joke_service.tell_joke()
        st.session_state.joke = joke  # Save joke to session state
        st.write(joke)

    # Check if a joke exists before allowing the generation of explanation
    if joke:
        if st.button("Explain the joke"):
            logger.info("Explain the joke button clicked.")
            with st.spinner("Generating explanation..."):
                try:
                    generated_prompt, tokens_used = joke_service.execute(joke)
                    st.text_area("Joke Explanation", generated_prompt, height=300)
                    st.caption(f"Tokens used: {tokens_used}")
                except Exception as e:
                    logger.error(f"Error during joke explanation: {str(e)}", exc_info=True)
                    st.error("Failed to generate an explanation. Please try again.")
    else:
        st.warning("Please have a joke first!")
