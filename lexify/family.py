import os
import spacy
from collections import defaultdict

FAMILIES_TXT_DATABASE = "families.txt"

DEFAULT_PARSE_FILENAME = "aux.txt"
DEFAULT_WORD_TYPE_FILENAME = "type.txt"

FULL_TYPE_LIST = [
    " idiom",
    " collocation",
    " phrase",
    " verb",
    " noun",
    " adjective",
    " adverb",
]


def read_words(words_file):
    global words
    file = open(words_file, "r")

    data = file.read()

    data_into_list = data.split("\n")
    data_into_list.pop(-1)

    words = data_into_list

    file.close()


# def parse_file(word, filename):


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
            f"pcregrep -M '(?s)(^{w}\n\t{w}.*?)(?=^(?!\t))' families.txt > {DEFAULT_PARSE_FILENAME}"
        )
        res = parse_file(w, args.csvfile)

        if res == -1:
            no_res.append(w)

    os.system(f"rm {DEFAULT_PARSE_FILENAME}")
    os.system(f"rm {DEFAULT_WORD_TYPE_FILENAME}")
    print_summary()
