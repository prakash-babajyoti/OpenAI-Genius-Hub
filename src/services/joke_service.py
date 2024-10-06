import pyjokes
import logging
from typing import Tuple
from src.services.base_operation import OpenAIOperation
from src.utils.load_yaml import load_yaml

# Initialize logger
logger = logging.getLogger(__name__)

class Joker(OpenAIOperation):
    """
    A class that implements the OpenAIOperation interface to handle joke explanation
    using the OpenAI client. It fetches a joke and explains it using OpenAI.
    """

    def __init__(self, client):
        """
        Initialize Joker with OpenAI client and load the YAML prompts.
        """
        self.client = client


    def execute(self, joke: str) -> Tuple[str, int]:
        """
        Executes the joke explanation by making a call to the OpenAI API.

        Args:
            joke (str): The joke to be explained.

        Returns:
            Tuple[str, int]: Explained joke and tokens used.
        """
        logger.info("Executing joke explanation.")
        system_msg = f"As an expert in computer science explain this joke: {joke}"

        try:
            logger.info(f"Making OpenAI API request with joke: '{joke}' and system message: '{system_msg}'")
            new_joke, tokens_used = self.client.call_openai_api(system_msg, joke)
            logger.info(f"Joke explained. Tokens used: {tokens_used}")
            return new_joke, tokens_used
        except Exception as e:
            logger.error(f"Error during joke explanation: {e}")
            raise

    def tell_joke(self) -> str:
        """
        Fetches a random joke using pyjokes.

        Returns:
            str: The random joke.
        """
        self.joke = pyjokes.get_joke()
        logger.info(f"Fetched joke: '{self.joke}'")
        return self.joke
