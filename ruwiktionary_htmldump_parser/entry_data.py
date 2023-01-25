import dataclasses
import json
from typing import Optional


@dataclasses.dataclass
class EntryData:
    """Contains the data of one etymology"""

    word: str
    canonical_form: str
    language: str
    alternative_form: Optional[str] = None
    inflections: list[str] = dataclasses.field(default_factory=list)
    definitions: list[str] = dataclasses.field(default_factory=list)
    grammar_info: str = ""
    IPA: str = ""
    # synonyms : list[str] = dataclasses.field(default_factory=list)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def print_entry_data_list_to_json(
    entry_data_list: list[EntryData], json_file_name: str
):
    with open(json_file_name, "w", encoding="utf-8") as json_file:
        json.dump(
            entry_data_list,
            json_file,
            cls=EnhancedJSONEncoder,
            indent=2,
            ensure_ascii=False,
        )


def read_json_to_entry_data_list(json_file_path: str) -> list[EntryData]:
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        return [EntryData(**entry_json) for entry_json in json_data]
