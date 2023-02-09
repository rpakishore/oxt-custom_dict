from pathlib import Path
import re
def generate_dic_wordlist_from_file(wordfile: Path) -> list[str]:
    """Calls a series of functions to generate a usable wordlist from the specified `wordfile`
    """
    words = extract_words_from_file(wordfile)
    check_words(words)
    return sorted_nicely(words)
    
def extract_words_from_file(wordfile: Path) -> list[str]:
    """Reads the list of words from the specified `wordfile`
    """
    with open(wordfile, 'r') as f:
        words = f.read()
    words = words.split('\n')
    words = [word.strip() for word in words]
    return words

def check_words(words:list[str]) -> None:
    """ Checks if the input list of words meet the custom criteria set to generate a dictionary.
        Creates an error if exceptions are found.
    """
    exceptions = []
    digit_regex = re.compile(r".*\d+.*")
    for word in words:
        if ' ' in word:
            exceptions.append(f"{word} - Empty space found in word. Enter 1 word per line, no space")

        if digit_regex.search(word):
            exceptions.append(f"{word} - Numeric value found in word. Remove entries with numeric values")

    if exceptions:
        for exception in exceptions:
            print(exception)
        raise Exception("Check the above messages for corrections")
    return 

def sorted_nicely( words: list[str] ) -> list[str]: 
    """ Sort the given iterable in the way that humans expect. (Alphanumerically)""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(words, key = alphanum_key)