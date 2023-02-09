import os
import zipfile
from pathlib import Path
    
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

with zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    path = Path(r"C:\Users\remaa\Downloads\dict-en_US_private")
    os.chdir(path)
    zipdir(path, zipf)
