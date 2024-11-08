import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

FULL_TYPE_LIST = [
    "idiom",
    "collocation",
    "phrase",
    "verb",
    "noun",
    "adjective",
    "adverb",
    "determiner",
    "interjection",
    "symbol",
    "pronoun",
    "preposition",
    "abbreviation",
]

file = open("sources/families_vanilla.txt", "r")

data = file.read()
data_into_list = data.split("\n")
data_into_list.pop(-1)

wfile = open("sources/families_db.txt", "w")

for d in data_into_list:
    u = ""
    print(d)
    if d[0] == "\t":
        u = d[1 : len(d) + 1]
    else:
        wfile.write(f"{d}\n")
        continue

    url_page = f"https://wordtype.org/of/{u}"
    encoded_url = urllib.parse.quote(url_page, safe=":/")
    print(url_page)
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    req = urllib.request.Request(encoded_url, None, headers)
    f = urllib.request.urlopen(req)
    page = f.read().decode("utf-8")
    # print(page)

    soup = BeautifulSoup(page, "html.parser")

    # Find all <h2> tags
    h2_tags = soup.findAll("title")

    types = []

    # Print the text of each <h2> tag
    if h2_tags is not None:
        for h2 in h2_tags:
            if h2 is not None:
                print(h2)
                for e in FULL_TYPE_LIST:
                    if e in h2.get_text():
                        types.append(e)

    line = ""
    for e in types:
        line += "(" + e + ")"

    wfile.write(f"{d}{line}\n")

file.close()
wfile.close()
