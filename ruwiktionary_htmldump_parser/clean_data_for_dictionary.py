import json
from entry_data import EntryData

def add_po_to_degrees(degrees: list[str]) -> list[str]:
    assert(len(degrees) == 2)
    # Assert that no degree starts with "по"
    assert(not any(degree.startswith("по") for degree in degrees))

    return ["по " + degree for degree in degrees] + degrees

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
        # Check if none of the degrees start with "по"
        if not any(degree.startswith("по") for degree in degrees):
            # Add по to both degrees
            return ["по " + degree for degree in degrees] + degrees
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
    #TODO: finish


def add_comparative_from_grammar_info_to_inflections(entry_data: EntryData):
    if "Сравнительная степень не образуется" in entry_data.grammar_info:
        return entry_data
    if "Сравнительная степень — " in entry_data.grammar_info:
        # Get string from Сравнительная степень to the next dot
        comparative_degrees = entry_data.grammar_info.split("Сравнительная степень — ")[1].split(".")[0]
        comparative_degrees = comparative_degrees.split(", ")
        comparative_degrees = fill_up_comparative_degrees(comparative_degrees)
        # Print to console
        print("Сравнительная степень: " + str(comparative_degrees))
        #Add the comparative degree to the inflections
        entry_data.inflections.extend(comparative_degrees)

def remove_pointless_no_example_complaint(entry_data: EntryData) -> EntryData:
    entry_data.definitions = [
        definition.translate(
            "◆ Отсутствует пример употребления (см. рекомендации).", ""
        ).strip()
        for definition in entry_data.definitions
    ]

def read_json_to_entry_data_list(json_file_path: str) -> list[EntryData]:
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        return [EntryData.from_json(entry_json) for entry_json in json_data]

def remove_separate_inflection_entries(entry_data_list: list[EntryData]) -> list[EntryData]:
    
    # We want to remove inflections as own entries. We can do this by by looking at entries which are in the inflections
    # of other entries and have in their definition a reference to their base word ("от ...")
   
    return entry_data_list

if __name__ == "__main__":
    entry_data_list = read_json_to_entry_data_list("ruwiktionary_words.json")
    comparative_degrees = "Сравнительная степень — просторе́чнее.".split("Сравнительная степень — ")[1].split(".")[0]
    print(comparative_degrees.split(", "))

    print(len("ре́"))