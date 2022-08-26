from pyglossary import Glossary

def get_first_lines_from_tabfile():
    N = 2000

    Glossary.init()

    glos = Glossary()
    input_dict = "Russian-Russian dictionary.txt"
    #temp_dir = "temp.txt"
    temp_dir = input_dict

    # Save the first N lines of the dictionary to a temporary file
    #with open(input_dict, "r", encoding="utf-8") as f:
    #    lines = f.readlines()[:N]
    #    with open(temp_dir, "w", encoding="utf-8") as f:
    #        f.writelines(lines)

    glos.convert(inputFilename=temp_dir, outputFilename="excerpt-ru-ru.ifo", outputFormat="Stardict")
    glos.convert(inputFilename="excerpt-ru-ru.ifo", outputFilename="sd-from-tabfile.txt", outputFormat="Tabfile")

    glos.convert(inputFilename="Russian-Russian dictionary.ifo", outputFilename="stardict-direct.txt", outputFormat="Tabfile")

def compare_files():
    with open("sd-from-tabfile.txt", "r", encoding="utf-8") as f:
        lines1 = set(f.readlines())
    with open("stardict-direct.txt", "r", encoding="utf-8") as f:
        lines2 = set(f.readlines())

    print("Lines in sd-from-tabfile.txt:", len(lines1))
    print("Lines that are not in sd-from-tabfile.txt:")
    # Print all lines that are not in lines1, but in lines2
    for line in lines2:
        if line not in lines1:
            print(line)
    print("Lines in stardict-direct.txt:", len(lines2))
    print("Lines that are not in stardict-direct.txt:")
    # Print all lines that are not in lines2, but in lines1
    for line in lines1:
        if line not in lines2:
            print(line)

    
if __name__ == "__main__":
    #get_first_lines_from_tabfile()
    compare_files()