from functools import reduce
from pathlib import Path
import random
import re

import pytest

from betterpassphrase.cli import main as betterpassphrase_cli
from betterpassphrase.config import BUFFER
from betterpassphrase.generator import (
    generate_phrase,
    PartsOfSpeech,
    UNIT_PHRASE_LENGTHS,
    UNIT_PHRASE_MIN_LENGTH,
    UNIT_PHRASE_MAX_LENGTH,
)


extract_capitals = lambda text: re.findall(r"[A-Z][a-z]+", text)

def test_basic_phrase_generation():
    phrase = generate_phrase(length=6, sep=" ")
    assert isinstance(phrase.passphrase, str)
    assert len(phrase.passphrase.split(" ")) == 6
    assert phrase.word_count == 6


def test_basic_phrase_generation():
    phrase = generate_phrase(length=6, sep=" ", capitalize=True)
    assert isinstance(phrase.passphrase, str)
    assert len(extract_capitals(phrase.passphrase)) == 6
    assert phrase.word_count == 6


def test_phrase_with_separator():
    phrase = generate_phrase(length=4, sep="-")
    assert "-" in phrase.passphrase
    assert len(phrase.passphrase.split("-")) == 4


def test_phrase_capitalization():
    phrase = generate_phrase(length=3, capitalize=True)
    assert all(word[0].isupper() for word in phrase.passphrase.split())

    phrase_lower = generate_phrase(length=3, capitalize=False)
    assert all(word[0].islower() for word in phrase_lower.passphrase.split())


def test_invalid_length():
    with pytest.raises(ValueError, match="Cannot generate phrase of length"):
        generate_phrase(
            length=-2
        )


def test_minimum_length():
    phrase = generate_phrase(length=UNIT_PHRASE_MIN_LENGTH, sep=" ")
    assert len(phrase.passphrase.split(" ")) == UNIT_PHRASE_MIN_LENGTH


def test_maximum_length():
    phrase = generate_phrase(length=UNIT_PHRASE_MAX_LENGTH, sep=" ")
    assert len(phrase.passphrase.split(" ")) == UNIT_PHRASE_MAX_LENGTH


def test_one_of_calculation():
    length = random.choice(UNIT_PHRASE_LENGTHS)
    phrase = generate_phrase(length=length)
    one_of_calculated = reduce(
        lambda x, y: x * y,
        [pos.n for pos in phrase.combination],
        1,
    )
    assert isinstance(phrase.one_of, int)
    assert phrase.one_of > 0  # `one_of` must be positive
    assert phrase.one_of == one_of_calculated


def test_parts_of_speech_loading():
    for part in PartsOfSpeech:
        words = part.words
        assert isinstance(words, list)
        assert all(isinstance(word, str) for word in words)
        assert len(words) > 0  # Ensure words are loaded


def test_random_word_selection():
    for part in PartsOfSpeech:
        word = part.word
        assert isinstance(word, str)
        assert word in part.words


def test_get_words():
    for part in PartsOfSpeech:
        words = part.get_words(n=5)
        assert len(words) == 5
        assert all(word in part.words for word in words)

def test_cli_integration():
    min_length = UNIT_PHRASE_MAX_LENGTH + BUFFER
    max_length = min_length + BUFFER
    temp_file = Path(".temp.txt")
    command_args_str = f"-l {min_length} -s - -c true -o {temp_file}"
    betterpassphrase_cli(command_args_str.split(" "))
    result = temp_file.read_text()
    assert temp_file.exists()
    assert min_length <= len(result.strip().split("-")) <= max_length
    assert min_length <= len(extract_capitals(result)) <= max_length
    temp_file.unlink()
