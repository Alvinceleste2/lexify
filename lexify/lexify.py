import csv
import os
import argparse

import classic as cl
import family as fm

HEADER = [
    "Q. Body",
    "Q. Clarifier",
    "Q. Footnote",
    "A. Body",
    "A. Clarifier",
    "A. Footnote",
]


def init_file(filename):
    f = open(filename, "w", encoding="UTF8", newline="")
    writer = csv.writer(f)
    writer.writerow(HEADER)
    f.close()


def main():
    parser = create_parser()
    args = parser.parse_args()

    init_file(args.csvfile)
    print_starter()

    if args.mode == 0:
        print("CLASSIC MODE SELECTED")
        cl.classic_flow(args)
    elif args.mode == 1:
        print("FAMILIES MODE SELECTED")
        fm.family_flow(args)


def print_starter():
    print(r" _               _  __       ")
    print(r"| |             (_)/ _|      ")
    print(r"| |     _____  ___| |_ _   _ ")
    print(r"| |    / _ \ \/ / |  _| | | |")
    print(r"| |___|  __/>  <| | | | |_| |")
    print(r"\_____/\___/_/\_\_|_|  \__, |")
    print(r"                        __/ |")
    print(r"                       |___/ ")


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
    parser.add_argument(
        "--mode",
        dest="mode",
        type=int,
        help="Select Lexify's mode: 0 for classic, definitions flashcards creator (default), 1 for word families mode",
        default=0,
    )

    return parser


if __name__ == "__main__":
    main()
