import pyjokes
import logging
from typing import Tuple
from src.services.base_operation import OpenAIOperation

# Initialize logger
logger = logging.getLogger(__name__)

class Joker(OpenAIOperation):
    """
    A class that implements the OpenAIOperation interface to handle joke explanations
    using the OpenAI client. It fetches and explains jokes via OpenAI.
    """

    def __init__(self, client):
        """
        Initialize Joker with the OpenAI client.
        """
        self.client = client

    def execute(self, joke: str) -> Tuple[str, int]:
        """
        Explains the joke using the OpenAI API.

        Args:
            joke (str): The joke to be explained.

        Returns:
            Tuple[str, int]: The explanation and the number of tokens used.
        """
        system_msg = f"As an expert in computer science, explain this joke: {joke}"

        try:
            logger.info(f"Requesting joke explanation from OpenAI: '{joke}'")
            new_joke, tokens_used = self.client.call_openai_api(system_msg, joke)
            logger.info(f"Joke explained successfully. Tokens used: {tokens_used}")
            return new_joke, tokens_used
        except Exception as e:
            logger.error(f"Error during joke explanation: {e}", exc_info=True)
            raise RuntimeError(f"Failed to explain the joke: {joke}") from e

    def tell_joke(self) -> str:
        """
        Fetches a random joke from the pyjokes library.

        Returns:
            str: The fetched joke.
        """
        joke = pyjokes.get_joke()
        logger.info(f"Fetched joke: '{joke}'")
        return joke
