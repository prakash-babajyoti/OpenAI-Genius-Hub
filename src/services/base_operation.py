from typing import Tuple


class OpenAIOperation:
    """
    Abstract base class for operations using the OpenAI client.
    Each specific operation must implement this interface.
    """

    def execute(self, client, *args, **kwargs) -> Tuple[str, int]:
        """
        Executes the OpenAI operation.

        Args:
            client: The OpenAI client instance used to perform the operation.
            *args: Additional arguments for the operation.
            **kwargs: Additional keyword arguments for the operation.

        Returns:
            Tuple[str, int]: The result of the operation and the token usage.
        """
        raise NotImplementedError("Each operation must implement the `execute` method.")
