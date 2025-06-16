import os
import csv
import time
import subprocess
from collections import defaultdict

from .common import FULL_TYPE_LIST

# Ignores TqdmExperimentalWarning
import warnings
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

# Default name for auxiliary parse file.
AUX_FILENAME = "aux.txt"

# Number of attempt while executing camb tool.
NUM_RETRIES = 4


def camb_output_ok():
    """Returns if a camb execution output is valid or not.

    Returns:
        True if the camb output is valid, False if not.
    """
    f = open(AUX_FILENAME, "r", newline="")

    # If len() of first line is lower than 2 camb has not worked properly.
    return not len(line := f.readline()) > 2


def exec_camb(word):
    """Executes camb program over the received word. Stores the result inside an aux file.
    It also checks if the output is ok, retrying if not.

    Args:
        word (string): Word whose definitions will be looked for.

    Returns:
        True if camb output is ok, False if not.
    """
    # Searches for definitions at least three times.
    for tries in range(NUM_RETRIES, -1, -1):
        try:
            # Run the command  TODO  possibly changing this to "poetry run camb..."
            subprocess.run(
                f"camb -n {word} | ansi2txt > {AUX_FILENAME}",
                shell=True,
                check=True,
            )
        except KeyboardInterrupt:
            print("Process interrupted by user (Ctrl+C)")
            exit(-1)

        # If camb output is ok, the program can continue. If not, camb execution is retried after waiting some time.
        if camb_output_ok():
            return True
        else:
            time.sleep(0.1)

    return False


def create_def_string(data):
    """Formats a definition string for one word.

    Args:
        data (dict): Dictionary containing the word definitions and examples.

    Returns:
        Return the formated string.
    """
    string = ""
    i = 1
    for d in data:
        string += f"**{i}. {d}**\n"
        for e in data[d]:
            string += f'* *"{e}"*\n'
        string += "\n"
        i += 1

    return string


def write_definition(filename, word, word_type, pronuntiation, data):
    """Writes a word definition and examples into the output file.

    Args:
        filename (string): Output file name.
        word (string): Current word.
        word_type (string): current word type.
        pronuntiation (string): Pronuntiation for the word.
        data (dict): Dictionary of definitions and examples.
    """
    # Opens the output file.
    f = open(filename, "a", encoding="UTF8", newline="")
    writer = csv.writer(f)

    # Writes the data into the output file.
    writer.writerow([word, pronuntiation, word_type, create_def_string(data)])
    f.close()


def parse_camb_file(filename, words, word):
    """Parses the camb tool output file for a word to find definitions, examples, etc.

    Args:
        words (dict): Dictionary of the words whose definitions need to be parsed.
        word (string): Word whose definitions are being searched.

    Returns:
        List of word types that are not compatible with the specified word.
        If this list is empty, that means that all specified word types were stored.
    """

    # Opens the camb output file in read mode and "removes" the first line of it.
    f = open(AUX_FILENAME, "r", newline="")
    line = f.readline()

    # In case the word is a phrase, splits the phrase in all its subwords.
    word_split = word.split(" ")
    word_split.pop(-1)

    # Initialises a dictionary that keeps track of the number of definitions that have been stored for each word type.
    stored_dict = defaultdict(int)

    # Searches the word entries until EOF.
    while (len(line := f.readline())) != 0:
        # If line starts with a space no definition is there.
        if line[0] == " ":
            continue

        # If a definition is found, creates a dictionary where to store all examples and other things.
        data = dict()

        # Some various initializations.
        current_type = ""
        current_word = ""
        current_definition = ""
        current_pronuntiation = ""

        # For each type of word requested, finds out if the current definition matches that type of word.
        for t in words[word]:
            # If word type is in line, the definition could be of that type.
            if t in line:
                # Ensures the definition is indeed of the selected word type.
                fi = line.find(t)

                # Checks if there are no more word types behind the selected.
                if all(e not in line[0:fi] for e in FULL_TYPE_LIST):
                    current_type = t
                    break

        # If current_type is empty means that no definition has been found that matches filters.
        if current_type == "":
            continue

        # Checks that all subwords in the current word is in the output file line.
        if all(x in line for x in word_split):

            # Gets current_word from dictionary definition and jumps to the next line.
            current_word = line.split(current_type, 1)[0]
            line = f.readline()

            # TODO  investigate about the inclusion of this line.
            if "HTML5" in line:
                continue

            # Stores the word pronuntiation in case it exists.
            if "uk " in line or " us " in line or "|" in line:
                current_pronuntiation = line
                line = f.readline()
            else:
                current_pronuntiation = " "

            # Retrieves all definitions and examples asociated to that word type.
            # Checks that the length of the line is greater than 1 and that the characters ":" or "|" are in the line.
            while len(line) > 1 and (line[0] == ":" or line[0] == "|"):
                # If the first character is ":", there is a word definition. If not, it is an example.
                if line[0] == ":":
                    current_definition = line[2:-1]
                    data[current_definition] = []
                else:
                    data[current_definition].append(line[1:-1])

                # Jumps to the next line.
                line = f.readline()

            # Once the definition is fully parsed, writes the data to the output file.
            write_definition(filename, f"**{current_word}**", current_type, current_pronuntiation[0:-1], data)

            # Adds one to the stored_flag.
            stored_dict[current_type] += 1

    f.close()

    no_def = []

    # Checks that definitions for all word types have been stored. If not, then the specified type of word for this current word does not exist.

    if words[word] == FULL_TYPE_LIST:
        return []

    for wt in words[word]:
        if stored_dict[wt] == 0:
            no_def.append(wt)

    return no_def


def search_definitions(filename, words):
    """Searches definitions for the received words and stores them into the output file.

    Args:
        words (dict): Dictionary containing the input file parsed words.

    Returns:
        Both not_found and no_def lists of words.
    """

    # Initialises not_found list of words that have not been found and no_def list of words whose definitions have been found but some of them were not stored.
    not_found, no_def = [], []

    # Iterates through the list of words to find definitions.
    for w in tqdm(words, desc="🧪 Searching definitions..."):
        # If camb output is not ok though all the attempts, the program assumes the word does not exists in cambridge dictionary.
        if not exec_camb(w):
            not_found.append(w)
            continue
        # If camb output is ok, the program continues.
        else:
            # Now, camb parsing function can return True if all definitions were stored, or False if some of them were not stored due to filters.
            ret_list = parse_camb_file(filename, words, w)
            if len(ret_list) != 0:
                d = dict()
                d[w] = ret_list
                no_def.append(d)
                continue

    # Removes the aux file from system.
    os.system(f"rm {AUX_FILENAME}")

    # Returns both not_found and no_def lists of words.
    return not_found, no_def
