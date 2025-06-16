from .common import FULL_TYPE_LIST

# Ignores TqdmExperimentalWarning
import warnings
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


class InputFileParsingError(Exception):
    """Exception that represents an error while trying to parse input file."""

    pass


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
            raise InputFileParsingError(f'Word type "{abbreviation}" is not known.')


def is_balanced(string):
    """Returns if the parenthesis of a string are balanced.
    It also checks that no other words or letters are written between two well-closed parenthesis.

    Args:
        string (string): String whose parenthesis are checked.
    """
    stack = 0
    # Used when first parenthesis is encountered, so no words can be between two well-closed parenthesis.
    first_parens = False

    for s in string:
        if s == "(":
            first_parens = True
            stack += 1
        elif s == ")":
            stack -= 1

            if stack < 0:
                raise InputFileParsingError("Parenthesis are not balanced.")

        # Checks that there are no words between well-closed parenthesis.
        elif stack <= 0 and first_parens == True:
            raise InputFileParsingError("No words or letters can be between two well-closed parenthesis.")

    if stack != 0:
        raise InputFileParsingError("Parenthesis are not balanced.")


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
        raise InputFileParsingError("Empty lines are not allowed.")

    # Checks that line parenthesis are balanced.
    is_balanced(line)

    # Checks that a word exists before the first parenthesis occurrence.
    if line[0] == "(":
        raise InputFileParsingError("A dictionary item must be specified before the first parenthesis.")

    # Retrieves the actual word.
    if (index := line.find("(")) != -1:
        word = line[0:index]
    else:
        word = line

    return word


def read_words(input):
    """Reads words from input file and store the desired word types inside a dictionary.

    Args:
        input (string): Input file name.

    Return:
        words (dict): Dictionary containing parsed words.
    """

    # Initialises the dictionary.
    words = {}

    # Opens the input file and starts reading it.
    file = open(input, "r")
    raw_data = file.read()

    # Puts all data into a list, separated by linebreaks.
    lines = raw_data.split("\n")
    lines.pop(-1)

    print()

    for line in tqdm(lines, desc="🐙 Parsing input file..."):
        # Initialises a list of word types for each word.
        types = []
        aux_line = line

        # Makes all checks about the input line.
        try:
            current_word = check_input_line(line)
        except InputFileParsingError as e:
            raise InputFileParsingError(f"Error in line #{lines.index(line) + 1} of input file -> {str(e)}")

        # Retrieves desired word types.
        # Continues till there are no more parenthesis left.
        while "(" in aux_line and ")" in aux_line:
            word_type_abb = aux_line[aux_line.index("(") + 1 : aux_line.index(")")]

            # Erases the current word type from the input file.
            aux_line = aux_line.replace(f"({word_type_abb})", "")

            # Checks that the word type selected is not duplicated.
            if "(" + word_type_abb + ")" in aux_line:
                raise InputFileParsingError(
                    f'Error in line #{lines.index(line) + 1} of input file -> The word type "{word_type_abb}" is duplicated.'
                )

            # If word type abbreviation is not known, exits the program.
            try:
                tt = abbtotype(word_type_abb)
            except InputFileParsingError as e:
                raise InputFileParsingError(f"Error in line #{lines.index(line) + 1} of input file -> {str(e)}")

            types.append(tt)

        # If no word type is specified, all word types are introduced.
        if len(types) == 0:
            types = FULL_TYPE_LIST

        # Saves specified word types into the dictionary.
        words[current_word] = types

    file.close()

    return words
