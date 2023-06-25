import sys
import os
import glob
from script import processfile, keywords_search

 

def get_files(folder_name):
    directory_path = os.path.join(os.getcwd(), folder_name)
    pdf_files_paths = []
    for entry in os.scandir(directory_path):
        if entry.is_file() and entry.name.lower().endswith('.pdf'):
            pdf_files_paths.append(entry.path)
    
    return pdf_files_paths

if __name__ =='__main__':
    files = get_files('june 2023')
    print(files)
    for file in  files:
        try:
             p = processfile(file)
             print(p)
             keywords_search(p)
        except Exception as e: print(e)  