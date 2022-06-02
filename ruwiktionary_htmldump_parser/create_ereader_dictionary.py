from ruwiktionary_htmldump_parser.entry_data import (
    EntryData,
    read_json_to_entry_data_list,
)
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
        # In the definition, write everything after "◆" in italics
        # and everything before "◆" in normal text
        html += "<li>"
        if "◆" in definition:
            html += definition.split("◆")[0]
            # Add the rest in italics
            html += "<i>" + "◆" + definition.split("◆")[1] + "</i>"
        else:
            html += definition
        html += "</li>"

    html += "</ul>"
    return html


def convert_line_endings(file_path: str):
    """Converts line endings in the given file to Unix style"""
    with open(file_path, "rb") as file:
        data = file.read()

    with open(file_path, "wb") as file:
        file.write(data.replace(b"\r\n", b"\n"))


def create_ereader_dictionary(
    input_json_file_name: str, output_path: str, output_format
):
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
    try:
        output_path = output_path.rsplit(".", 1)[0]
    except:
        pass
    if output_format == "Stardict":
        # Remove the extension from the output path
        print("Writing dictionary to " + output_path + ".ifo")
        glos.write(output_path + ".ifo", format="Stardict")

        convert_line_endings(output_path + ".ifo")

    elif output_format == "Tabfile":
        print("Writing dictionary to " + output_path + ".txt")
        glos.write(output_path + ".txt", format="Tabfile")


if __name__ == "__main__":

    # Create a CLI using argparse#
    import argparse

    parser = argparse.ArgumentParser(
        description="Creates an Ereader dictionary out of the JSON file using Pyglossary"
    )
    parser.add_argument(
        "input_json_file_name",
        help="The JSON file containing the data of the Wiktionary entries",
    )
    parser.add_argument(
        "output_path",
        help="The path to the output file. The extension will be added automatically.",
    )
    parser.add_argument(
        "output_format",
        help="The format of the output file. Either Stardict or Tabfile.",
    )

    args = parser.parse_args()
    create_ereader_dictionary(
        args.input_json_file_name, args.output_path, args.output_format
    )

    # create_ereader_dictionary(
    #    "ruwiktionary_words_fixed.json", "Russian-Russian dictionary.txt", "Stardict"
    # )
