"""
The main module for the betterpassphrase package.

Contains the following submodules:
- `generator`: Contains the `generate_phrase` function and the `Passphrase` class.
- `config`: Contains the `PARTS_OF_SPEECH_DIR` constant, which is the path to the directory containing the parts of speech files.
"""
from .generator import generate_phrase, Passphrase
from .config import PARTS_OF_SPEECH_DIR

__all__ = ["generate_phrase", "Passphrase", "PARTS_OF_SPEECH_DIR"]
