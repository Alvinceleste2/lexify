import sys
import urllib.request
import urllib.parse
import urllib.error as err
from bs4 import BeautifulSoup

FULL_TYPE_LIST = [
    " idiom",
    " collocation",
    " phrase",
    " verb",
    " noun",
    " adjective",
    " adverb",
    " determiner",
    " interjection",
    " symbol",
    " pronoun",
    " preposition",
    " abbreviation",
]

file = open("sources/families_vanilla.txt", "r")

data = file.read()
data_into_list = data.split("\n")
data_into_list.pop(-1)

wfile = open("sources/families_db.txt", "w" if len(sys.argv) < 2 else "a")

reached = len(sys.argv) <= 1

for d in data_into_list:
    if not reached:
        if d != f"{sys.argv[1]}":
            continue
        else:
            reached = True

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

    try:
        f = urllib.request.urlopen(req)
    except err.HTTPError as e:
        print(e.reason)
        wfile.write(f"{d}()\n")
        continue
    except err.URLError as e:
        print(e.reason)
        wfile.write(f"{d}()\n")
        continue

    page = f.read().decode("utf-8")

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
    if len(types) == 0:
        line += "()"
    else:
        for e in types:
            line += "(" + e + ")"

    wfile.write(f"{d}{line}\n")

file.close()
wfile.close()
