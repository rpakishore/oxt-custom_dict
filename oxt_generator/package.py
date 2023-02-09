#https://forum.openoffice.org/en/forum/viewtopic.php?t=33297

from pathlib import Path
from shutil import copy, make_archive, rmtree
import re

def main(wordfile: str, filename:str):
    wordfile = Path(str(wordfile))
    words = generate_dic_wordlist(wordfile)

    folderpath = Path() / f"en_US_{filename}"
    Path.mkdir(folderpath)
    dicpath = folderpath / f"en_US_{filename}.dic"
    words.insert(0, str(len(words)))
    write_to_file(filepath=dicpath, txtblob='\n'.join(words))

    afftemplatefile = Path(__file__).parent / "en_US_private.aff"
    afffile = folderpath / f"en_US_{filename}.aff"
    copy(afftemplatefile, afffile)

    write_xcufile(folderpath, filename)
    write_description(folderpath, filename)

    copy_from = Path(__file__).parent / "README_extension_owner.txt"
    copy_to = folderpath / f"README_extension_owner.txt"
    copy(copy_from, copy_to)

    copy_from = Path(__file__).parent / "license.txt"
    copy_to = folderpath / f"license.txt"
    copy(copy_from, copy_to)

    write_manifest(folderpath, filename)
    final_filename = folderpath.parent / f"en_US_{filename}"
    make_archive(final_filename, 'zip', folderpath)
    final_filename = folderpath.parent / f"en_US_{filename}.zip"
    final_filename.rename(final_filename.with_suffix(".oxt"))
    rmtree(folderpath)



def write_manifest(folderpath: Path, filename: str):
    metapath = folderpath / "META-INF"
    Path.mkdir(metapath)
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE manifest:manifest PUBLIC "-//OpenOffice.org//DTD Manifest 1.0//EN" "Manifest.dtd">
<manifest:manifest xmlns:manifest="http://openoffice.org/2001/manifest">
    <manifest:file-entry manifest:media-type="application/vnd.sun.star.configuration-data" 
        manifest:full-path="dictionaries.xcu"/>
</manifest:manifest>"""
    filepath = metapath / "manifest.xml"
    write_to_file(filepath, content)



def write_xcufile(folderpath:Path, filename: str):
    dict_xcu=f"""<?xml version="1.0" encoding="UTF-8"?>
<oor:component-data xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" oor:name="Linguistic" oor:package="org.openoffice.Office">	
 <node oor:name="ServiceManager">
    <node oor:name="Dictionaries">
    	<node oor:name="HunSpellDic_en-US_{filename}" oor:op="fuse">
            <prop oor:name="Locations" oor:type="oor:string-list">
                <value>%origin%/en_US_{filename}.aff %origin%/en_US_{filename}.dic</value>
            </prop>
            <prop oor:name="Format" oor:type="xs:string">
                <value>DICT_SPELL</value>
            </prop>
            <prop oor:name="Locales" oor:type="oor:string-list">
                <value>en-US</value>
            </prop>
        </node>
    </node>
 </node>
</oor:component-data>"""
    xcu_file = folderpath / "dictionaries.xcu"
    write_to_file(xcu_file, dict_xcu)

def write_description(folderpath: Path, filename: str):
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<description xmlns="http://openoffice.org/extensions/description/2006" xmlns:d="http://openoffice.org/extensions/description/2006"  xmlns:xlink="http://www.w3.org/1999/xlink">
    <version value="2010.08.16" />
    <identifier value="en_US_{filename}" />
    <display-name>
        <name lang="en">en_US_{filename} spelling dictionary</name>
    </display-name>
    <platform value="all" />
    <dependencies>
        <OpenOffice.org-minimal-version value="3.0" d:name="OpenOffice.org 3.0" />
    </dependencies>
</description>"""
    filepath = folderpath / "description.xml"
    write_to_file(filepath, content)


def generate_dic_wordlist(wordfile: Path):
    words = extract_words_from_file(wordfile)
    check_words(words)
    return sorted_nicely(words)
    


def extract_words_from_file(wordfile: Path):
    with open(wordfile, 'r') as f:
        words = f.read()
    words = words.split('\n')
    words = [word.strip() for word in words]
    return words

def write_to_file(filepath: Path, txtblob: str) -> None:
    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(txtblob)

def check_words(words:list[str]) -> None:
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
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(words, key = alphanum_key)