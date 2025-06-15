import os
import subprocess

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
        print(f"Attempt number {abs(5 - tries)}")
        try:
            # Run the command  TODO  possibly changing this to "poetry run camb..."
            subprocess.run(
                f"camb -n {w} | ansi2txt > {AUX_FILENAME}",
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


def parse_camb_file(word):
    """Parses the camb tool output file for a word to find definitions, examples, etc.

    Args:
        word (string): Word whose definitions are being searched.
    """

    f = open(AUX_FILENAME, "r", newline="")

    pass


def search_definitions(words):
    """Searches definitions for the received words and stores them into the output file.

    Args:
        words (dict): Dictionary containing the input file parsed words.
    """

    # Initialises not_found list of words that have not been found and no_def list of words whose definitions have been found but some of them were not stored.
    not_found, no_def = []

    # Iterates through the list of words to find definitions.
    for w in words:
        # If camb output is not ok though all the attempts, the program assumes the word does not exists in cambridge dictionary.
        # If camb output is ok, the program continues.
        if not exec_camb(w):
            not_found.append(w)
            continue
        else:
            pass

    os.system(f"rm {AUX_FILENAME}")
    pass
