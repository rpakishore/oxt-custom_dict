from pathlib import Path
from shutil import copy, make_archive

def aff_file(folderpath: Path, filename: str):
    """Generate the `.aff` file"""
    afftemplatefile = Path(__file__).parent / "en_US_private.aff"
    afffile = folderpath / f"en_US_{filename}.aff"
    copy(afftemplatefile, afffile)

def dicfile(folderpath: Path, filename: str, words: list):
    """Generate the `.dic` file"""
    dicpath = folderpath / f"en_US_{filename}.dic"
    words.insert(0, str(len(words)))
    write_to_file(filepath=dicpath, txtblob='\n'.join(words))

def license(folderpath: Path):
    """Copy over template `license.txt` file"""
    copy_from = Path(__file__).parent / "license.txt"
    copy_to = folderpath / f"license.txt"
    copy(copy_from, copy_to)

def readme(folderpath: Path):
    """Copy over template `README_extension_owner.txt` file"""
    copy_from = Path(__file__).parent / "README_extension_owner.txt"
    copy_to = folderpath / f"README_extension_owner.txt"
    copy(copy_from, copy_to)

def manifest(folderpath: Path):
    """Generate the `manifest.xml` file"""
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

def xcufile(folderpath:Path, filename: str):
    """Generate the `.xcu` file"""
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

def description(folderpath: Path, filename: str):
    """Generate the `description.xml` file"""
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

def write_to_file(filepath: Path, txtblob: str) -> None:
    """Writes the specified textblob to the filepath"""
    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(txtblob)

def create_zip_from_folder(folderpath:Path, filename: str) -> str:
    """Creates a zip archive of the folders in `folderpath`. returns the filename"""
    final_filename = folderpath.parent / f"en_US_{filename}"
    make_archive(final_filename, 'zip', folderpath)
    final_filename = folderpath.parent / f"en_US_{filename}.zip"
    return final_filename