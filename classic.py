import csv
import os

DEFAULT_PARSE_FILENAME = "aux.txt"

FULL_TYPE_LIST = [
    " idiom",
    " collocation",
    " phrase",
    " verb",
    " noun",
    " adjective",
    " adverb",
]


def transform_type(string):
    if string == "n":
        return " noun"
    elif string == "v":
        return " verb"
    elif string == "adj":
        return " adjective"
    elif string == "adv":
        return " adverb"
    elif string == "id":
        return " idiom"
    elif string == "col":
        return " collocation"
    elif string == "ph":
        return " phrase"
    else:
        return None


def read_words(words_file):
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
            tt = transform_type(word_type)
            if tt is not None:
                types.append(tt)

        if len(types) == 0:
            types = FULL_TYPE_LIST

        words[d] = types
    file.close()


def create_def_string(data):
    string = ""
    i = 1
    for d in data:
        string += f"**{i}. {d}**\n"
        for e in data[d]:
            string += f'* *"{e}"*\n'
        string += "\n"
        i += 1

    return string


def write_file(filename, word, word_type, pronuntiation, data):
    f = open(filename, "a", encoding="UTF8", newline="")
    writer = csv.writer(f)
    writer.writerow([word, pronuntiation, word_type, create_def_string(data)])
    f.close()


# returns 0 on success, -1 if camb did not work properly, -2 if the word could be found but did not match any word types selected
def parse_file(word, filename):
    global words

    f = open(DEFAULT_PARSE_FILENAME, "r", newline="")
    # If len(empty) != 1 means that the answer has not been properly extracted
    if len(line := f.readline()) < 2:
        return -1

    stored_flag = 0

    line = ""
    word_split = word.split(" ")
    word_split.pop(-1)

    # Searches word entries until EOF
    # It must be a definition for the possible word types specified in the dictionary
    while len(line := f.readline()) != 0:
        if line[0] == " ":
            continue

        # Definition -> list of examples dictionary
        data = dict()
        current_pronuntiation = ""
        current_type = ""
        current_word = ""

        for t in words[word]:
            if t in line:

                fi = line.find(t)

                if (
                    all(e not in line[0:fi] for e in FULL_TYPE_LIST)
                    and word in line[0:fi]
                ):
                    current_type = t
                    break

        if current_type == "":
            continue

        # Searches the start of a possible definition
        if (
            all(x in line for x in word_split)
            and current_type in line
            and line[0] != " "
        ):
            current_word = line.split(current_type, 1)[0]
            if (
                current_type != " collocation"
                and current_type != " idiom"
                and current_type != " phrase"
            ):
                current_pronuntiation = f.readline()
            else:
                current_pronuntiation = "‎ "
            line = f.readline()
            current_definition = ""
            while len(line) > 1 and (line[0] == ":" or line[0] == "|"):
                if line[0] == ":":
                    current_definition = line[2:-1]
                    data[current_definition] = []
                else:
                    data[current_definition].append(line[1:-1])

                line = f.readline()

            write_file(
                filename,
                f"**{current_word}**",
                current_type,
                current_pronuntiation[0:-1],
                data,
            )
            stored_flag += 1

    f.close()

    if stored_flag >= len(words[word]) or words[word] == FULL_TYPE_LIST:
        return 0
    else:
        return -2


def print_summary(not_found, no_def):
    print()

    if len(not_found) == 0 and len(no_def) == 0:
        print("✅Every word has been given an appropiate meaning")
    else:
        if len(not_found) != 0:
            print(
                f"❌There have been {len(not_found)} word(s) which could not be found:"
            )
            print(not_found)
            print()
        if len(no_def) != 0:
            print(
                f"🟨There have been {len(no_def)} word(s) whose definitions were found, but some of them have not been saved due to filters:"
            )
            print(no_def)


def classic_flow(args):
    global words, no_def
    words = dict()
    not_found, no_def = [], []

    read_words(args.wfile)
    print(words)

    for w in words:
        print(f"{w}...")
        os.system(f"camb -n {w} | ansi2txt > {DEFAULT_PARSE_FILENAME}")
        res = parse_file(w, args.csvfile)
        if res == -1:
            not_found.append(w)
        elif res == -2:
            no_def.append(w)

    os.system(f"rm {DEFAULT_PARSE_FILENAME}")
    print_summary(not_found, no_def)
