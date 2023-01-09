
from ruwiktionary_htmldump_parser.entry_data import print_entry_data_list_to_json, read_json_to_entry_data_list
from ruwiktionary_htmldump_parser.parse_wiktionary import extract_entries_from_html_dump
from ruwiktionary_htmldump_parser.clean_data_for_dictionary import fix_up_entry_data_list_complete
from ruwiktionary_htmldump_parser.create_ereader_dictionary import create_ereader_dictionary, pack_stardict_dictionary

class HTMLDumpParser:
    
    # Init with parameters: wiktionary_dump_path, cleaned_data_path, output_path, by default all null
    def __init__(self, intermediate_data_path: str = "ruwiktdata_int.json", cleaned_data_path: str = "ruwiktdata_cleaned.json"):
        self.intermediate_data_path = intermediate_data_path
        self.cleaned_data_path = cleaned_data_path

    def parse_wiktionary_dump(self):
        extract_entries_from_html_dump(self.intermediate_data_path)

    def clean_entries(self):
        data = read_json_to_entry_data_list(self.intermediate_data_path)
        cleaned_data = fix_up_entry_data_list_complete(data)
        print_entry_data_list_to_json(cleaned_data, self.cleaned_data_path)

    def create_dictionary(self, output_path = "Russian-Russian dictionary (Wiktionary).ifo"):
        create_ereader_dictionary(self.cleaned_data_path, output_path )
        self.output_path = output_path

    def pack_dictionary(self, output_path = "Russian-Russian dictionary (Wiktionary).tar.gz"):
        
        pack_stardict_dictionary(self.output_path, output_path)