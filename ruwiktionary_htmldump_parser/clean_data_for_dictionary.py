from entry_data import EntryData
from ruwiktionary_htmldump_parser.entry_data import print_entry_data_list_to_json, read_json_to_entry_data_list
from ruwiktionary_htmldump_parser.helper_methods import unaccentify
import argparse


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
                        #print("Removed definition: " + definition)
            if entry_data.definitions == []:
                continue
        filtered_entry_data_list.append(entry_data)

    return filtered_entry_data_list


def fix_up_entry_data_list_complete(
    entry_data_list: list[EntryData],
) -> list[EntryData]:

    fixed_list = [
        remove_pointless_no_example_complaint(
            add_comparative_from_grammar_info_to_inflections(entry_data)
        )
        for entry_data in entry_data_list
    ]

    fixed_list = remove_separate_inflection_entries(fixed_list)

    return fixed_list


if __name__ == "__main__":

    # Take arguments using Argparse
    parser = argparse.ArgumentParser(
        description="Fix up the entries in the dictionary"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="The input JSON file to fix up",
        required=True,
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="The output JSON file to write to",
        required=True,
    )
    args = parser.parse_args()

    entry_data_list = read_json_to_entry_data_list(args.input_file)

    #entry_data_list = read_json_to_entry_data_list("ruwiktionary_words.json")

    entry_data_list = fix_up_entry_data_list_complete(entry_data_list)

    #print_entry_data_list_to_json(entry_data_list, "ruwiktionary_words_fixed.json")

    print_entry_data_list_to_json(entry_data_list, args.output_file)
