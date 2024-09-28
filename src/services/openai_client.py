import logging
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt
from typing import List, Tuple


def _create_messages(system_msg: str, user_msg: str) -> List[dict]:
    """
    Helper function to format messages for the OpenAI API.

    Args:
        system_msg (str): The system role's instruction message.
        user_msg (str): The user's input message.

    Returns:
        list: Formatted list of message dictionaries.
    """
    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ]


class OpenAIGeniusClient:
    """
    A client to interact with OpenAI's API to perform various tasks such as code translation,
    sentiment analysis, text rephrasing, and more.

    Attributes:
        api_key (str): The API key used to authenticate with OpenAI.
        model (str): The OpenAI model to be used for generating responses.
        temperature (float): The temperature to control the randomness of the model's output.
        max_tokens (int): The maximum number of tokens for the completion.
    """

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        """
        Initializes the OpenAIGeniusClient with the given API key, model, temperature, and max_tokens.
        """
        if not api_key:
            raise ValueError("API key is required")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Initialize the logger
        self.logger = logging.getLogger(__name__)

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def get_chat_completion(self, messages: List[dict], temperature: float = None, max_tokens: int = None) -> Tuple[
        str, int]:
        """
        Fetches chat completion results from OpenAI's API.

        Args:
            messages (list): A list of formatted message dictionaries.
            temperature (float, optional): Temperature for controlling randomness. Defaults to class setting.
            max_tokens (int, optional): Maximum tokens for the completion. Defaults to class setting.

        Returns:
            tuple: The generated content and the number of tokens used.
        """
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens

        try:
            self.logger.info(f"Sending request to OpenAI API with messages: {messages}")
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            self.logger.info(f"Received response from OpenAI API. Total tokens used: {completion.usage.total_tokens}")
            return completion.choices[0].message.content, completion.usage.total_tokens
        except Exception as e:
            self.logger.error(f"Error during chat completion: {e}", exc_info=True)
            return f"An error occurred: {e}", 0

    def call_openai_api(self, system_msg: str, user_msg: str) -> Tuple[str, int]:
        """
        Helper function to structure messages and call OpenAI's API.

        Args:
            system_msg (str): The system's instruction message.
            user_msg (str): The user's input message.

        Returns:
            tuple: The generated content and the number of tokens used.
        """
        self.logger.info(
            f"Preparing to call OpenAI API with system message: '{system_msg[:50]}...' and user message: '{user_msg[:50]}...'")

        # Format the messages to send to the OpenAI API
        messages = _create_messages(system_msg, user_msg)

        # Call the OpenAI API to get the completion
        return self.get_chat_completion(messages)
