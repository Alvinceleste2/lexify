import subprocess

FAMILIES_TXT_DATABASE = "sources/families_db.txt"

AUX_FILENAME = "aux.txt"
PRON_FILENAME = "pron.txt"
DEF_FILENAME = "def.txt"


def grep_output_ok():
    """Checks if the grep command output is ok and therefore the word was found inside the database.

    Returns:
        True if the grep command output is valid, False if not.
    """

    f = open(AUX_FILENAME, "r", newline="")

    # If len() of first line is lower than 2, grep did not return any matches.
    res = not len(line := f.readline()) < 2
    f.close()

    return res


def exec_grep(filename, word):
    """Runs the pcregrep command to search for words in the database.

    Args:
        filename (string): Output file name.
        word (string): Word whose families are being looked for.

    Returns:
        True if the word could be found in database, False if not.
    """
    # Runs the command
    try:
        subprocess.run(
            f"pcregrep -M '(?s)(^{word}\n\t{word}.*?)(?=^(?!\t))' sources/families_db.txt > {AUX_FILENAME}",
            shell=True,
            check=True,
        )
    except KeyboardInterrupt:
        print("Process interrupted by user (Ctrl+C)")
        exit(-1)

    # If grep output is ok (this meaning that the word could be found in the database), the program can continue. If not, the method returns false.
    if grep_output_ok():
        return True
    else:
        return False


def get_word_types(line):
    """Parses one line of the grep output and retrieves the associated word types.

    Args:
        line (string): Line of the file.

    Returns:
        Returns the types that appear in the line between parenthesis and the result line, which contains the word itself.
    """
    line = line[1 : len(line) - 1]

    types = []

    while "(" in line and ")" in line:
        word_type = line[line.index("(") + 1 : line.index(")")]
        line = line.replace(f"({word_type})", "")
        if word_type != "":
            types.append(word_type)

    return types, line


def get_pronuntiation(word):
    """Retrieves the pronuntiation for a specified word.

    Args:
        word (string): Word whose pronuntiation is being searched.

    Returns:
        Returns the pronuntiation of the word or empty string in case or error.
    """
    for tries in range(3, -1, -1):
        os.system(f"camb -n {word} | ansi2txt > {PRON_FILENAME}")

        f = open(PRON_FILENAME, "r")

        if len(line := f.readline()) > 2:
            time.sleep(0.05)
            continue
        else:
            line = f.readline()
            line = f.readline()

            return line[0 : len(line) - 1]

    return ""


def write_file(filename, word, origin_types, word_type, pronuntiation, data):
    f = open(filename, "a", encoding="UTF8", newline="")
    writer = csv.writer(f)

    origin_tt = ""
    for o in origin_types:
        origin_tt += o + ", "

    origin_tt = origin_tt[0 : len(origin_tt) - 2]

    writer.writerow(
        [
            word,
            pronuntiation,
            f"{origin_tt} ~> **{word_type}**",
            create_form_string(data),
            "",
            "",
        ]
    )

    f.close()


def parse_grep_file(filename, words, word):
    """Parses the grep command output file for a word to find its families.

    Args:
        filename (string): Output file name.
        words (dict): Dictionary of the words whose families need to be stored.
        word (string): Word whose families are being searched.

    Returns:
        List of words that were not stored due to filters if everything went ok, False if not.
    """

    # List that holds the word types that have not been stored due to filters.
    filter_flag = []

    # Opens the grep output file in read mode.
    f = open(AUX_FILENAME, "r", newline="")

    # Reads the first line and identifies all word types for all possible families.
    line = f.readline()
    origin_types, _ = get_word_types(line)

    # Initialises the data dictionary, where all parsed data will be stored.
    data = defaultdict(list)

    while len(line := f.readline()) != 0:
        types, form = get_word_types(line)

        # For each of the parsed word types, checks that the type has also been requested by user.
        for t in types:
            if t in words[word]:
                data[t].append(form)
            else:
                filter_flag.append(t)

    # Retrieves the pronuntiation for words.
    if len(data.keys()) > 0:
        for tt in data.keys():
            # If pronuntiation is not obtained, the method returns False.
            if (pron := get_pronuntiation(word)) == "":
                return False

            write_file(filename, f"**{word}**", origin_types, tt, pron, data[tt])

    return filter_flag


def search_families(filename, words):
    """Searches families for parsed words and stores them into the output file.

    Args:
        filename (string): Output file name.
        words (dict): List of parsed words and the desired word types for each one.
    Returns:
        Both not_found and no_res lists of words.
    """

    # Initialises not_found list of words that have not been found and no_res list of words whose families have been found but some of them were not stored.
    not_found, no_res, not_in_dict = [], [], []

    # Iterates through the list of words to find families.
    for w in tqdm(words, desc="🍐 Searching families..."):
        # Executes the grep routine to search the word in the database.
        # If grep output is empty, the word could not be obtained from the database.
        if not exec_grep(filename, w):
            not_found.append(w)
            continue
        # If grep output is ok, the program continues.
        else:
            # Now, grep parsing function can return True if all definitions were stored, or False if some of them could not be stored due to filters.
            ret_list = parse_grep_file(filename, words, w)
