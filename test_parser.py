from ruwiktionary_htmldump_parser.htmldumpparser import HTMLDumpParser


if __name__ == "__main__":
    parser = HTMLDumpParser(
        "123test",
        intermediate_data_path="ruwiktionary_words.json",
        cleaned_data_path="ruwiktionary_words_fixed.json",
    )
    parser.clean_entries()
