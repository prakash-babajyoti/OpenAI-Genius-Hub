import yaml
import os


def load_yaml(file_path: str) -> dict:
    """
    Loads prompts from the given YAML file.

    Args:
        file_path (str): The path to the YAML file containing the prompts.

    Returns:
        dict: A dictionary of prompts.

    Raises:
        FileNotFoundError: If the YAML file cannot be found.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompts file not found: {file_path}")

    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")
