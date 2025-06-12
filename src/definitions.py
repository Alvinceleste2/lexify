import csv
import os
import subprocess
import time

# Default name for auxiliary parse file.
DEFAULT_PARSE_FILENAME = "aux.txt"

# Full list of possible word types.
FULL_TYPE_LIST = [
    " idiom",
    " collocation",
    " phrase",
    " verb",
    " noun",
    " adjective",
    " adverb",
]


def abbtotype(abbreviation):
    """Transforms word type abbreviations into full word type names.

    Args:
        abbreviation (string): Word type abbreviation.

    Returns:
        Full word type name associated to the abbreviation.
    """
    match (abbreviation):
        case "n":
            return " noun"
        case "v":
            return " verb"
        case "adj":
            return " adjective"
        case "adv":
            return " adverb"
        case "id":
            return " idiom"
        case "col":
            return " collocation"
        case "ph":
            return " phrase"
        case _:
            # If word type abbreviation is not known, raises an exception.
            raise KeyError()


def is_balanced(string):
    """Returns if the parenthesis of a string are balanced.
    It also checks that no other words or letters are written between two well-closed parenthesis.

    Args:
        string (string): String whose parenthesis are checked.
    """
    stack = 0
    # Used when first parenthesis is encountered, so no words can be between outside two well-closed parenthesis.
    first_parens = False

    for s in string:
        if s == "(":
            first_parens = True
            stack += 1
        elif s == ")":
            stack -= 1

            if stack < 0:
                return False

        # Checks that there are no words between well-closed parenthesis.
        elif stack <= 0 and first_parens == True:
            return False

    if stack != 0:
        return False

    return True


def check_input_line(line):
    """Checks if parenthesis are balanced.
    Checks that no other words are written between parenthesis.
    Retrieves the word before the first parenthesis. Checks if that exists.
    Checks that line is not empty.

    Args:
        line (string): One line from input file.

    Returns:
        Returns
    """

    # Checks that line is not empty
    if len(line) == 0:
        raise ValueError()

    # Checks that line parenthesis are balanced.
    if not is_balanced(line):
        raise ValueError()

    # Checks that a word exists before the first parenthesis occurrence.
    if line[0] == "(":
        raise ValueError()

    # Retrieves the actual word.
    if (index := s.find("(")) != -1:
        word == line[0 : index - 1]
    else:
        word = line


def read_words(input):
    """Reads words from input file and store the desired word types inside a dictionary.

    Args:
        input (string): Input file name.
    """
    global words

    # Opens the input file and starts reading it.
    file = open(input, "r")
    raw_data = file.read()

    # Puts all data into a list, separated by linebreaks.
    data_list = raw_data.split("\n")
    data_list.pop(-1)

    for d in data_list:
        # Initialises a list of word types for each word.
        types = []

        if not balanced_parens():
            pass

        # Continues till there are no more parenthesis left.
        while "(" in d and ")" in d:
            word_type_abb = d[d.index("(") + 1 : d.index(")")]

            # Erases the current word type from the input file.
            d = d.replace(f"({word_type_abb})", "")

            # If word type abbreviation is not known, exits the program.
            try:
                tt = abbtotype(word_type_abb)
            except:
                print(
                    f'❌ There was an error while parsing the input file: word type "{word_type_abb}" for word "{d}" is not know.'
                )

            if tt is not None:
                types.append(tt)

            # If no word type is specified, all word types are introduced.
            if len(types) == 0:
                types = FULL_TYPE_LIST

            # Saves specified word types into the dictionary.
            words[d] = types

    file.close()


def definitions_flow(args):
    global words, no_def

    words = dict()
    not_found, no_def = [], []

    read_words(args["input"])
    print(words)
