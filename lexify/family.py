import os

FAMILIES_TXT_DATABASE = "families.txt"

DEFAULT_PARSE_FILENAME = "aux.txt"


def read_words(words_file):
    global words
    file = open(words_file, "r")

    data = file.read()

    data_into_list = data.split("\n")
    data_into_list.pop(-1)

    words = data_into_list

    file.close()


def parse_file(filename):
    print("TODO")


def print_summary():
    print("TODO")


def family_flow(args):
    global words, no_res

    words, no_res = [], []

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
    print_summary(no_res)
