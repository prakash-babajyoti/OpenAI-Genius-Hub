import streamlit as st
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def chat_app(client):
    """
    A Streamlit-based chat interface to interact with the OpenAI API.

    Args:
        client: The OpenAIGeniusClient instance used to handle communication with OpenAI's API.
    """
    st.header("Chat with AI", anchor=False)
    logger.info("Chat interface loaded.")

    # Initialize session state for messages if not already set
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.info("Session state for messages initialized.")

    # Display chat messages from the session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        logger.info(f"Displayed {message['role']} message: {message['content']}")

    # Handle user input and interaction
    if prompt := st.chat_input("Ask something..."):
        logger.info(f"User input received: {prompt}")

        # Store user message in session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        logger.info("User message stored in session state.")

        # Display the user message in the chat
        with st.chat_message("user"):
            st.markdown(prompt)
            logger.info("User message displayed in chat.")

        # Display assistant response (OpenAI)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Placeholder for AI response
            try:
                # Get AI's response from the OpenAI client
                full_response, tokens_used = client.get_chat_completion(st.session_state.messages)
                message_placeholder.markdown(full_response)  # Display the AI response
                st.caption(f"Tokens used: {tokens_used}")  # Display token usage
                logger.info(f"AI response received: {full_response}, Tokens used: {tokens_used}")
            except Exception as e:
                # Handle API call errors gracefully
                st.error(f"Error while communicating with OpenAI: {e}")
                full_response = "Error: Unable to fetch response"
                logger.error(f"Error while communicating with OpenAI: {e}")

        # Append AI's response to the session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        logger.info("AI response stored in session state.")

