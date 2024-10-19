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

Additionaly, `Lexify` will inform the user about the words for which any definition have been found, in case any exists. Moreover, the system will track those specified word types which have not been stored, so that there is no redundant or useless information inside the `.txt` file. For example, if the `.txt` contains `orange(n)(v)`, the script will tell that no definitions were found for orange(v) (as it does not exist such a verb) although orange(n) has been found and stored in correctly.

With all this in mind, the `.csv` file will finally be created and ready for the import. Help and further documentation refering to csv import can be found here: https://brainscape.zendesk.com/hc/en-us/articles/115002369931-How-do-I-import-a-csv-file-correctly

## Examples
## Example 1
### Example `.txt` file (words.txt):

```txt
cat(n)
orange(n)(adj)
eat(v)
eat your words(id)
confess(v)
do business(col)
```

### `Lexify` output:
```terminal
$ python3 lexify
 _               _  __       
| |             (_)/ _|      
| |     _____  ___| |_ _   _ 
| |    / _ \ \/ / |  _| | | |
| |___|  __/>  <| | | | |_| |
\_____/\___/_/\_\_|_|  \__, |
                        __/ |
                       |___/ 
{'cat': [' noun'], 'orange': [' noun', ' adjective'], 'eat': [' verb'], 'eat your words': [' idiom'], 'confess': [' verb'], 'do business': [' collocation']}
cat...
orange...
eat...
eat your words...
confess...
do business...

✅Every word has been given an appropiate meaning
```

### Output `.csv` file:
```csv
Q. Body,Q. Clarifier,Q. Footnote,A. Body,A. Clarifier,A. Footnote
**cat**,uk |kæt| us |kæt|, noun,"**1. a small animal with fur, four legs, a tail, and claws, usually kept as a pet or for catching mice**

**2. any member of the group of animals similar to the cat, such as the lion**
* *""the cat family""*

"
**orange**,uk |ˈɒr.ɪndʒ| us |ˈɔːr.ɪndʒ|, noun,"**1. a round sweet fruit that has a thick orange skin and an orange centre divided into many parts [C]**
* *""a glass of orange juice""*

**2. a colour between red and yellow [C/U]**
* *""Orange is her favourite colour.""*

"
**orange**,uk |ˈɒr.ɪndʒ| us |ˈɔːr.ɪndʒ|, adjective,"**1. of a colour between red and yellow**
* *""The setting sun filled the sky with a deep orange glow.""*

"
**eat**,uk |iːt| us |iːt| , verb,"**1. to put or take food into the mouth, chew it (= crush it with the teeth), and swallow it**
* *""Do you eat meat?""*
* *""When I've got a cold, I don't feel like eating.""*
* *""We usually eat (= have a meal) at about seven o'clock.""*

"
**eat your words**, , idiom,"**1. to admit that something you said before was wrong**
* *""Sam said it would never sell, but when he sees these sales figures he'll have to eat his words.""*

"
**confess**,uk |kənˈfes| us |kənˈfes|, verb,"**1. to admit that you have done something wrong or something that you feel guilty or bad about**
* *""[+ that] She confessed to her husband that she had sold her wedding ring.""*
* *""He confessed to sleeping/having slept through most of the movie.""*
* *""He has confessed to the murder.""*
* *""[+ (that)] I have to confess (that) when I first met Reece I didn't think he was very bright.""*
* *""It was all very confusing, I must confess.""*

"
**do business with someone/something**, , collocation,"**1. to buy or sell goods or services from or to a person or organization**
* *""Our firm does a lot of business with overseas customers.""*
* *""He cautions against doing business with contractors who promise to make repairs but ask to be paid up front.""*

"
```

### Brainscape import
One imported into `Brainscape`, the cards will have this look:

.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}

<p align="center">
<img src="https://github.com/user-attachments/assets/757abb26-7417-4b2b-b7b5-f87adbaa8300" width="200" class="center">

<img src="https://github.com/user-attachments/assets/05ca315c-f784-48cd-9838-724e99ade004" width="200" class="center">

<img src="https://github.com/user-attachments/assets/1783c4b9-1acf-4ef6-bacb-4c7cf1a5a1d0" width="200" class="center">

<img src="https://github.com/user-attachments/assets/c611ca46-6f64-499d-8714-1c99d7fa0fbd" width="200" class="center">
</p>

<p align="center">
<img src="https://github.com/user-attachments/assets/8f16ce21-df9b-454e-ad42-35a5d1ba52af" width="200" class="center">

<img src="https://github.com/user-attachments/assets/5ea69383-88df-4fc8-81a8-6d7581f529a2" width="200" class="center">

<img src="https://github.com/user-attachments/assets/e4de8a78-80fe-44ce-9c7d-d416106f0d68" width="200" class="center">
<\p>




