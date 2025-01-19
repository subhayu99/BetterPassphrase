# BetterPassphrase

**BetterPassphrase** is a Python library and CLI tool for generating _somewhat_ secure, meaningful passphrases. It uses various parts of speech to construct grammatically correct and easy-to-remember phrases.

---

## Features

- **Customizable Length**: Generate passphrases with a specified number of words.
- **Custom Separators**: Use any character as a separator between words.
- **Capitalization Options**: Choose whether to capitalize the words in the passphrase.
- **Probability Calculation**: Get the uniqueness probability of the generated passphrase.
- **Verbose Output**: Optionally display detailed information about the generation process.
- **CLI Support**: Generate passphrases directly from the command line.

---

## Installation

Install the package via [PyPI](https://pypi.org/project/BetterPassphrase):

```bash
pip install BetterPassphrase
```

---

## Usage

### Library Usage

Use the library in your Python code to generate passphrases programmatically:

```python
from betterpassphrase.generator import generate_phrase

# Generate a passphrase
phrase = generate_phrase(length=6, sep="-", capitalize=True)

print(f"Generated passphrase: {phrase.passphrase}")
print(f"Word count: {phrase.word_count}")
print(f"Probability: {1 / phrase.one_of:.2e}")
```

### CLI Usage

After installing the package, you can use the `betterpassphrase` command directly from your terminal:

```bash
betterpassphrase --length 6 --sep "" --capitalize --verbose
```

#### Options

| Option            | Short Flag | Description                                   | Default         |
|-------------------|------------|-----------------------------------------------|-----------------|
| `--length`        | `-l`       | Number of words in the passphrase             | `6`             |
| `--sep`           | `-s`       | Separator to use between words                | `-`             |
| `--capitalize`    | `-c`       | Capitalize the words (true/false)             | `False`         |
| `--output`        | `-o`       | Save passphrase to a file                     | None            |
| `--verbose`       | `-v`       | Print verbose information (true/false)        | `False`         |

#### Example CLI Output

```bash
$ betterpassphrase --length 8 --sep "-"
Generated phrase: the-actor-and-the-subtle-dancer-played-wonderfully
Word count:       8
```

To generate a passphrase with capitalization and a custom separator:

```bash
$ betterpassphrase --length 8 --sep "" --capitalize
Generated phrase: TheActorAndTheSubtleDancerPlayedWonderfully
Word count:       8
```

To write the passphrase to a file:

```bash
$ betterpassphrase --length 8 --sep "-" --output passphrase.txt
Generated phrase: the-actor-and-the-subtle-dancer-played-wonderfully
Word count:       8

$ cat passphrase.txt
the-actor-and-the-subtle-dancer-played-wonderfully
```

Verbose mode can provide additional details:

```bash
$ betterpassphrase --length 6 --verbose
Generated phrase: the-actor-and-the-subtle-dancer-played-wonderfully
Word count:       8
Probability:      3.733316339298084e-18
Parts of speech:  DETERMINER, SUBJECT_NOUN, CONJUNCTION, DETERMINER, ADJECTIVE, OBJECT_NOUN, VERB, ADVERB
```

---

## Development

### Setting Up for Local Development

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/BetterPassphrase.git
    cd BetterPassphrase
    ```

2. Install the package locally in editable mode:

    ```bash
    pip install -e .
    ```

3. Run tests:

    ```bash
    pytest
    ```

---

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.

---

## Author

[Subhayu Kumar Bala](https://github.com/subhayu99)

---

## Acknowledgments

- Inspired by the concept of secure passphrases for authentication.
- Built with Python's `secrets` and `random` libraries for randomness and security.
