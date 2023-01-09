from ruwiktionary_htmldump_parser.htmldumpparser import HTMLDumpParser


if __name__ == "__main__":
    parser = HTMLDumpParser(
        intermediate_data_path="ruwiktionary_words.json",
        cleaned_data_path="ruwiktionary_words_fixed.json",
    )
    #parser.parse_wiktionary_dump()
    #parser.clean_entries()
    #parser.create_dictionary()
    parser.output_path = "Russian-Russian dictionary (Wiktionary).ifo"
    parser.pack_dictionary()
    