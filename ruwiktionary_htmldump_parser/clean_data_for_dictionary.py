import json
from entry_data import EntryData
from ruwiktionary_htmldump_parser.entry_data import print_entry_data_list_to_json


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


def read_json_to_entry_data_list(json_file_path: str) -> list[EntryData]:
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        return [EntryData(**entry_json) for entry_json in json_data]


def remove_separate_inflection_entries(
    entry_data_list: list[EntryData],
) -> list[EntryData]:

    # We want to remove inflections as own entries. We can do this by by looking at entries which are in the inflections
    # of other entries and have in their definition a reference to their base word ("от ...")

    return entry_data_list


def fix_up_entry_data_list_complete(
    entry_data_list: list[EntryData],
) -> list[EntryData]:
    fixed_entry_data_list: list[EntryData] = []
    for entry_data in entry_data_list:
        entry_data = add_comparative_from_grammar_info_to_inflections(entry_data)
        fixed_entry_data_list.append(remove_pointless_no_example_complaint(entry_data))
    return entry_data_list


if __name__ == "__main__":
    # osto = EntryData(**{
    # "word": "неосторо́жный",
    # "inflections": [
    #  "неосторо́жные",
    #  "неосторо́жную",
    #  "неосторо́жною",
    #  "неосторо́жен",
    #  "неосторо́жных",
    #  "неосторо́жного",
    #  "неосторо́жны",
    #  "неосторо́жное",
    #  "неосторо́жному",
    #  "неосторо́жно",
    #  "неосторо́жном",
    #  "неосторо́жна",
    #  "неосторо́жным",
    #  "неосторо́жными",
    #  "неосторо́жной",
    #  "неосторо́жная",
    #  "понеосторо́жнее",
    #  "понеосторо́жней",
    #  "неосторо́жнее",
    #  "неосторо́жней"
    # ],
    # "definitions": [
    #  "действующий без необходимой осторожности (о человеке)",
    #  "совершаемый опрометчиво, без необходимой осторожности (о действиях, поступках, высказываниях и т. п.)"
    # ],
    # "grammar_info": "Прилагательное, качественное, тип склонения по классификации А. Зализняка — 1*a. Сравнительная степень — неосторо́жнее, неосторо́жней.",
    # "IPA": "nʲɪəstɐˈroʐnɨɪ̯"
    # })

    # fix_up_entry_data_list_complete([osto])
    #
    # print(osto)
    #
    # print(fill_up_comparative_degrees(["неосторо́жнее", "неосторо́жней"]))
    # quit()
    entry_data_list = read_json_to_entry_data_list("ruwiktionary_words.json")

    entry_data_list = fix_up_entry_data_list_complete(entry_data_list)

    # Print entry data list to json
    print_entry_data_list_to_json(entry_data_list, "ruwiktionary_words_fixed.json")

    # Print the first 10 items of entry data list
    for entry_data in entry_data_list[:10]:
        print(entry_data)
        print("\n")

    comparative_degrees = "Сравнительная степень — просторе́чнее.".split(
        "Сравнительная степень — "
    )[1].split(".")[0]
    print(comparative_degrees.split(", "))

    print(len("ре́"))
