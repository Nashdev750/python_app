import os
from ai import process_image, convert_images_to_pdf, convert_pdf_to_images
import sys
from messages import send_message


def get_files(folder_name,ext):
    directory_path = os.path.join(os.getcwd(), folder_name)
    pdf_files_paths = []
    for entry in os.scandir(directory_path):
        if entry.is_file() and entry.name.lower().endswith(ext):
            pdf_files_paths.append(entry.path)

    return pdf_files_paths
def process_file(folder):
    files = get_files(folder,'.pdf')
    print(files)
    if len(files) < 1: return
    convert_pdf_to_images(files[0])  
    images = get_files(folder,'.png')
    send_message("Starting image highlight, this might take a minute")
    process_image(images)
    convert_images_to_pdf(images)

# process_file('april/me')   
if __name__ == '__main__':
    folder = sys.argv[1]
    process_file(folder)