import streamlit as st
import logging
from src.services.openai_client import OpenAIGeniusClient
from src.services.prompt_generator_service import PromptGenerator

# Initialize logger
logger = logging.getLogger(__name__)

def prompt_generator_ui(client: OpenAIGeniusClient):
    """Streamlit UI for prompt generation using the OpenAI API."""
    st.title("Prompt Engineering Assistant")
    logger.info("Prompt Engineering Assistant UI initialized.")

    # User input: Context
    context = st.text_area("Context", height=30)
    if context:
        logger.info(f"User input - Context: {context[:50]}...")  # Log truncated input

    # Tone options with descriptions
    tone_options = {
        "Technical": "Detailed and specific, with a focus on precision and clarity.",
        "Technical but simple": "Accurate but simplified for easier understanding.",
        "Formal": "Polished and professional tone, ideal for official communication.",
        "Casual": "Friendly and informal, suitable for everyday communication.",
        "Creative": "Imaginative and expressive, suited for artistic or inventive content.",
        "Conversational": "Friendly and engaging, suitable for dialogue-based responses.",
        "Instructive": "Focused on giving clear, step-by-step instructions.",
        "Persuasive": "Geared toward convincing or influencing the reader.",
        "Empathetic": "Compassionate and sensitive to emotional needs.",
        "Neutral": "Unbiased and impartial in tone.",
        "Authoritative": "Confident and assertive, often used in expert communication.",
        "Humorous": "Light-hearted and funny.",
        "Analytical": "Detailed, logical, and data-driven.",
        "Sarcastic": "Witty with a biting or ironic tone.",
        "Optimistic": "Positive and forward-looking.",
        "Pessimistic": "Cautious or focusing on potential negatives.",
        "Other": "Customize your tone or select if the above options don't fit."
    }

    # User input: Tone selection
    tone_selected = st.radio(
        "Select the Tone/Style:",
        options=list(tone_options.keys()),
        format_func=lambda x: f"{x} - {tone_options[x]}"
    )
    logger.info(f"User input - Tone selected: {tone_selected}")

    # User input: Constraints
    constraints = st.text_area("Constraints", height=30)
    if constraints:
        logger.info(f"User input - Constraints: {constraints[:50]}...")

    # Generate prompt button
    if st.button("Generate Prompt"):
        logger.info("Generate Prompt button clicked.")
        with st.spinner("Generating prompt..."):
            prompt_gen = PromptGenerator(context, tone_selected, constraints)
            try:
                # Execute prompt generation
                logger.info("Calling OpenAI API for prompt generation.")
                generated_prompt, tokens_used = prompt_gen.execute(client)
                logger.info("Prompt generated successfully.")

                # Display generated prompt
                st.text_area("Generated Prompt", generated_prompt, height=500)
                st.caption(f"Tokens used: {tokens_used}")
                logger.info(f"Generated Prompt: {generated_prompt[:50]}... (truncated)")
                logger.info(f"Tokens used: {tokens_used}")
            except Exception as e:
                logger.error(f"Error during prompt generation: {str(e)}", exc_info=True)
                st.error(f"Error during prompt generation: {str(e)}")
