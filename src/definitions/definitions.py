import csv
import os
import subprocess

from .read_words import read_words, InputFileParsingError
from .search_definitions import search_definitions

## Basic definitions flow is:
# 1. Read words from input file
# 2. Look for definitions for those parsed words.
# 3. Print summary of execution.


def print_summary(not_found, no_def):
    """Prints a summary of execution.

    Args:
        not_found (list): List of words whose definitions could not be found in the dictionary.
        no_def (list): List of words for which any definition was stored due to filters.
    """
    print()

    if len(not_found) == 0 and len(no_def) == 0:
        print("✅ Every word has been given an appropiate meaning")
    else:
        if len(not_found) != 0:
            print(f"❌ There have been {len(not_found)} word(s) which could not be found:")
            print(not_found)
            print()
        if len(no_def) != 0:
            print(
                f"🟨 There have been {len(no_def)} word(s) whose definitions were found, but some of them have not been saved due to filters:"
            )
            print(no_def)


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
        return

    print()

    # Searches definitions for every parsed word and prints an execution summary.
    not_found, no_def = search_definitions(args["output"], words)
    print_summary(not_found, no_def)
