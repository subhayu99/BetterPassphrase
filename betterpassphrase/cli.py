import argparse
from .generator import generate_phrase

def main(_args: list[str] = None):
    parser = argparse.ArgumentParser(description="Generate a phrase based on the specified options.")
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=6,
        help="Number of words in the phrase (default: 6).",
    )
    parser.add_argument(
        "-s",
        "--sep",
        type=str,
        default="",
        help="Separator to use between words in the phrase (default: no separator).",
    )
    parser.add_argument(
        "-c",
        "--capitalize",
        type=lambda x: x.lower() in {"true", "1", "yes"},
        default=True,
        help="Whether to capitalize the phrase (default: True).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="",
        help="File to write the generated phrase to (default: just print to stdout).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=lambda x: x.lower() in {"true", "1", "yes"},
        default=False,
        help="Whether to print verbose information (default: False).",
    )

    args = parser.parse_args(_args)

    phrase = generate_phrase(length=args.length, sep=args.sep, capitalize=args.capitalize)

    if args.output:
        with open(args.output, "w") as f:
            f.write(phrase.passphrase)
    
    pos_sep = ', '
    phrase_sep = '\n                  '
    
    print()
    print(f"Generated phrase: {phrase}")
    print(f"Word count:       {phrase.word_count}")
    if args.verbose:
        print(f"Probability:      {phrase.probability}")
        print(f"Parts of speech:  {phrase_sep.join(pos_sep.join(pos.name for pos in phrase) for phrase in phrase.sub_combinations)}")
    print()

if __name__ == "__main__":
    main()
