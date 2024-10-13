import csv
import os

DEFAULT_PARSE_FILENAME = "aux.txt"
HEADER = [
    "Q. Body",
    "Q. Clarifier",
    "Q. Footnote",
    "A. Body",
    "A. Clarifier",
    "A. Footnote",
]


def readWords(words_file):
    file = open(words_file, "r")

    data = file.read()

    data_into_list = data.split("\n")
    data_into_list.pop(-1)
    file.close()

    return data_into_list


def initFile(filename):
    f = open(filename, "w", encoding="UTF8", newline="")
    writer = csv.writer(f)
    writer.writerow(HEADER)
    f.close()


def writeFile(filename, word, clarifier, pron, defin, ex):
    f = open(filename, "a", encoding="UTF8", newline="")
    writer = csv.writer(f)
    writer.writerow([word, clarifier[0:-1], pron[0:-1], defin[1:-1], ex, ""])
    f.close()


def parseFile():
    global filename

    f = open(DEFAULT_PARSE_FILENAME, "r", newline="")
    empty = f.readline()
    if len(empty) != 1:
        return -1

    word = f.readline()
    word_list = word.split(" ", 1)
    clarifier = word_list[1]
    word = "**" + word_list[0] + "**"

    pron = f.readline()
    defin = f.readline()
    ex = f.readline()

    writeFile(
        filename,
        word,
        pron,
        clarifier,
        defin,
        '*"' + ex[1:-1] + '"*' if ex[0] == "|" else "",
    )

    f.close()


def main(words_file, fl):
    global filename, not_found
    filename = fl
    not_found = []
    initFile(filename)
    words = readWords(words_file)
    print(words)

    for w in words:
        print(w)
        os.system(f"camb -n {w} | ansi2txt > aux.txt")
        if parseFile() == -1:
            not_found.append(w)

    os.system("rm aux.txt")

    f = open(filename)
    rows = len(f.readlines()) - 1
    if len(words) == rows:
        print("Every word has been given an appropiate meaning")
    else:
        print(f"There have been {len(words) - rows} words which could not be found:")
        print(not_found)

    f.close()


if __name__ == "__main__":
    main("words.txt", "example.csv")
