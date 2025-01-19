import secrets
from pathlib import Path


BUFFER = 3
"""
Buffer to add to the length of the passphrase.

This when added to length defines the maximum length of the passphrase.
"""

assert BUFFER >= 3, "Buffer must be at least 3 as the program might go into an infinite loop."

PARTS_OF_SPEECH_DIR = Path(__file__).parent / "parts_of_speech"
"""Path to the directory containing the parts of speech files."""

SEED: int | None = None
"""Seed for the random number generator."""

try:
    RANDOM_SELECTOR = secrets.SystemRandom(SEED).choice
except:
    RANDOM_SELECTOR = secrets.choice
