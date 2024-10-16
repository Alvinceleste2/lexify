# Lexify
![hlogo](https://github.com/user-attachments/assets/b2e516ec-0f5d-47f4-b0b7-49b1ce10f5ee)

`Lexify` is a tool to automate the creation of vocabulary flashcards. `Lexify` will search up definitions for each word or expression (included in a list by the user) on the official Cambridge Dictionary and will make a `.csv` file ready to be imported in `Brainscape`.

## Dependencies
`Lexify` makes use of mhwgoo's cambridge tool to search definitions. You can check how to install it here: https://github.com/mhwgoo/cambridge
Also, you will need `ansi2txt` for the script to work properly.

## How it works
`Lexify` uses the utility previously mentioned to make searches on the dictionary. It then takes the word, pronuntiation, definitions and examples and places them on a `.csv` file prepared for `Brainscape` importation. To give `Lexify` a list of words, you must create a `.txt`file (inside the same directory than the script) with the words you want to create flashcards for. Once done, you can run the programm with:
```bash

python3 lexify word-list.txt output-name.csv
```

The `.csv` file will be created and ready for the import. Additionaly, `Lexify` will inform the user about the words for which any definition had been found. Help and further documentation refering to csv import can be found here: https://brainscape.zendesk.com/hc/en-us/articles/115002369931-How-do-I-import-a-csv-file-correctly

## Examples
Example `.txt` file:

