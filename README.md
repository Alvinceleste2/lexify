# Lexify
![hlogo](https://github.com/user-attachments/assets/b2e516ec-0f5d-47f4-b0b7-49b1ce10f5ee)

`Lexify` is a tool to automate the creation of vocabulary flashcards. `Lexify` will search up definitions for each word or expression (included in a list by the user) on the official Cambridge Dictionary and will make a `.csv` file ready to be imported in `Brainscape`.

## Dependencies
`Lexify` makes use of mhwgoo's cambridge tool to search definitions. You can check how to install it here: https://github.com/mhwgoo/cambridge

>[!IMPORTANT]
>Also, you will need `ansi2txt` for the script to work properly.

## How it works
`Lexify` uses the utility previously mentioned to make searches on the dictionary. It then takes the word, pronuntiation, definitions and examples and places them on a `.csv` file prepared for `Brainscape` importation. To give `Lexify` a list of words, you must create a `.txt`file (inside the same directory than the script) with the words and type of words (see examples below) you want to create flashcards for.

To create the words file you first need to know which words you want to save and add them to a `.txt` file separating each one with a linebreak. This could be an example:
```txt
orange
cat
table
up
```

As a single word can have several uses (orange, for example, can be a noun but also an adjective), you will have to specify which type of words you want to save for each of the previous ones. This is done by adding those types you want between parenthesis:
```txt
orange(n)
cat(n)
table(n)
up(adv)
```
You can see every word type supported in this table:

| Abreviation (.txt file)   | Type of word  |
| ------------------------- |:-------------:|
| n                         | noun          |
| v                         | verb          |
| adj                       | adjective     |
| adv                       | adverb        |
| col                       | collocation   |
| id                        | idiom         |

>[!TIP]
>If you want to save several word type definitions for a single word, you can concatenate them this way: `word(a)(b)`, where a and b are element from the list above. Example: `orange(n)(adj)` will store orange definitions as a noun but also as an adjective.

Once the `.txt` file is created properly, you can run the program with:
```bash

$ python3 lexify.py [--wfile word_list.txt] [--cfile output_file.csv]
```
By default, Lexify will take a file named `words.txt` for the word list and `cards.csv` for the output filename.

Additionaly, `Lexify` will inform the user about the words for which any definition have been found, in case any exists. Moreover, the system will track those specified word types which have not been stored, so that there is no redundant or useless information inside the `.txt` file. For example, if the `.txt` contains `orange(n)(v)` or `orange(v)`, the script will tell than no definitions were found for orange(v) (as it does not exist such a verb) but the noun one has been stored.

With all this in mind, the `.csv` file will finally be created and ready for the import. Help and further documentation refering to csv import can be found here: https://brainscape.zendesk.com/hc/en-us/articles/115002369931-How-do-I-import-a-csv-file-correctly

## Examples
Example `.txt` file:

```txt
cat(n)
orange(n)
