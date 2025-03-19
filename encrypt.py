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
    letters = list(string.ascii_lowercase + string.ascii_uppercase)
    
    shuffled_letters = letters.copy()
    random.shuffle(shuffled_letters)
    
    mapping = dict(zip(letters, shuffled_letters))
    
    result = [mapping.get(char, char) for char in text]
    return ''.join(result)
