from typing import Callable
from ruwiktionary_htmldump_parser.entry_data import (
    EntryData,
    print_entry_data_list_to_json,
    read_json_to_entry_data_list,
)
import argparse

from stressed_cyrillic_tools import unaccentify

# Here the a bit more agressive cleanup is performed


def add_po_to_degrees(degrees: list[str]) -> list[str]:
    assert len(degrees) == 2

    return ["по" + degree for degree in degrees] + degrees


# Fills up the comparative degrees with the missing prefix "по"
def fill_up_comparative_degrees(degrees: list[str]) -> list[str]:

    if len(degrees) > 4:
        print("Too many comparative degrees")
        print(degrees)
        return degrees
    elif len(degrees) == 4:
        return degrees
    elif len(degrees) == 3:
        print("Weird number of degrees, why?")
        print(degrees)
        return degrees
    elif len(degrees) == 2:
        # Check if the last 2 characters of the degree strings are different
        if degrees[0][-2:] != degrees[1][-2:]:
            return ["по" + degree for degree in degrees] + degrees
        else:
            print("по form only?" + str(degrees))
            return degrees
    elif len(degrees) == 1:
        degree = degrees[0]
        # Get the last two non-diacritic characters of the degree
        if degree.endswith("ее"):
            return add_po_to_degrees([degree[:-2] + "ей", degree])
        elif degree.endswith("е́е"):
            return add_po_to_degrees([degree[:-2] + "е́й", degree])
        else:
            print("Unknown degree: " + degree)
            return degrees
    return degrees


def add_comparative_from_grammar_info_to_inflections(
    entry_data: EntryData,
) -> EntryData:
    if "Сравнительная степень не образуется" in entry_data.grammar_info:
        return entry_data
    if "Сравнительная степень — " in entry_data.grammar_info:
        # Get string from Сравнительная степень to the next dot
        comparative_degrees = entry_data.grammar_info.split("Сравнительная степень — ")[
            1
        ].split(".")[0]
        comparative_degrees = comparative_degrees.split(", ")
        # Delete △ from each degree
        comparative_degrees = [
            degree.replace("△", "") for degree in comparative_degrees
        ]
        comparative_degrees = fill_up_comparative_degrees(comparative_degrees)
        # Print to console
        # print("Сравнительная степень: " + str(comparative_degrees))
        # Add the comparative degree to the inflections
        entry_data.inflections.extend(comparative_degrees)
    return entry_data


def remove_pointless_no_example_complaint(entry_data: EntryData) -> EntryData:
    entry_data.definitions = [
        definition.replace(
            "◆ Отсутствует пример употребления (см. рекомендации).", ""
        ).strip()
        for definition in entry_data.definitions
    ]
    return entry_data


def remove_separate_inflection_entries(
    entry_data_list: list[EntryData],
) -> list[EntryData]:

    # We want to remove inflections as own entries. We can do this by by looking at entries which are in the inflections
    # of other entries and have in their definition a reference to their base word ("от ...")

    # Create a dictionary with the inflections as keys and the base words as values
    inflection_to_base_word_dict: dict[str, list[str]] = {}
    for entry_data in entry_data_list:
        for inflection in entry_data.inflections:
            # Append the base word to the list of base words for this inflection, so that we have a list
            # of base words for each inflection
            inflection_to_base_word_dict.setdefault(inflection, []).append(
                entry_data.word
            )

    filtered_entry_data_list: list[EntryData] = []
    # Iterate through the entries that have no inflections
    for entry_data in entry_data_list:
        if (
            len(entry_data.inflections) == 0
            and entry_data.word in inflection_to_base_word_dict
        ):
            base_words = inflection_to_base_word_dict[entry_data.word]
            for base_word in base_words:
                for definition in entry_data.definitions:
                    if "от " + unaccentify(base_word) in definition:
                        entry_data.definitions.remove(definition)
                        # print("Removed definition: " + definition)
            if entry_data.definitions == []:
                continue
        filtered_entry_data_list.append(entry_data)

    return filtered_entry_data_list


def remove_exotic_line_separators(word: str) -> str:
    """Turn exotic line separators into line breaks and also remove non-breaking spaces"""
    # I choose HTML here because using \n will probably break sdcv -> Let's hope it works without
    line_sep = "<br>"
    return (
        word.replace("\u2028", line_sep)
        .replace("\u2029", line_sep)
        .replace("\u00a0", " ")
        .replace("\u0085", line_sep)
        .replace("\u000C", line_sep)
        .replace("\u000B", line_sep)
        .replace("\n", line_sep)
    )


def apply_function_to_each_entry(
    entry_data_list: list[EntryData], function: Callable[[str], str]
) -> list[EntryData]:
    """This function applies a function to each word, definition, inflection, grammar info and IPA field in the entry data list"""

    for entry_data in entry_data_list:
        entry_data.word = function(entry_data.word)
        entry_data.definitions = [
            function(definition) for definition in entry_data.definitions
        ]
        entry_data.inflections = [
            function(inflection) for inflection in entry_data.inflections
        ]
        entry_data.grammar_info = function(entry_data.grammar_info)
        entry_data.IPA = function(entry_data.IPA)
    return entry_data_list


# Remove LS ans PS line separators from the entry data -> They break sdcv and KOReader
def remove_ls_ps_line_separators(entry_data: EntryData) -> EntryData:
    entry_data.definitions = [
        remove_exotic_line_separators(definition)
        for definition in entry_data.definitions
    ]
    entry_data.word = remove_exotic_line_separators(entry_data.word)
    entry_data.inflections = [
        remove_exotic_line_separators(inflection)
        for inflection in entry_data.inflections
    ]
    entry_data.grammar_info = remove_exotic_line_separators(entry_data.grammar_info)
    entry_data.IPA = remove_exotic_line_separators(entry_data.IPA)

    return entry_data


def fix_up_entry_data_list_complete(
    entry_data_list: list[EntryData],
) -> list[EntryData]:
    print("DEPRECATED")

    fixed_list = [
        remove_ls_ps_line_separators(
            remove_pointless_no_example_complaint(
                add_comparative_from_grammar_info_to_inflections(entry_data)
            )
        )
        for entry_data in entry_data_list
    ]

    fixed_list = remove_separate_inflection_entries(fixed_list)

    return fixed_list


# def fix_up_entry_data_list_new(
#    entry_data_list: list[EntryData],
# ) -> list[EntryData]:
#    # Apply remove_exotic_line_separators to each entry
#    entry_data_list = apply_function_to_each_entry(entry_data_list, remove_exotic_line_separators)


def scan_json_for_unusual_line_terminators(json_file: str) -> None:
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:
            if line != remove_exotic_line_separators(line):
                print("Found unusual line terminator: " + line)
                print("Edited: " + remove_exotic_line_separators(line))


if __name__ == "__main__":
    # scan_json_for_unusual_line_terminators("ruwiktionary_words_fixed.json")
    # quit()
    # Take arguments using Argparse
    parser = argparse.ArgumentParser(description="Fix up the entries in the dictionary")
    parser.add_argument(
        "--input_file",
        type=str,
        help="The input JSON file to fix up",
        required=True,
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="The output JSON file to write to",
        required=True,
    )
    args = parser.parse_args()

    entry_data_list = read_json_to_entry_data_list(args.input_file)

    # entry_data_list = read_json_to_entry_data_list("ruwiktionary_words.json")

    entry_data_list = fix_up_entry_data_list_complete(entry_data_list)

    # print_entry_data_list_to_json(entry_data_list, "ruwiktionary_words_fixed.json")

    print_entry_data_list_to_json(entry_data_list, args.output_file)
