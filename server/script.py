import fitz
import re
import random
import colorsys
import glob
import zipfile
import os
from getkeywords import read_google_sheet_column
import PyPDF2

colors = [
        (0,1,0),
        (0,0,1),
        (1,1,0),
        (0,1,1),
        (1,0,1),
        (0,128/255,128/255),
        (1,99/255,71/255),
        (173/255,1,47/255),
        (0,250/255,154/255),
        (32/255,178/255,170/255),
        (0,206/255,209/255),
        (147/255,112/255,219/255),
        (148/255,0,211/255),
        (1,228/255,196/255),
        (244/255,164/255,96/255),
        (176/255,196/255,222/255),
        (240/255,248/255,1)
    ]
# uzip files
def unzip_files_recursively(directory=".",path='/'):
    print('Checking for zip files in '+path)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".zip"):
                try:
                    zip_path = os.path.join(root, file)
                    with zipfile.ZipFile(zip_path, "r") as zip_ref:
                        zip_ref.extractall(root)
                    os.remove(zip_path)  # Remove the original zip file

                    # Recursively unzip files within the extracted zip
                    unzip_files_recursively(root,zip_path)
                except:pass 
    print('Done checking for zip files in '+path)               
# Get the current working directory
def get_files():
    # directory_path = os.getcwd()
    pdf_files_paths = glob.glob("**/*.pdf", recursive=True)
    
    return pdf_files_paths        

def add_highlight_annot(page, match, color):
    r,g,b = color
    highlight = page.add_highlight_annot(match)
    highlight.set_colors(stroke=[r,g,b])
    highlight.set_opacity(0.7)
    highlight.update()

def add_highlight_annot_nsf(page, match, word):
    x,y,z,zz = match

    if "(" in word:
        z -= 4
        x += 4
    highlight = page.add_highlight_annot((x,y,z,zz))
    highlight.set_colors(stroke=[1,0,0])
    highlight.update()


def generate_color(index):
     if index < len(colors)-1: return colors[index]
     while True:
        r, g, b = [random.uniform(0.2, 0.8) for _ in range(3)]  # generate random RGB values between 0.2 and 0.8
        color = (0, g, b)  # create the RGBA color tuple
        try:
            fitz.CheckColor(color)  # check that the color is valid
            hsv = colorsys.rgb_to_hsv(r, g, b)  # convert RGB to HSV color space
            if hsv[1] < 0.3 or hsv[2] > 0.7:  # check that the color is not too close to white or black
                raise ValueError
            return color  # return the color if it's valid
        except ValueError:
            pass
def read_keywords():
    with open("data/keywords.txt") as fp:
        lines = [l.strip() for l in fp.readlines() if l.strip()]
        keywords = []
        for line in lines:
            if len(line.split('-')) > 1:
                keywords.append([x.strip() for x in line.split("-")])
            else:
                keywords.append(line)
        return keywords       
def read_keyword(path):
    try:
        with open(path) as fp:
            lines = [l.strip() for l in fp.readlines() if l.strip()]
            keywords = []
            for line in lines:
                if len(line.split('-')) > 1:
                    keywords.append([x.strip() for x in line.split("-")])
                else:
                    keywords.append(line)
            return keywords 
    except:    
       return []

def keywords_search(file):
    pdffileobj=open(file,'rb')
    doc=PyPDF2.PdfReader(pdffileobj)
    text = ''
    for page in doc.pages:
        text +=page.extract_text()+" "

    print(text)
    keywords = read_google_sheet_column()
    matched = []
    for keyword in keywords:
        try:
            pattern = r"\b" + re.escape(str(keyword)) + r"\b"
            matches = re.findall(pattern, text, re.IGNORECASE)
            if len(matches) > 0:
                if keyword not in matched:
                    matched.append(keyword)
        except Exception as e: print(e)  
    directory_path = os.path.dirname(file)
    k_path = os.path.join(directory_path,'keywords.txt')
    if os.path.exists(k_path):
        os.remove(k_path)
    with open(k_path,'a') as fl:
        fl.write('\n'.join(matched))    
   
    # for page in doc:
    #     for match in matched:
    #         words = page.search_for(match.strip(), ignorecase=True)   
    #         for word in words:
    #             color = colors[3]
    #             points = list(word)
    #             points[0] = points[0]-12
    #             points[2] = points[2]+12
             
    #             text_in_rect = page.get_textbox(tuple(points))
    #             pattern = r"\b" + re.escape(match.strip()) + r"\b"
    #             found = re.findall(pattern, text_in_rect, re.IGNORECASE)
    #             if len(found) > 0:
    #                 add_highlight_annot(page, word, color) 
   
    # doc.saveIncr()
    # doc.close()                
         
    # RuntimeError: Can't do incremental writes on a repaired file    
    # 5.10 Normal\05-02-2023\BUDD LAKE DINER\NEW MID Statement-534701850101809-04-2023.pdf    
            
image_files = []
def processfile(file_name):
        doc = fitz.open(file_name)
        print('processing '+file_name.split("/")[-1])
        pdffileobj=open(file_name,'rb')
        pdfreader=PyPDF2.PdfReader(pdffileobj)
        # Iterate through all the pages
        duplicates = {}
        for page in pdfreader.pages:
            # Get the text on the page
            text = page.extract_text()

            # Find all the matches for the pattern
            pattern = r"\-?\ ?\$?-?[\d,]+\.\d{2}\-?"
            # pattern = r"\-?\$?-?[\d,]+\.\d{2}"
            text_matches = re.findall(pattern, text)
            # find the duplicates
            for token in text_matches:
                amount = token.replace('$','').replace(',','').replace(' ','').replace('-','').strip()
                
                if amount in duplicates:
                    duplicates[amount][0] +=1
                    if token not in duplicates[amount]:
                        duplicates[amount].append(token)
                else:
                    duplicates[amount] = [1,token]  
        duplicates_list = [value[1:] for key, value in duplicates.items() if (value[0] > 2 and (float(key) >= 50 and float(key) <= 50000)) or (float(key)==36 or float(key)==35)] 
        # Highlight the duplicate matches
        for index, words in enumerate(duplicates_list):
            # break
            color = generate_color(index)
            wrds = []
            for word in words:
                if word in wrds:
                    continue
                val = token.replace('$','').replace(',','').replace(' ','').replace('-','').strip()
                if(float(val)==35 or float(val)==36):
                    color = (1,0,0)
                for page in doc:
                    search = " "+word+" "
                    if '-' in word[-1]:
                        search = " "+word.replace('-', '')
                    matches = page.search_for(search)
                    if len(matches) == 0:
                        matches = page.search_for(" ".join(search)) 
                    for match in matches:
                        points = list(match)
                        print(points[2] - points[0])
                        if points[2] - points[0] < 6:
                            continue
                        else:
                            points[0] = 0
                            points[2] = page.rect.width
                            add_highlight_annot(page, tuple(points), color)
                            # add_highlight_annot(page, match, color)
                        # points = [list(inner_tuple) for inner_tuple in match]
                        # if points[1][0] - points[0][0] < 6:
                        #     continue
                        # else:
                        #     add_highlight_annot(page, match, color)
                            
                    wrds.append(word)        
        # Highlight the nsf  
        # for page in doc: 
        #     # break                
        #     nsf = page.search_for('nsf:', ignorecase=True)
        #     nsf2 = page.search_for('(nsf)',ignorecase=True)
                        
        #     for match in nsf:
        #         add_highlight_annot_nsf(page, match,'nsf:')

        #     for match in nsf2:
        #         add_highlight_annot_nsf(page, match,'(nsf)') 

        # Save the modified PDF file

        processed_folder = os.path.join(os.path.dirname(file_name), 'processed')
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        processed_file_path = os.path.join(processed_folder, os.path.basename(file_name))
        
       
        doc.save(processed_file_path)
        doc.close()
        return processed_file_path
        
        
                
    


# if __name__ =='__main__':
#      # Search for PDF files in Google Drive
#     # unzip_files_recursively()
#     data = get_files()
#     if data is not None:
#         failed = []
#         for file in data:
#             try:
#                 processfile(file)
#                 keywords_search(file) 
#             except Exception as e:
#               print(e) 
#               failed.append(file)
             
               
#         print(str(len(data))+" pdf files processed")
#         print(str(len(failed))+" pdf files failed to processed")
#     else:
#         print("No files found")   

#     # with open('pdf_files_paths.txt', 'w') as file:
#     #     for path in pdf_files_paths:
#     #         file.write(path + '\n')    