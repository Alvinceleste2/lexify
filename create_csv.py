import csv
import os
import sys
import argparse

DEFAULT_PARSE_FILENAME = "aux.txt"
HEADER = [
    "Q. Body",
    "Q. Clarifier",
    "Q. Footnote",
    "A. Body",
    "A. Clarifier",
    "A. Footnote",
]
WORD_TYPES = [
    "noun",
    "verb",
    "adjective",
    "adverb",
]


def transform_type(string):
    if string == "n":
        return " noun"
    elif string == "v":
        return " verb"
    elif string == "adj":
        return " adjective"
    elif string == "adv":
        return " adv"
    else:
        return None


def initFile(filename):
    f = open(filename, "w", encoding="UTF8", newline="")
    writer = csv.writer(f)
    writer.writerow(HEADER)
    f.close()


def readWords(words_file):
    global words
    file = open(words_file, "r")

    data = file.read()

    data_into_list = data.split("\n")
    data_into_list.pop(-1)
    for d in data_into_list:
        types = []
        while "(" in d and ")" in d:
            word_type = d[d.index("(") + 1 : d.index(")")]
            d = d.replace(f"({word_type})", "")
            types.append(transform_type(word_type))
        words[d] = types
    file.close()


def createDefStrings(data):
    string = ""
    i = 1
    for d in data:
        string += f"**{i}. {d}**\n"
        for e in data[d]:
            string += f'* *"{e}"*\n'
        string += "\n"
        i += 1

    return string


def writeFile(word, word_type, pronuntiation, data):
    global filename
    f = open(filename, "a", encoding="UTF8", newline="")
    writer = csv.writer(f)
    writer.writerow([word, pronuntiation, word_type, createDefStrings(data)])
    f.close()


# returns 0 on success, -1 if camb did not work properly, -2 if the word could be found but did not match any word types selected
def parseFile(word):
    global filename, words

    f = open(DEFAULT_PARSE_FILENAME, "r", newline="")
    # If len(empty) != 1 means that the answer has not been properly extracted
    if len(f.readline()) != 1:
        return -1

    stored_flag = False

    line = ""
    word_split = word.split(" ")
    word_split.pop(-1)

    # Searches word entries until EOF
    # It must be a definition for the possible word types specified in the dictionary
    while len(line := f.readline()) != 0:
        # Definition -> list of examples dictionary
        data = dict()
        current_pronuntiation = ""
        current_type = ""
        current_word = ""

        for t in words[word]:
            if t in line:
                current_type = t
                break

        if current_type == "":
            continue

        # Searches the start of a possible definition
        if all([x for x in word_split if x in line]) and current_type in line:
            current_word = line.split(current_type, 1)[0]
            current_pronuntiation = f.readline()
            line = f.readline()
            current_definition = ""
            while len(line) > 1 and (line[0] == ":" or line[0] == "|"):
                if line[0] == ":":
                    current_definition = line[2:-1]
                    data[current_definition] = []
                else:
                    data[current_definition].append(line[1:-1])

                line = f.readline()

            writeFile(
                f"**{current_word}**", current_type, current_pronuntiation[0:-1], data
            )
            stored_flag = True

    f.close()

    if stored_flag:
        return 0
    else:
        return -2


def main():
    global filename, words, no_def

    parser = create_parser()
    args = parser.parse_args()

    filename = args.csvfile

    not_found = []
    no_def = []
    words = dict()
    initFile(args.csvfile)
    readWords(args.wfile)
    print(words)

    for w in words:
        print(f"{w}...")
        os.system(f"camb -n {w} | ansi2txt > aux.txt")
        res = parseFile(w)
        if res == -1:
            not_found.append(w)
        elif res == -2:
            no_def.append(w)

    os.system("rm aux.txt")

    print("\n")

    if len(not_found) == 0 and len(no_def) == 0:
        print("Every word has been given an appropiate meaning")
    else:
        if len(not_found) != 0:
            print(f"There have been {len(not_found)} word(s) which could not be found:")
            print(not_found)
            print("\n")
        if len(no_def) != 0:
            print(
                f"There have been {len(no_def)} word(s) whose definitions were found, but none of them have been saved due to filters:"
            )
            print(no_def)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A tool to automate the creation of word definition flashcards in Brainscape.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--wfile",
        dest="wfile",
        type=str,
        help="Input .txt filename",
        default="words.txt",
    )
    parser.add_argument(
        "--csvfile",
        dest="csvfile",
        type=str,
        help="Output .csv filename",
        default="cards.csv",
    )

    return parser


if __name__ == "__main__":
    main()
