if __name__ == "__main__":
    # Load the file docs/execution_log.txt
    with open("docs/execution_log.txt", "r", encoding="utf-8") as execution_log_file:
        execution_log_lines = execution_log_file.readlines()
        # iterate over all lines that start with PARSE ERROR
        for line in execution_log_lines:
            if line.startswith("PARSE ERROR"):
                # extract string between "for the word " and ":"
                word = line[line.find("for the word") + 13 : line.find(":")]
                # print the word surrounded by [[]]
                print(f"[[{word}]]")