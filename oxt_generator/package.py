#https://forum.openoffice.org/en/forum/viewtopic.php?t=33297

from pathlib import Path
from shutil import rmtree
from oxt_generator import file_generator
from oxt_generator.word_list import generate_dic_wordlist_from_file

def create_oxt(wordfile: str, filename:str):
    wordfile = Path(str(wordfile))
    words = generate_dic_wordlist_from_file(wordfile)

    folderpath = Path() / f"en_US_{filename}"
    Path.mkdir(folderpath)

    file_generator.dicfile(folderpath, filename, words)
    file_generator.aff_file(folderpath, filename)
    file_generator.xcufile(folderpath, filename)
    file_generator.description(folderpath, filename)
    file_generator.manifest(folderpath)

    #Copy over templates
    file_generator.readme(folderpath)
    file_generator.license(folderpath)

    final_filename = file_generator.create_zip_from_folder(folderpath=folderpath, filename=filename)
    final_filename.rename(final_filename.with_suffix(".oxt"))

    #Cleanup
    rmtree(folderpath)