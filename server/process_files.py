import os
from script import processfile, keywords_search


def get_files(folder_name):
    directory_path = os.path.join(os.getcwd(), folder_name)
    pdf_files_paths = []
    for entry in os.scandir(directory_path):
        if entry.is_file() and entry.name.lower().endswith('.pdf'):
            pdf_files_paths.append(entry.path)
    
    return pdf_files_paths
def process_file(folder):
    files = get_files(folder)
    for file in  files:
        try:
             p = processfile(file)
             keywords_search(p)
        except: pass    