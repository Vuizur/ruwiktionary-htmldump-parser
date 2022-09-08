import argparse
import logging
import os
import json
from bs4 import BeautifulSoup, PageElement
import re

from ruwiktionary_htmldump_parser.clean_inflections import clean_inflection
from ruwiktionary_htmldump_parser.entry_data import EntryData, print_entry_data_list_to_json

# has to contain cyrillic, but not the characters only other slavic languages have


def can_be_russian(text: str):
    text_lower = text.lower()
    return (
        bool(re.search("[а-яА-Я]", text))
        and "ў" not in text_lower
        and "ї" not in text_lower
        and "є" not in text_lower
        and "ћ" not in text_lower
        and "ђ" not in text_lower
        and "ґ" not in text_lower
        and "і" not in text_lower
        and "қ" not in text_lower
    )


def get_lemma(lemma_bold_paragraph) -> str:
    if lemma_bold_paragraph.find("span"):
        for span in lemma_bold_paragraph.find_all("span"):
            span.extract()
        return lemma_bold_paragraph.text
    else:
        return lemma_bold_paragraph.text


def get_morph_table_words(morph_table) -> list[str]:
    words: list[str] = []
    rows = morph_table.find("tbody").find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        for cell in cells[1:]:  # Leave out left definition cell

            words.extend(cell.get_text("|").split("|"))

    return [
        word.replace("буду/будешь… ", "")
        for word in words
        if word != "-" and word != "—"
    ]


def extract_definition_from_section(entry_data: EntryData, section: PageElement):
    """Updates the entry data with the definitions"""
    # find the h4 tag which has an id that contains the word "Значение"
    definition_el = section.find("h4", id=re.compile("Значение"))
    # definition_el = section.find("h4", id="Значение")
    if definition_el == None:
        return
    else:
        ol = definition_el.find_next("ol")
        for li in ol.children:
            def_text = li.text
            if def_text != "" and def_text != "\n":
                entry_data.definitions.append(li.text.strip())


def extract_entry_data_from_section(morphology_section: PageElement) -> EntryData:
    # This takes a section with the format
    #  <section>
    #    <h3 id="Морфологические и синтаксические свойства">
    #    <table class="morfotable-ru">

    try:
        lemma_p = morphology_section.find("p", about=True)
        lemma = get_lemma(lemma_p.b)
    except Exception:
        # This does sometimes happen with weird formatted (second) etymologies
        logging.info("No lemma found in section: " + str(morphology_section))
        return None
    entry_data = EntryData(lemma)

    try:
        # Find the second paragraph tag in the morphology section
        grammar_info_paragraph = morphology_section.find(
            "p", about=True
        ).find_next_sibling("p")
        entry_data.grammar_info = grammar_info_paragraph.text.strip()

    except Exception:
        # This does sometimes happen with weird formatted (second) etymologies
        logging.info("No grammar info found in section: " + str(morphology_section))

    morpher_table = morphology_section.find("table", {"class": "morfotable"})

    if morpher_table != None:
        entry_data.inflections.extend(get_morph_table_words(morpher_table))
    # Iterates through the sections with different info about the word
    for next_sbln in morphology_section.next_siblings:
        if next_sbln.find("h3", id=re.compile("Семантические_свойства")):
            extract_definition_from_section(entry_data, next_sbln.find("section"))
        if next_sbln.find("h3", id=re.compile("Произношение")):
            try:
                entry_data.IPA = next_sbln.find("span", class_="IPA").text
            except Exception:
                logging.info("No pronunciation found in section: " + str(next_sbln))
    return entry_data


def section_contains_two_etymologies(section) -> bool:
    # h2 etc
    return section.find("h2")


def append_definition_to_entry_data(
    entry_data: EntryData, section_containing_lemma: PageElement
) -> None:
    for next_sbln in section_containing_lemma.next_siblings:
        if next_sbln.find("h3", id=re.compile("Семантические_свойства")):
            extract_definition_from_section(entry_data, next_sbln.find("section"))


def get_stressed_words_from_html(html: str) -> list[EntryData]:

    # Lxml should be faster than the standard parser
    soup = BeautifulSoup(html, "lxml")
    # Important: The HTML dump pages are structured differently from the online hosted version
    russian_h1 = soup.find("h1", id="Русский")
    if russian_h1 != None:
        for sibling in russian_h1.next_siblings:
            if sibling.name == "section":
                if not section_contains_two_etymologies(sibling):
                    entry_data = extract_entry_data_from_section(sibling)
                    if entry_data != None:
                        return [entry_data]
                else:
                    entry_data_list: list[EntryData] = []
                    # Each iteration here iterates over on etymology
                    for sibling in russian_h1.next_siblings:
                        if sibling.name == "section":
                            # Get first subsection
                            first_subsection = sibling.find("section")
                            entry_data = extract_entry_data_from_section(
                                first_subsection
                            )
                            if entry_data != None:
                                entry_data_list.append(entry_data)
                    return entry_data_list
        return []
    else:
        return []


def extract_entries_from_html_dump(dump_folder_path, json_file_path) -> None:
    """Extracts entries from the HTML dump and dumps them to a JSON file"""
    entry_data_all_words: list[EntryData] = []
    i = 0
    for path in os.scandir(dump_folder_path):
        filename = path.path
        print(filename)
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                name = obj["name"]
                if can_be_russian(name):
                    try:
                        entry_data_list = get_stressed_words_from_html(
                            obj["article_body"]["html"]
                        )
                        if entry_data_list != None:
                            entry_data_all_words.extend(entry_data_list)
                    except Exception as e:
                        print(f"PARSE ERROR for the word {name}: {e}")
                        pass

                i += 1
                if i % 5000 == 0:
                    print(i)
    for entry_data in entry_data_all_words:
        entry_data = clean_inflection(entry_data)

    print_entry_data_list_to_json(entry_data_all_words, json_file_path)


if __name__ == "__main__":
    # Take a command line parameter called "dump folder path" using Argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dump_folder_path", help="The path to the folder containing the HTML dump"
    )
    # Add a command line parameter called "json file name" using Argparse
    # and add a default value
    parser.add_argument(
        "--json_file_name",
        help="The name of the JSON file to write the extracted data to",
        default="extracted_data.json",
    )

    args = parser.parse_args()

    extract_entries_from_html_dump(args.dump_folder_path, args.json_file_name)

    #json_path = "ruwiktionary_words.json"
    #dump_folder_path = "D:/ruwiktionary-NS0-20220501-ENTERPRISE-HTML.json"
    #extract_entries_from_html_dump(dump_folder_path, json_path)
