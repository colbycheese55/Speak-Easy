from perspective import Client, Attributes, utils
import os
from dotenv import load_dotenv
load_dotenv()

# Load your API key from an environment variable
API_KEY = os.environ.get("GOOGLE_CLOUD_API_KEY")

# Initialize the Perspective API client
client = Client(token=API_KEY)

def analyze_text(text, attributes):
    """
    Analyze the given text for the specified attributes using the Perspective API.

    Parameters:
    text (str): The text to be analyzed.
    attributes (list): A list of attributes to analyze the text for.

    Returns:
    dict: The response from the Perspective API as a dictionary.
    """
    response = client.analyze(text=text, attributes=attributes)
    return response

# You can also include the utility function for formatting if needed
def format_response(response, align_right=False):
    """
    Format the response from the Perspective API.

    Parameters:
    response (dict): The response dictionary from the Perspective API.
    align_right (bool): Whether to align the text to the right.

    Returns:
    str: The formatted response.
    """
    return utils.format_response(response, align_right=align_right)