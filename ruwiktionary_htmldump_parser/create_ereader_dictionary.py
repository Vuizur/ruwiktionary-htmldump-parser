from ruwiktionary_htmldump_parser.entry_data import EntryData, read_json_to_entry_data_list
from pyglossary.glossary import Glossary

from ruwiktionary_htmldump_parser.helper_methods import unaccentify

def get_all_inflections(entry_data: EntryData):
    """Generates unaccented inflections for the given entry data, also includes the base word as the first enty"""
    inflections = [entry_data.word]
    for inflection in entry_data.inflections:
        inflections.append(inflection)
        inflections.append(unaccentify(inflection))
    inflections.append(unaccentify(entry_data.word))
    
    # Remove duplicates, while preserving the order of the list
    inflections = list(dict.fromkeys(inflections))

    return inflections

def generate_html_from_definitions(definitions: list[str]):
    """Generates an HTML list from the given definitions"""
    html = "<ul>"
    for definition in definitions:
        html += "<li>" + definition + "</li>"
    html += "</ul>"
    return html


def create_ereader_dictionary(input_json_file_name: str, output_path: str):
    """Creates an Ereader dictionary out of the JSON file using Pyglossary"""

    # Load the JSON file
    entry_data_list = read_json_to_entry_data_list(input_json_file_name)

    # Create a pyglossary dictionary
    Glossary.init()

    glos = Glossary()

    # Add the entries to the dictionary
    for entry_data in entry_data_list:
        word = get_all_inflections(entry_data)
        # Continue if no definitions are available
        if len(entry_data.definitions) == 0:
            continue

        html = generate_html_from_definitions(entry_data.definitions)
        glos.addEntryObj(glos.newEntry(word, html, defiFormat="h"))

    # Write the dictionary to the output file
    glos.setInfo("title", "Русский Викисловарь")
    glos.setInfo("author", "Русский Викисловарь")
    glos.sourceLangName = "Russian"
    glos.targetLangName = "Russian"
    
    print("Writing dictionary to " + output_path)
    glos.write(output_path, format="Tabfile")

if __name__ == "__main__":
    create_ereader_dictionary(
        "ruwiktionary_words_fixed.json", "Russian-Russian dictionary.txt"
    )
