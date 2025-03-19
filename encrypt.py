import random
import string
from dotenv import load_dotenv

load_dotenv()
RANDOM_SEED = os.environ.get("RANDOM_SEED")

def encrypt(text: str) -> str:
    """
    Given a text string, swaps each letter using a randomly generated mapping.
    Non-letter characters (such as punctuation, spaces, and numbers) remain unchanged.
    """
    random.seed(RANDOM_SEED)
    # Create a list of all letters: lowercase and uppercase
    letters = list(string.ascii_lowercase + string.ascii_uppercase)
    
    # Create a shuffled copy to form a random mapping
    shuffled_letters = letters.copy()
    random.shuffle(shuffled_letters)
    
    # Build the mapping: each original letter maps to a randomly chosen letter
    mapping = dict(zip(letters, shuffled_letters))
    
    # Transform the text by swapping the letters
    result = [mapping.get(char, char) for char in text]
    return ''.join(result)
