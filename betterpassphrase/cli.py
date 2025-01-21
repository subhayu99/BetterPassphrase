import argparse

from betterpassphrase.models import Passphrase
from betterpassphrase.utils import run_parallel_exec_but_return_in_order
from .generator import generate_phrase


def main(_args: list[str] = None):
    parser = argparse.ArgumentParser(
        description="Generate a phrase based on the specified options."
    )

    # -l flag for phrase length
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=6,
        help="Number of words in the phrase (default: 6).",
    )

    # -s flag for separator
    parser.add_argument(
        "-s",
        "--sep",
        type=str,
        default="-",
        help="Separator between words (default: no separator).",
    )

    # -c flag for capitalization (True by default)
    parser.add_argument(
        "-c",
        "--capitalize",
        action="store_true",
        help="Capitalize the phrase (default: True).",
    )

    # -o flag for output file
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="",
        help="File to write the phrase to (default: print to stdout).",
    )
    
    # -r flag for generating multiple phrases
    parser.add_argument(
        "-n",
        "--num-phrases",
        type=int,
        default=1,
        help="Number of phrases to generate (default: 1).",
    )

    # -v flag for verbosity level
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Verbosity level: 0 for passphrase only, 1 for basic info, 2 for detailed info (default: 1).",
    )

    args = parser.parse_args(_args)

    capitalize = args.capitalize

    if args.num_phrases >= 1:
        phrases: list[Passphrase] = run_parallel_exec_but_return_in_order(
            generate_phrase,
            [args.length] * args.num_phrases, 
            args.sep, 
            capitalize, 
        )
    else:
        print("Invalid number of phrases to generate.")
        exit(1)

    for i, phrase in enumerate(phrases):
        if args.output:
            _mode = "w" if i == 0 else "a"
            with open(args.output, _mode) as f:
                f.write(f"{phrase.passphrase}\n")

        pos_sep = ", "
        phrase_sep = "\n                        "

        if args.verbosity == 0:
            # Only the passphrase
            print(phrase.passphrase)
        elif args.verbosity == 1:
            # Basic info
            print()
            print(f"Generated phrase: {phrase.passphrase}")
            print(f"Word count:       {phrase.word_count}")
        elif args.verbosity == 2:
            # Detailed info
            print()
            print(f"Generated phrase:       {phrase.passphrase}")
            print(f"Word count:             {phrase.word_count}")
            print(f"Wordlist Probability:   {phrase.wordlist_probability:.2e}")
            print(f"Character Probability:  {phrase.character_probability:.2e}")
            print(f"Parts of speech:        {phrase_sep.join(pos_sep.join(pos.name.lower() for pos in phrase) for phrase in phrase.sub_combinations)}\n")


if __name__ == "__main__":
    main()
