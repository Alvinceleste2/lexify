import csv
import os
import subprocess

from .read_words import read_words, InputFileParsingError

## Basic definitions flow is:
# 1. Read words from input file
# 2. Look for definitions for those parsed words.
# 3. Finish execution informing the user.


def definitions_flow(args):
    """Definitions mode main method.

    Args:
        args (dict): Dictionary with parsed arguments.
    """
    not_found, no_def = [], []

    try:
        words = read_words(args["input"])
    except InputFileParsingError as e:
        print(f"❌ There was an error while parsing the input file -> {str(e)}")

    print("✅ Input has been correctly parsed.")
