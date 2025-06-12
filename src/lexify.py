import csv
import os

from pathlib import Path

# Output file (.csv) headers.
HEADER = [
    "Q. Body",
    "Q. Clarifier",
    "Q. Footnote",
    "A. Body",
    "A. Clarifier",
    "A. Footnote",
]

DEFAULT_INPUT_FILENAME = "input.txt"
DEFAULT_OUTPUT_FILENAME = "output.txt"
DEFAULT_MODE = "0"


def print_init():
    """Prints initial screen."""
    print(r" _               _  __       ")
    print(r"| |             (_)/ _|      ")
    print(r"| |     _____  ___| |_ _   _ ")
    print(r"| |    / _ \ \/ / |  _| | | |")
    print(r"| |___|  __/>  <| | | | |_| |")
    print(r"\_____/\___/_/\_\_|_|  \__, |")
    print(r"                        __/ |")
    print(r"                       |___/ ")


def ask_args():
    """Asks the user (interactively) which arguments to use."""

    # Creates the args dictionary.
    args = dict()

    # Asks for input file name.
    print(f'⚡ Input file name (leave blank for default "{DEFAULT_INPUT_FILENAME}"):', end=" ")
    if (input_filename := input()) == "":
        input_filename = DEFAULT_INPUT_FILENAME

    # Checks if a file with the specified name exists.
    file_path = Path(input_filename)
    if not file_path.exists():
        print("❌ ERROR. Selected input file does not exist. Aborting...")
        raise ValueError()

    # Asks for output file name.
    print(
        f'⚡ Output file name (⚠️ Existing files with the same name will be overwritten ⚠️) (leave blank for default "{DEFAULT_OUTPUT_FILENAME}"):',
        end=" ",
    )
    if (output_filename := input()) == "":
        output_filename = DEFAULT_OUTPUT_FILENAME

    # Asks for lexify's execution mode.
    print(f'❓ Execution mode [0 for definitions, 1 for families] (leave blank for default "{DEFAULT_MODE}"):', end=" ")
    if (mode := input()) == "":
        mode = DEFAULT_MODE

    if mode != "0" and mode != "1":
        print("❌ ERROR. The specified mode does not exist. Aborting...")
        raise ValueError()

    # Inserts all arguments inside the dictionary.
    args["input"] = input_filename
    args["output"] = output_filename
    args["mode"] = mode

    return args


def init_file(filename):
    """Creates and initialises the output file with the appropriate headers.

    Args:
        filename (string): Output file name.
    """

    # Creates a new file with the specified name.
    f = open(filename, "w", encoding="UTF8", newline="")

    # Includes the appropriate headers.
    writer = csv.writer(f)
    writer.writerow(HEADER)

    f.close()


def main():
    """Main funtion to initialise lexify tool."""

    # Prints initial screen.
    print_init()

    # Asks the user for execution arguments.
    try:
        args = ask_args()
    except:
        return

    # Runs the appropriate methods depending on the selected mode.
    if args["mode"] == "0":
        print("DEFINITIONS MODE SELECTED")
        # TODO  call definitions mode methods
    elif args["mode"] == "1":
        print("FAMILIES MODE SELECTED")
        # TODO  call families mode methods
    else:
        print("NO VALID MODE SELECTED")


if __name__ == "__main__":
    main()
