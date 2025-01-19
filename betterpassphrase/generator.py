import random
from enum import Enum
from pathlib import Path
from typing import NamedTuple
from functools import cached_property, reduce

from .config import BUFFER, PARTS_OF_SPEECH_DIR, RANDOM_SELECTOR


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
    
    def get_words(self, n: int = 5) -> list[str]:
        """
        Get a list of `n` random words from the list of words for the given part of speech.

        Args:
            n (int): Number of words to get. Defaults to 5.

        Returns:
            list[str]: List of `n` random words.
        """
        if not self.words:
            return []
        return random.choices(self.words, k=n)
    
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

    passphrase: str
    """The generated passphrase."""

    word_count: int
    """The number of words in the passphrase."""

    one_of: int
    """The probability of the passphrase being generated."""

    sub_combinations: list[list[PartsOfSpeech]]
    """A list of sub-combinations of parts of speech used to generate the passphrase."""

    @property
    def combination(self) -> list[PartsOfSpeech]:
        """The combination of parts of speech used to generate the passphrase."""
        return [
            pos for phrase in self.sub_combinations for pos in phrase
        ]
    
    @property
    def probability(self) -> float:
        """
        The probability of the passphrase being generated.

        Returns:
            float: The probability.
        """
        return 1 / self.one_of

    def __str__(self) -> str:
        """
        The string representation of the passphrase.

        Returns:
            str: The passphrase.
        """
        return self.passphrase


P = PartsOfSpeech
"""
A short alias for the PartsOfSpeech class.
"""


def generate_lengths(length: int = 10, buffer: int = 3) -> list[int]:
    """
    Generate a list of word lengths for a passphrase generator.

    This function creates a list of word lengths that adhere to the constraints of 
    a desired total passphrase length (`length`) and an allowable buffer (`buffer`). 
    Word lengths are chosen from a predefined list (`UNIT_PHRASE_LENGTHS`), with 
    separators of length 1 (representing conjunctions) included between words.

    The algorithm ensures the following:
    - The total length of the passphrase (including separators) is between 
      `length` and `length + buffer`.
    - Word lengths of 1 are not used, except for separators.

    Args:
        length (int): The target length of the passphrase.
        buffer (int): The maximum additional length allowed beyond the target length. 
                      Must be at least 3.

    Returns:
        list[int]: A list of integers representing word lengths for the passphrase. 
                   Separators are not explicitly included in the output.

    Notes:
        - The function ensures that separators of length 1 are used during generation 
          but are removed from the final output list.
        - The function relies on a predefined `UNIT_PHRASE_LENGTHS` list, which should 
          include acceptable word lengths.

    Examples:
        >>> UNIT_PHRASE_LENGTHS = [3, 4, 5, 6, 7, 8]
        >>> generate_lengths(length=10, buffer=3)
        [5, 4]  # Example output, actual values may vary due to randomness.
    """
    lengths = []
    # Ensure a minimum buffer value of 3
    buffer = max(3, buffer)

    # UNIT_PHRASE_LENGTHS should be a predefined list of acceptable word lengths.
    options = UNIT_PHRASE_LENGTHS
    if 1 in options:
        
        # Remove 1 as a valid word length (used only for separators).
        options.remove(1)

    while sum(lengths[:-1]) < length:
        # Calculate the difference between the target length and current sum of lengths
        diff = length - sum(lengths[:-1]) - 1  # -1 for the added separator

        if diff in options:
            # If the difference matches an option, use it as the next word length
            sub_length = diff
        else:
            # Otherwise, choose a random word length from the available options
            sub_length = RANDOM_SELECTOR(options)

        lengths.append(sub_length)

        # Check if the total length exceeds the allowed range
        if sum(lengths) > length + buffer:
            # If the length exceeds, remove the last added word and try again
            lengths = lengths[:-1]
            continue

        # Add a separator (length of 1) after the word length
        lengths.append(1)

    # Remove any standalone separators (lengths of 1) from the final list
    lengths = [x for x in lengths if not x == 1]

    return lengths


def generate_phrase(length: int = 6, sep: str = "", capitalize: bool = True) -> Passphrase:
    """
    Generate a passphrase of the specified length.

    Args:
        length (int): The number of words in the passphrase.
        sep (str): Separator between words.
        capitalize (bool): Whether to capitalize words.

    Returns:
        Passphrase: Generated passphrase with metadata.
    """
    # If length is greater than the maximum length, generate a phrase of the maximum length
    # and then generate a new phrase of the remaining length, joining them with the conjunction.
    if length > UNIT_PHRASE_MAX_LENGTH:
        one_of = 1
        sub_phrases: list[str] = []
        sub_combinations: list[list[PartsOfSpeech]] = []

        # Generate a list of sub-phrase lengths
        lengths = generate_lengths(length, buffer=BUFFER)
        total_length = (
            sum(lengths) # Total number of words in the sub-phrases
            + (len(lengths) - 1) # Number of conjunctions
        )
        
        for index, curr_length in enumerate(lengths):
            # Generate a sub-phrase of the current length and add it to the list
            passphrase = generate_phrase(curr_length, sep, capitalize)
            sub_phrases.append(passphrase.passphrase)
            sub_combinations.append(passphrase.combination)
            one_of *= passphrase.one_of
            
            if index == len(lengths) - 1:
                continue
            
            # Get the conjunction word and capitalize it if necessary
            conjunction = P.CONJUNCTION.word.capitalize() if capitalize else P.CONJUNCTION.word
            sub_phrases.append(conjunction)
            sub_combinations.append([P.CONJUNCTION])

            # Calculate the probability of the generated phrase
            one_of *= P.CONJUNCTION.n
        
        # Join the generated phrases with the separator and return the result
        return Passphrase(sep.join(sub_phrases), total_length, one_of, sub_combinations)

    # If the length is not in the length-to-word-combinations map, raise a ValueError
    if length not in LENGTH_TO_WORD_COMBINATIONS_MAP:
        raise ValueError(f"Cannot generate phrase of length {length}")

    # Choose a random combination of parts of speech for the given length
    combination = RANDOM_SELECTOR(LENGTH_TO_WORD_COMBINATIONS_MAP[length])

    # NOTE: Uncomment this for debugging (will print the selected combination and its index)
    # print(
    #     f"COMBINATION LENGTH:INDEX:[*PARTS] : {length}"
    #     f":{LENGTH_TO_WORD_COMBINATIONS_MAP[length].index(combination)}"
    #     f":[{', '.join([x.name for x in combination])}]"
    # )

    # Generate the words for the combination and capitalize them if necessary
    words = [pos.word for pos in combination]
    if capitalize:
        words = [word.capitalize() for word in words]

    # Calculate the probability of the generated phrase
    one_of = reduce(lambda x, y: x * y, [pos.n for pos in combination])

    # Return the generated passphrase with its metadata
    return Passphrase(sep.join(words), length, one_of, [combination])


LENGTH_TO_WORD_COMBINATIONS_MAP = {
    3: [
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN],      # The Quick Hunter
        [P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN],       # The Quick Wolf
        [P.DETERMINER, P.SUBJECT_NOUN, P.VERB],           # The Hunter Chased
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB],            # The Wolf Chased
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.ADVERB],          # Quick Hunter Eagerly
        [P.ADJECTIVE, P.OBJECT_NOUN, P.ADVERB],           # Quick Wolf Eagerly
        [P.SUBJECT_NOUN, P.VERB, P.ADVERB],               # Hunter Chased Eagerly
        [P.OBJECT_NOUN, P.VERB, P.ADVERB],                # Wolf Chased Eagerly
        [P.VERB, P.DETERMINER, P.OBJECT_NOUN],            # Chased The Wolf
        [P.VERB, P.DETERMINER, P.SUBJECT_NOUN],           # Chased The Hunter
        [P.ADVERB, P.PREPOSITION, P.DETERMINER],          # Eagerly Across The
        [P.PREPOSITION, P.DETERMINER, P.ADJECTIVE],       # Across The Quick
        [P.PREPOSITION, P.DETERMINER, P.SUBJECT_NOUN],    # Across The Hunter
    ],
    4: [
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB],             # The Quick Hunter Chased
        [P.DETERMINER, P.OBJECT_NOUN, P.ADVERB, P.VERB],                 # The Wolf Eagerly Chased
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.ADVERB],                 # Quick Hunter Chased Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.VERB, P.PREPOSITION],           # The Hunter Chased Across
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.ADVERB],                 # The Wolf Chased Eagerly
        [P.SUBJECT_NOUN, P.OBJECT_NOUN, P.VERB, P.ADVERB],               # Hunter Wolf Chased Eagerly
        [P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN],           # Hunter Chased The Wolf
        [P.DETERMINER, P.OBJECT_NOUN, P.CONJUNCTION, P.SUBJECT_NOUN],    # The Wolf And Hunter
        [P.OBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.SUBJECT_NOUN],    # Wolf And The Hunter
        [P.OBJECT_NOUN, P.ADVERB, P.VERB, P.SUBJECT_NOUN],               # Wolf Eagerly Chased Hunter
        [P.SUBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.OBJECT_NOUN],    # Hunter And The Wolf
        [P.DETERMINER, P.SUBJECT_NOUN, P.CONJUNCTION, P.OBJECT_NOUN],    # The Hunter And Wolf
        [P.OBJECT_NOUN, P.VERB, P.DETERMINER, P.SUBJECT_NOUN],           # Wolf Chased The Hunter
        [P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.VERB],              # The Quick Wolf Chased
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.OBJECT_NOUN],            # Quick Hunter Chased Wolf
        [P.DETERMINER, P.SUBJECT_NOUN, P.ADVERB, P.VERB],                # The Hunter Eagerly Chased
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.SUBJECT_NOUN],           # The Wolf Chased Hunter
        [P.OBJECT_NOUN, P.VERB, P.ADVERB, P.PREPOSITION],                # Wolf Chased Eagerly Across
    ],
    5: [
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.ADVERB],                 # The Quick Hunter Chased Eagerly
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.ADJECTIVE, P.SUBJECT_NOUN],            # The Wolf Chased Quick Hunter
        [P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN],            # Hunter Chased The Quick Wolf
        [P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.VERB, P.ADVERB],                  # The Quick Wolf Chased Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN],           # The Hunter Chased The Wolf
        [P.DETERMINER, P.OBJECT_NOUN, P.ADVERB, P.VERB, P.SUBJECT_NOUN],               # The Wolf Eagerly Chased Hunter
        [P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN, P.ADVERB],               # Hunter Chased The Wolf Eagerly
        [P.SUBJECT_NOUN, P.VERB, P.ADJECTIVE, P.OBJECT_NOUN, P.PREPOSITION],           # Hunter Chased Quick Wolf Across
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.CONJUNCTION, P.OBJECT_NOUN],     # The Quick Hunter And Wolf
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.OBJECT_NOUN],     # Quick Hunter And The Wolf
        [P.OBJECT_NOUN, P.VERB, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN],            # Wolf Chased The Quick Hunter
        [P.ADJECTIVE, P.OBJECT_NOUN, P.VERB, P.DETERMINER, P.SUBJECT_NOUN],            # Quick Wolf Chased The Hunter
        [P.DETERMINER, P.SUBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.OBJECT_NOUN],    # The Hunter And The Wolf
        [P.ADVERB, P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.PREPOSITION],                # Eagerly The Wolf Chased Across
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN],            # Quick Hunter Chased The Wolf
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.ADVERB, P.PREPOSITION],                # The Wolf Chased Eagerly Across
        [P.SUBJECT_NOUN, P.VERB, P.ADJECTIVE, P.OBJECT_NOUN, P.ADVERB],                # Hunter Chased Quick Wolf Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.CONJUNCTION, P.ADJECTIVE, P.OBJECT_NOUN],     # The Hunter And Quick Wolf
    ],
    6: [
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN],           # The Quick Hunter Chased The Wolf
        [P.DETERMINER, P.SUBJECT_NOUN, P.ADVERB, P.VERB, P.DETERMINER, P.OBJECT_NOUN],              # The Hunter Eagerly Chased The Wolf
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN, P.ADVERB],               # Quick Hunter Chased The Wolf Eagerly
        [P.DETERMINER, P.OBJECT_NOUN, P.ADVERB, P.VERB, P.DETERMINER, P.SUBJECT_NOUN],              # The Wolf Eagerly Chased The Hunter
        [P.ADVERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB],               # Eagerly Across The Quick Hunter Chased
        [P.DETERMINER, P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN, P.ADVERB],              # The Hunter Chased The Wolf Eagerly
        [P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.VERB, P.ADVERB, P.PREPOSITION],                # The Quick Wolf Chased Eagerly Across
        [P.SUBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.ADVERB],             # Hunter And The Wolf Chased Eagerly
        [P.OBJECT_NOUN, P.VERB, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.ADVERB],               # Wolf Chased The Quick Hunter Eagerly
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.OBJECT_NOUN, P.VERB],          # Quick Hunter And The Wolf Chased
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.OBJECT_NOUN],    # The Quick Hunter And The Wolf
        [P.ADVERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.VERB],                # Eagerly Across The Quick Wolf Chased
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN],           # The Wolf Chased The Quick Hunter
        [P.OBJECT_NOUN, P.VERB, P.ADVERB, P.PREPOSITION, P.DETERMINER, P.SUBJECT_NOUN],             # Wolf Chased Eagerly Across The Hunter
        [P.DETERMINER, P.SUBJECT_NOUN, P.OBJECT_NOUN, P.VERB, P.ADVERB, P.PREPOSITION],             # The Hunter Wolf Chased Eagerly Across
    ],
    7: [
        [P.DETERMINER, P.OBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.SUBJECT_NOUN, P.VERB, P.ADVERB],       # The Wolf And The Hunter Chased Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.OBJECT_NOUN, P.VERB, P.ADJECTIVE, P.CONJUNCTION, P.ADVERB],        # The Hunter Wolf Chased Quick And Eagerly
        [P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN, P.ADJECTIVE, P.CONJUNCTION, P.ADVERB],        # Hunter Chased The Wolf Quick And Eagerly
        [P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.VERB, P.DETERMINER, P.SUBJECT_NOUN, P.ADVERB],         # The Quick Wolf Chased The Hunter Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.ADVERB],         # The Hunter Chased The Quick Wolf Eagerly
        [P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.PREPOSITION, P.DETERMINER, P.OBJECT_NOUN, P.ADVERB],        # Quick Hunter Chased Across The Wolf Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.CONJUNCTION, P.OBJECT_NOUN, P.VERB, P.PREPOSITION, P.ADVERB],      # The Hunter And Wolf Chased Across Eagerly
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.PREPOSITION, P.DETERMINER, P.OBJECT_NOUN, P.VERB],    # The Quick Hunter Across The Wolf Chased
        [P.SUBJECT_NOUN, P.VERB, P.ADVERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN],        # Hunter Chased Eagerly Across The Quick Wolf
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.ADVERB],         # The Wolf Chased The Quick Hunter Eagerly
        [P.OBJECT_NOUN, P.VERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.ADVERB],        # Wolf Chased Across The Quick Hunter Eagerly
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.DETERMINER, P.OBJECT_NOUN, P.ADVERB],         # The Quick Hunter Chased The Wolf Eagerly
        [P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.SUBJECT_NOUN, P.VERB],    # The Quick Wolf And The Hunter Chased
    ],
    8: [
        [P.DETERMINER, P.OBJECT_NOUN, P.ADVERB, P.VERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN],     # The Wolf Eagerly Chased Across The Quick Hunter
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.ADVERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN],     # The Wolf Chased Eagerly Across The Quick Hunter
        [P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.VERB, P.PREPOSITION, P.DETERMINER, P.OBJECT_NOUN, P.ADVERB],     # The Quick Hunter Chased Across The Wolf Eagerly
        [P.DETERMINER, P.OBJECT_NOUN, P.VERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.SUBJECT_NOUN, P.ADVERB],     # The Wolf Chased Across The Quick Hunter Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.VERB, P.PREPOSITION, P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.ADVERB],     # The Hunter Chased Across The Quick Wolf Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.OBJECT_NOUN, P.VERB, P.PREPOSITION, P.ADJECTIVE, P.CONJUNCTION, P.ADVERB],    # The Hunter Wolf Chased Across Quick And Eagerly
        [P.DETERMINER, P.SUBJECT_NOUN, P.CONJUNCTION, P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.VERB, P.ADVERB],     # The Hunter And The Quick Wolf Chased Eagerly
        [P.DETERMINER, P.ADJECTIVE, P.OBJECT_NOUN, P.VERB, P.PREPOSITION, P.DETERMINER, P.SUBJECT_NOUN, P.ADVERB],     # The Quick Wolf Chased Across The Hunter Eagerly
    ],
}
"""
Map of lengths to word combinations.
Here's a better representation:
```yaml
LENGTH_TO_WORD_COMBINATIONS_MAP:
    length1: [
        [option1 for that length1],
        [option2 for that length1],
        ...
    ]
    length2: [
        [option1 for that length2],
        [option2 for that length2],
        ...
    ]
    ...
```
"""
UNIT_PHRASE_LENGTHS = sorted(LENGTH_TO_WORD_COMBINATIONS_MAP)
"""List of lengths that can be used to generate an unit passphrase."""

UNIT_PHRASE_MIN_LENGTH, *_, UNIT_PHRASE_MAX_LENGTH = UNIT_PHRASE_LENGTHS
