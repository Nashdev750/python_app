import cv2
import pytesseract
import os
import fitz
import re
import random
import colorsys
from messages import send_message
from getkeywords import read_google_sheet_column

colors = [
        (0,255,0),
        (0,0,255),
        (255,255,0),
        (0,255,255),
        (255,0,255),
        (0,128,128),
        (255,99,71),
        (173,255,47),
        (0,250,154),
        (32,178,170),
        (0,206,209),
        (147,112,219),
        (148,0,211),
        (255,228,196),
        (244,164,96),
        (176,196,222),
        (240,248,255)
    ]


def convert_images_to_pdf(image_paths, output_pdf_name='pages.pdf'):
   
    send_message("Merging images to pdf")
    # Extract the directory path from one of the image paths
    directory = os.path.dirname(image_paths[0])
    outp = os.path.join(directory,'processed')
    if not os.path.exists(outp):
        os.makedirs(outp)

    # Combine the directory path with the desired PDF file name
    output_pdf_path = os.path.join(outp, output_pdf_name)

    doc = fitz.open()

    for i,image_path in enumerate(image_paths):
        send_message("Merging image "+str(i+1)+" out of "+str(len(image_paths)))
        img = fitz.open(image_path)
        rect = img[0].rect
        pdf_bytes = img.convert_to_pdf()
        img.close()

        pdf_img = fitz.open("pdf", pdf_bytes)
        page = doc.new_page(width=rect.width, height=rect.height)
        page.show_pdf_page(rect, pdf_img, 0)
        pdf_img.close()

    doc.save(output_pdf_path)
    doc.close()
    send_message("end")
    send_message("Done!... fetching processed file...")

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

def getDup(text_matches):
    duplicates = {}
    for token in text_matches:
                amount = token.replace('$','').replace(',','').replace(' ','').strip()
                if '-' in amount:
                    amount = amount.replace('-','')
                    # amount = '-'+amount
                if amount in duplicates:
                    duplicates[amount][0] +=1
                    duplicates[amount].append(token)
                    if token not in duplicates[amount]:
                        duplicates[amount].append(token)
                else:
                    duplicates[amount] = [1,token]  
    duplicates_list = [value[1:] for key, value in duplicates.items() if value[0] > 1 and (float(key) >= 26 and float(key) <= 20000)] 
    flattened_list = [item[0].strip() for item in duplicates_list]
   
    return flattened_list

def convert_pdf_to_images(pdf_path):
    send_message("start")
    send_message("Extracting images from pdf")
    output_folder = os.path.dirname(pdf_path)
    doc = fitz.open(pdf_path)
    dpi = 50
    for i, page in enumerate(doc):
        
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72), alpha=False)
        image_path = os.path.join(output_folder, f"page{i + 1}.png")
        pix.save(image_path)
        send_message("page "+str(i))

    # Close the PDF file
    doc.close()
    send_message("Done!")

def search_keywords(directry, text):
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
    directory_path = os.path.dirname(directry)
    p_path = os.path.join(directory_path,'processed')
    if not os.path.exists(p_path):
        os.makedirs(p_path)
    k_path = os.path.join(p_path,'keywords.txt')
    if os.path.exists(k_path):
        os.remove(k_path)
    with open(k_path,'a') as fl:
        fl.write('\n'.join(matched))      


def process_image(imgs,colors={}, index = 0, text=''):
    
    if index >= len(imgs)-1:
       search_keywords(imgs[0],text)
       return  
    image_path = imgs[index]
    image = cv2.imread(image_path)
    highlighted_image = None
    send_message("Reading text on page "+str(index+1))
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    extracted_text = ' '.join([word.lower() for word in data['text']])
    text = text+extracted_text
  
    pattern = r"\-?\ ?\$?-?[\d,]+\.\d{2}\-?"
    keywords = re.findall(pattern, extracted_text)
    keywords = getDup(keywords)  
 
    
    for k, highlight_phrase in enumerate(keywords):
        h_color = None
        if highlight_phrase not in colors:
             h_color = generate_color(k)
             colors[highlight_phrase] = h_color
        else:
            h_color = colors[highlight_phrase]   
        for indx, word in enumerate(data['text']):
            if highlight_phrase.strip() != word.strip(): continue
            else:
                send_message("highlighting "+word)
                # # Find the bounding box of the phrase
                x = data["left"][indx]
                y = data["top"][indx]
                w = image.shape[1]
                # w = data["width"][indx]
                h = data["height"][indx]
                overlay = image.copy()
                cv2.rectangle(overlay, (0, y), (w, y+h), h_color, -1)

                # Apply the overlay on the original image
                alpha = 0.5  # Adjust the transparency of the overlay
                highlighted_image = cv2.addWeighted(overlay, alpha, image, 1-alpha, 0)

                    
                # Save the image with highlighted phrase
                cv2.imwrite(image_path, highlighted_image)
                image = cv2.imread(image_path)
    index = index + 1
    return process_image(imgs,colors, index, text) 



