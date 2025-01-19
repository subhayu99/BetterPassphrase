import argparse
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

    # -v flag for verbose output (False by default)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose information (default: False).",
    )

    args = parser.parse_args(_args)

    capitalize = args.capitalize

    phrase = generate_phrase(length=args.length, sep=args.sep, capitalize=capitalize)

    if args.output:
        with open(args.output, "w") as f:
            f.write(phrase.passphrase)

    pos_sep = ", "
    phrase_sep = "\n                        "

    print()
    print(f"Generated phrase:       {phrase}")
    print(f"Word count:             {phrase.word_count}")
    if args.verbose:
        print(f"Wordlist Probability:   {phrase.wordlist_probability:.2e}")
        print(f"Character Probability:  {phrase.character_probability:.2e}")
        print(f"Parts of speech:        {phrase_sep.join(pos_sep.join(pos.name for pos in phrase) for phrase in phrase.sub_combinations)}\n")


if __name__ == "__main__":
    main()
