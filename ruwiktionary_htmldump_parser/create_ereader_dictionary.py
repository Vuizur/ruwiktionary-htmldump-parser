from ruwiktionary_htmldump_parser.entry_data import (
    EntryData,
    read_json_to_entry_data_list,
)
from pyglossary.glossary import Glossary

from stressed_cyrillic_tools import unaccentify
import os
import tarfile


def get_all_inflections(entry_data: EntryData):
    """Generates unaccented inflections for the given entry data, also includes the base word as the first enty"""
    inflections = [entry_data.word]
    for inflection in entry_data.inflections:
        inflections.append(inflection)
        inflections.append(unaccentify(inflection))
    # I tried this because base words don't get found currently due to a bug in sdcv/pyglossary?
    # But they still don't get found in the dictionary
    # inflections.append(entry_data.word)
    inflections.append(unaccentify(entry_data.word))

    # Remove duplicates, while preserving the order of the list
    inflections = list(dict.fromkeys(inflections))

    return inflections


def generate_html_from_definitions(definitions: list[str]):
    """Generates an HTML list from the given definitions"""
    html = "<ol>"
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

    html += "</ol>"
    return html


def convert_line_endings(file_path: str):
    """Converts line endings in the given file to Unix style"""
    with open(file_path, "rb") as file:
        data = file.read()

    with open(file_path, "wb") as file:
        file.write(data.replace(b"\r\n", b"\n"))


def create_ereader_dictionary(
    input_json_file_name: str, output_path: str, output_format="Stardict"
):
    """Creates an Ereader dictionary out of the JSON file using Pyglossary"""

    # Load the JSON file
    entry_data_list = read_json_to_entry_data_list(input_json_file_name)

    # Create a pyglossary dictionary
    Glossary.init()

    glos = Glossary()

    # Add the entries to the dictionary
    for entry_data in entry_data_list:
        if len(entry_data.word) == 0:
            continue
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
        # It is done like this because currently the direct Stardict export does not work for some sort of unkown reason -> Some strange characters? No idea
        print("Writing dictionary to " + output_path + ".ifo")
        glos.write(output_path + ".txt", format="Tabfile")
        glos.convert(
            inputFilename=output_path + ".txt",
            outputFilename=output_path + ".ifo",
            outputFormat="Stardict",
        )

        convert_line_endings(output_path + ".ifo")

    elif output_format == "Tabfile":
        print("Writing dictionary to " + output_path + ".txt")
        glos.write(output_path + ".txt", format="Tabfile")


def pack_stardict_dictionary(
    dictionary_ifo_path: str, tar_gz_path="Russian-Russian-wiktionary.tar.gz"
):
    """Packs the given Stardict dictionary into a .tar.gz file"""

    # Create a tar file
    with tarfile.open(tar_gz_path, "w:gz") as tar:
        # Add the files to the tar file
        tar.add(dictionary_ifo_path, arcname=os.path.basename(dictionary_ifo_path))
        dictionary_base_path = dictionary_ifo_path.rsplit(".", 1)[0]
        tar.add(
            dictionary_base_path + ".dict.dz",
            arcname=os.path.basename(dictionary_base_path) + ".dict.dz",
        )
        tar.add(
            dictionary_base_path + ".idx",
            arcname=os.path.basename(dictionary_base_path) + ".idx",
        )
        tar.add(
            dictionary_base_path + ".syn",
            arcname=os.path.basename(dictionary_base_path) + ".syn",
        )


if __name__ == "__main__":
    # Create a CLI using argparse#
    import argparse

    parser = argparse.ArgumentParser(
        description="Creates an Ereader dictionary out of the JSON file using Pyglossary"
    )
    parser.add_argument(
        "--json_file_name",
        help="The JSON file containing the data of the Wiktionary entries",
    )
    parser.add_argument(
        "--output_path",
        help="The path to the output file",
    )
    parser.add_argument(
        "--output_format",
        help="The format of the output file. Either Stardict or Tabfile.",
    )

    args = parser.parse_args()
    create_ereader_dictionary(args.json_file_name, args.output_path, args.output_format)

    # create_ereader_dictionary(
    #   "ruwiktionary_words_fixed.json", "Russian-Russian dictionary.ifo", "Stardict"
    # )

    # create_ereader_dictionary(
    #   "ruwiktionary_words_fixed.json", "Russian-Russian dictionary.txt", "Tabfile"
    # )
