import random
from enum import Enum
from pathlib import Path
from typing import NamedTuple
from functools import cached_property, reduce

from .config import RANDOM_SELECTOR, PARTS_OF_SPEECH_DIR


class PartsOfSpeech(str, Enum):
    """
    Enum representing the different parts of speech used in the library.
    """
    ADJECTIVE = "adjectives.txt"
    SUBJECT_NOUN = "sub_nouns.txt"
    VERB = "verbs.txt"
    PREPOSITION = "prepositions.txt"
    DETERMINER = "determiners.txt"
    OBJECT_NOUN = "obj_nouns.txt"
    ADVERB = "adverbs.txt"
    CONJUNCTION = "conjunctions.txt"
    
    @property
    def filepath(self) -> Path:
        """
        The path to the file containing the words for the given part of speech.

        Returns:
            Path: The path to the file.
        """
        return PARTS_OF_SPEECH_DIR / self.value

    @cached_property
    def words(self) -> list[str]:
        """
        List of words for the given part of speech.

        Returns:
            list[str]: List of words.
        """
        wordfile = self.filepath
        if not wordfile.exists():
            return []
        return [
            x.strip()
            for x in wordfile.read_text().splitlines()
        ]
    
    @property
    def word(self) -> str:
        """
        A random word from the list of words for the given part of speech.

        Returns:
            str: A random word.
        """
        if not self.words:
            return ""
        return RANDOM_SELECTOR(self.words)
    
    @property
    def n(self) -> int:
        """
        The number of words in the list of words for the given part of speech.

        Returns:
            int: The number of words.
        """
        return len(self.words)

    def __str__(self) -> str:
        """
        The string representation of the part of speech.

        Returns:
            str: The string representation.
        """
        return self.value
    
    def __repr__(self) -> str:
        """
        The representation of the part of speech.

        Returns:
            str: The representation.
        """
        return self.value


class Passphrase(NamedTuple):
    """A generated passphrase with metadata."""

    words: list[str]
    """The list of words in the passphrase."""

    word_count: int
    """The number of words in the passphrase."""

    separator: str
    """The separator between words in the passphrase."""

    capitalize: bool
    """Whether the words in the passphrase should be capitalized."""

    sub_combinations: list[list[PartsOfSpeech]]
    """A list of sub-combinations of parts of speech used to generate the passphrase."""

    @property
    def passphrase(self) -> str:
        """The generated passphrase."""
        return self.separator.join(self.words)

    @property
    def combination(self) -> list[PartsOfSpeech]:
        """The combination of parts of speech used to generate the passphrase."""
        return [
            pos for phrase in self.sub_combinations for pos in phrase
        ]

    @property
    def one_of(self) -> int:
        """This is one of the different passphrases can be generated using the same set of parts of speech wordlists."""
        return reduce(lambda x, y: x * y, [pos.n for pos in self.combination])

    @property
    def wordlist_probability(self) -> float:
        """The probability of generating the passphrase using the same set of parts of speech wordlists."""
        return 1 / self.one_of

    @property
    def character_probability(self) -> float:
        """The probability of generating the passphrase using alphabetical characters."""
        return 1 / reduce(
            lambda x, y: x * y,
            [
                26 if char.isalpha() else 10 if char.isdigit() else 1
                for char in "".join(self.words)
            ],
        )

    def __str__(self) -> str:
        """The string representation of the passphrase."""
        return self.passphrase


P = PartsOfSpeech
"""
A short alias for the PartsOfSpeech class.
"""
