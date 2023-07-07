import os
from script import processfile, keywords_search
import fitz

def is_image_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    is_image = True

    for page in doc:
        if page.get_text("text") != "":
            is_image = False
            break

    doc.close()

    return is_image


def get_files(folder_name):
    directory_path = os.path.join(os.getcwd(), folder_name)
    pdf_files_paths = []
    for entry in os.scandir(directory_path):
        if entry.is_file() and entry.name.lower().endswith('.pdf'):
            pdf_files_paths.append(entry.path)
    
    return pdf_files_paths
def process_pdf_file(folder):
    files = get_files(folder)
    if len(files) < 1: return False
    isimg = is_image_pdf(files[0])
    print(files)
    if isimg: return True
    for file in  files:
        try:
             p = processfile(file)
             keywords_search(p)
        except: pass    
    return False