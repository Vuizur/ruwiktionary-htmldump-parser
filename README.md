# Russian Wiktionary HTML dump parser

This parses the Russian entries of the Russian Wiktionary using the HTML dump that can be found [here](https://dumps.wikimedia.org/other/enterprise_html/) into a JSON file. 

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

The generated JSON file can be found in the Releases section so that you don't have to run the script yourself.

### Details
It additionally performs some cleanup and adds the comparative forms (which are not in the tables, but instead in the text) to the inflections, generating their alternative forms. Pages with multiple etymologies are also supported, and by default it deletes unneeded inflection entries that have no other content than being an inflection.

### Installation
Then should clone the project, install poetry and then run `poetry install`. 

Then run `poetry run python ./ruwiktionary_htmldump_parser\parse_wiktionary.py` to parse the dictionary into a JSON file

# Additional info
Be aware that for me on Windows the HTML dumps could only be unpacked using Winrar and not 7-zip