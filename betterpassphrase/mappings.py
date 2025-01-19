from .models import P


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

UNIT_PHRASE_MIN_LENGTH = UNIT_PHRASE_LENGTHS[0]
"""Minimum length allowed to generate an unit passphrase."""

UNIT_PHRASE_MAX_LENGTH = UNIT_PHRASE_LENGTHS[-1]
"""Maximum length allowed to generate an unit passphrase."""
