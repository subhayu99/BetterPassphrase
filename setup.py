from setuptools import setup, find_packages

setup(
    name="BetterPassphrase",
    version="0.1.0",
    description="A Python library to generate secure, meaningful passphrases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Subhayu Kumar Bala",
    author_email="balasubhayu99@gmail.com",
    url="https://github.com/subhayu99/BetterPassphrase",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "betterpassphrase=betterpassphrase.cli:main",
        ],
    },
)
