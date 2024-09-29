import logging
from src.services.openai_client import OpenAIGeniusClient


def initialize_openai_client(api_key: str, model: str, temperature: float, max_tokens: int) -> OpenAIGeniusClient:
    """
    Initializes the OpenAI client with the given configuration.

    Args:
        api_key (str): OpenAI API key.
        model (str): Selected model name.
        temperature (float): The temperature setting for creativity.
        max_tokens (int): Maximum token limit.

    Returns:
        OpenAIGeniusClient: Initialized OpenAI client.
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing OpenAI client.")

    client = OpenAIGeniusClient(api_key, model, temperature, max_tokens)
    logger.info("OpenAI client initialized successfully.")
    return client
