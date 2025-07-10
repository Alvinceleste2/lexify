from common.read_words import read_words, InputFileParsingError


def print_summary(not_found, no_def):
    """Prints a summary of execution.

    Args:
        not_found (list): List of words whose families could not be found in the dictionary.
        no_def (list): List of words for which any related word was stored due to filters.
    """
    print()

    if len(not_found) == 0 and len(no_def) == 0:
        print("✅ Every word has been given an appropriate family.")
    else:
        if len(not_found) != 0:
            print(f"❌ ERROR! There have been {len(not_found)} word(s) which could not be found:")
            print(not_found)
            print()
        if len(no_def) != 0:
            print(
                f"🟨 WARNING! There have been {len(no_def)} word(s) whose specified target word types do not exist. Please, review the input file. Here is the full list:"
            )
            print(no_def)


def family_flow(args):
    """Families mode main method.

    Args:
        args (dict): Dictionary with parsed arguments.
    """
    not_found, no_res = [], []

    try:
        words = read_words(args["input"])
    except InputFileParsingError as e:
        print(f"❌ There was an error while parsing the input file -> {str(e)}")
        return

    print()

    # Searches families for every parsed word and prints an execution summary.
    not_found, no_def = search_families(args["output"], words)
    print_summary(not_found, no_def)
