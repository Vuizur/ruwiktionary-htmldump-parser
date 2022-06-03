# Russian Wiktionary HTML dump parser

This parses the Russian entries of the Russian Wiktionary using the HTML dump that can be found [here](https://dumps.wikimedia.org/other/enterprise_html/) into a JSON file and into dictionaries for ebook readers. 

At the end the output looks like this:
```
{
    "word": "самоло́в",
    "inflections": [
      "самоло́ве",
      "самоло́вам",
      "самоло́ву",
      "самоло́вах",
      "самоло́вов",
      "самоло́вами",
      "самоло́вы",
      "самоло́вом",
      "самоло́ва"
    ],
    "definitions": [
      "охотн. самодействующий (автоматически срабатывающий) снаряд для ловли зверей, птиц и рыб"
    ],
    "grammar_info": "Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a  по классификации А. А. Зализняка).",
    "IPA": "səmɐˈɫof"
}
```

The generated JSON file and the dictionaries (Stardict, Tabfile with html) can be found in the Releases section so that you don't have to run the script yourself. It uses pyglossary for the dictionary generation, so you can simply change the parameters to generate the format you want.

## Details
It additionally performs some cleanup and adds the comparative forms (which are not in the tables, but instead in the text) to the inflections, generating their alternative forms. Pages with multiple etymologies are also supported, and by default it deletes unneeded inflection entries that have no other content than being an inflection.

## Installation
Then should clone the project, install poetry and then run `poetry install`. 

Then run `poetry run python ./ruwiktionary_htmldump_parser/parse_wiktionary.py --dump_folder_path D:/ruwiktionary-NS0-20220501-ENTERPRISE-HTML  --json_file_name ruwiktionary_words.json` to parse the dictionary into a JSON file.

After that `poetry run python ./ruwiktionary_htmldump_parser/clean_data_for_dictionary.py --input_file ruwiktionary_words.json --output_file ruwiktionary_words_fixed.json` to clean the data.

Then run `poetry run python ./ruwiktionary_htmldump_parser/create_ereader_dictionary.py --json_file_name ruwiktionary_words_fixed.json --output_path Russian-Russian-dict --output_format Stardict` to generate the dictionaries

## Additional info
Be aware that for me on Windows the HTML dumps could only be unpacked using Winrar and not 7-zip