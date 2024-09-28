import logging
from typing import Tuple
from src.services.base_operation import OpenAIOperation
from src.utils.load_yaml import load_yaml

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PromptGenerator(OpenAIOperation):
    """
    A class responsible for generating prompts by interacting with the OpenAI API.
    It formats user inputs into a prompt request and sends it to the API.
    """

    def __init__(self, context: str, tone_selected: str, constraints: str):
        """
        Initializes the PromptGenerator with the necessary user inputs.

        Args:
            context (str): The context or background for the prompt.
            tone_selected (str): The tone or style for the generated response.
            constraints (str): Any specific limitations or instructions.
        """
        self.context = context
        self.tone_selected = tone_selected
        self.constraints = constraints
        logger.info("PromptGenerator initialized with context, tone, and constraints.")

    def execute(self, client) -> Tuple[str, int]:
        """
        Executes the prompt generation process by calling the OpenAI API.

        Args:
            client: The OpenAI API client.

        Returns:
            Tuple[str, int]: The generated prompt and the number of tokens used.
        """
        self._validate_input()
        logger.info("Input validated successfully.")

        # Load the system prompt template
        prompts = load_yaml('src/prompts/prompt_generator.yml')
        system_msg = prompts.get('SYSTEM_PROMPT_ENGINEER')
        logger.info("Prompt template loaded from configuration.")

        # Generate the user message based on the inputs
        user_msg = self._create_user_message()
        logger.info("User message created.")

        # Call the OpenAI API to generate the prompt
        logger.info("Calling OpenAI API...")
        try:
            result = client.call_openai_api(system_msg, user_msg)
            logger.info("OpenAI API call successful.")
            return result
        except Exception as e:
            logger.error(f"Error during OpenAI API call: {str(e)}", exc_info=True)
            raise

    def _validate_input(self):
        """
        Validates that all required inputs are provided.

        Raises:
            ValueError: If any required fields (context, tone, constraints) are missing.
        """
        if not all([self.context, self.tone_selected, self.constraints]):
            logger.error("Validation failed: Missing required fields.")
            raise ValueError("Context, tone, and constraints are required fields.")
        logger.info("All inputs are valid.")

    def _create_user_message(self) -> str:
        """
        Constructs the user message using the provided context, tone, and constraints.

        Returns:
            str: The formatted user message for the OpenAI API.
        """
        user_message = (
            f"You are tasked with creating a response based on the following details:\n"
            f"**Context**: {self.context}\n"
            f"**Tone/Style**: {self.tone_selected}\n"
            f"**Constraints**: {self.constraints}\n"
            f"Please ensure that the response adheres to the provided instructions and is structured accordingly."
        )
        logger.info("User message constructed.")
        return user_message
