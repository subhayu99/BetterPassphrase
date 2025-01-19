from functools import reduce

from .config import BUFFER, RANDOM_SELECTOR
from .models import P, Passphrase
from .mappings import (
    UNIT_PHRASE_LENGTHS,
    UNIT_PHRASE_MAX_LENGTH,
    LENGTH_TO_WORD_COMBINATIONS_MAP,
)


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


def generate_phrase(
    length: int = 6, sep: str = "", capitalize: bool = True
) -> Passphrase:
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
        words: list[str] = []
        sub_combinations: list[list[P]] = []

        # Generate a list of sub-phrase lengths
        lengths = generate_lengths(length, buffer=BUFFER)
        total_length = (
            sum(lengths)        # Total number of words in the sub-phrases
            + len(lengths) - 1  # Number of conjunctions
        )

        for index, curr_length in enumerate(lengths):
            # Generate a sub-phrase of the current length and add it to the list
            passphrase = generate_phrase(curr_length, sep, capitalize)
            words.extend(passphrase.words)
            sub_combinations.append(passphrase.combination)

            if index == len(lengths) - 1:
                continue

            # Get the conjunction word and capitalize it if necessary
            conjunction = (
                P.CONJUNCTION.word.capitalize() if capitalize else P.CONJUNCTION.word
            )
            words.append(conjunction)
            sub_combinations.append([P.CONJUNCTION])

        # Join the generated phrases with the separator and return the result
        return Passphrase(
            words=words, 
            word_count=total_length, 
            separator=sep,
            capitalize=capitalize,
            sub_combinations=sub_combinations,
        )

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

    # Return the generated passphrase with its metadata
    return Passphrase(
        words=words, 
        word_count=length, 
        separator=sep,
        capitalize=capitalize,
        sub_combinations=[combination],
    )
