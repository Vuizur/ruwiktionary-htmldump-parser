import dataclasses


@dataclasses.dataclass
class EntryData:
    """Contains the data of one etymology"""

    word: str
    inflections: list[str] = dataclasses.field(default_factory=list)
    definitions: list[str] = dataclasses.field(default_factory=list)
    grammar_info: str = ""
    IPA: str = ""
    #synonyms : list[str] = dataclasses.field(default_factory=list)


