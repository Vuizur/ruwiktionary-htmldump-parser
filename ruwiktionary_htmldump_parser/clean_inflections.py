from entry_data import EntryData


def word_is_useless_grammatical_info(word: str) -> bool:
    return word.strip() in ["одуш.", "одуш"]


def strip_punctuation(word: str) -> str:
    return word.strip(",.!?:;* ")


def strings_only_differ_in_last_2_characters(string1: str, string2: str) -> bool:
    return string1[:-2] == string2[:-2]


def clean_inflection(entry_data: EntryData) -> EntryData:
    """
    Removes inflections that are either grammatical tags or punctuation or otherwise undesired, plus remove duplicates
    """

    # Clean all inflections from punctuation
    entry_data.inflections = [
        strip_punctuation(inflection)
        for inflection in entry_data.inflections
        if strip_punctuation(inflection) != ""
    ]

    # Clean now all empty inflections
    entry_data.inflections = [
        inflection for inflection in entry_data.inflections if inflection.strip() != ""
    ]

    # Remove inflections that are the same as the lemma
    entry_data.inflections = [
        inflection
        for inflection in entry_data.inflections
        if inflection != entry_data.word
    ]

    # Remove inflections that are grammatical tags
    entry_data.inflections = [
        inflection
        for inflection in entry_data.inflections
        if not word_is_useless_grammatical_info(inflection)
    ]

    fixed_inflections: list[str] = []
    # Iterate through all inflections
    for inflection in entry_data.inflections:
        if " " in inflection:
            parts = inflection.split(" ")
            if len(parts) == 2 and strings_only_differ_in_last_2_characters(
                parts[0], parts[1]
            ):
                fixed_inflections.append(parts[0])
                fixed_inflections.append(parts[1])
            else:
                fixed_inflections.append(inflection)
        else:
            fixed_inflections.append(inflection)
    
    entry_data.inflections = fixed_inflections
    # Remove duplicates
    entry_data.inflections = list(set(entry_data.inflections))
