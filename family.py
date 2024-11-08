import os
import csv
from collections import defaultdict

FAMILIES_TXT_DATABASE = "sources/families_db.txt"

DEFAULT_PARSE_FILENAME = "aux.txt"
DEFAULT_PRON_FILENAME = "pron.txt"

FULL_TYPE_LIST = [
    "idiom",
    "collocation",
    "phrase",
    "verb",
    "noun",
    "adjective",
    "adverb",
]


def read_words(words_file):
    global words
    file = open(words_file, "r")

    data = file.read()

    data_into_list = data.split("\n")
    data_into_list.pop(-1)

    words = data_into_list

    file.close()


def parse_word_types(line):
    line = line[1 : len(line) - 1]

    types = []

    while "(" in line and ")" in line:
        word_type = line[line.index("(") + 1 : line.index(")")]
        line = line.replace(f"({word_type})", "")
        if word_type != "":
            types.append(word_type)

    return types, line


def get_pronuntiation(word):
    os.system(f"camb -n {word} | ansi2txt > {DEFAULT_PRON_FILENAME}")

    f = open(DEFAULT_PRON_FILENAME, "r")

    line = f.readline()
    line = f.readline()
    line = f.readline()
    return line[0 : len(line) - 1]


def create_form_string(data):
    string = ""
    for d in data:
        string += f"* {d}\n"

    return string


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
            f"{origin_tt} ~~> **{word_type}**",
            create_form_string(data),
            "",
            "",
        ]
    )

    f.close()


def parse_file(word, filename):
    f = open(DEFAULT_PARSE_FILENAME, "r", newline="")
    # If len(empty) != 1 means that the answer has not been properly extracted
    if len(line := f.readline()) < 2:
        return -1

    line = f.readline()
    origin_types, _ = parse_word_types(line)
    data = defaultdict(list)

    while len(line := f.readline()) != 0:
        types, form = parse_word_types(line)

        for t in types:
            data[t].append(form)

    if len(data.keys()) > 0:
        for tt in data.keys():
            write_file(
                filename,
                f"**{word}**",
                origin_types,
                tt,
                get_pronuntiation(word),
                data[tt],
            )


def print_summary():
    global no_res
    print()

    if len(no_res) == 0:
        print("✅Every word has been given a family")
    else:
        print(
            f"🟨There have been {len(no_res)} word(s) whose families could not be found"
        )
        print(no_res)


def family_flow(args):
    global words, no_res
    words = []
    no_res = []

    read_words(args.wfile)
    print(words)

    for w in words:
        print(f"{w}...")
        os.system(
            f"pcregrep -M '(?s)(^{w}\n\t{w}.*?)(?=^(?!\t))' sources/families_db.txt > {DEFAULT_PARSE_FILENAME}"
        )
        res = parse_file(w, args.csvfile)

        if res == -1:
            no_res.append(w)

    os.system(f"rm {DEFAULT_PARSE_FILENAME}")
    os.system(f"rm {DEFAULT_PRON_FILENAME}")
    print_summary()
