# import PyPDF2
# import re


# def repair():
#      pdffileobj=open('DEC7259.pdf','rb')
#      pdfreader=PyPDF2.PdfReader(pdffileobj)
#      pdf_writer = PyPDF2.PdfWriter()
#      for page in pdfreader.pages:
#           pdf_writer.add_page(page)
#      with open('DEC72592.pdf', "wb") as output_file:
#           pdf_writer.write(output_file)

# def test():
#         pdffileobj=open('DEC72592.pdf','rb')
#         pdfreader=PyPDF2.PdfReader(pdffileobj)
#         # Iterate through all the pages
#         duplicates = {}
#         text = ''
#         print(pdfreader.pages[1].extract_text())

#         for page in pdfreader.pages:
#             try:
#                 if page:
#                     text += page.extract_text()
#                     print(text)
#             except Exception as e:
#                  print(e)
#                  pass     
#             # Get the text on the page
            
#         text = re.sub(r'\s+', ' ', text)    
#         search_term = "Businessbacker"
    
#         # Create a pattern with optional spaces between letters
#         pattern = r"\b{}\b".format(r"\s?".join(list(search_term)))
    
#         # Search for the pattern in the text
#         matches = re.findall(pattern, text, re.IGNORECASE)  
#         print(matches)
#         with open('txt.txt', 'w') as fl:
#               fl.write(text)

# test()              


# # repair()
import fitz
doc = fitz.open('DEC7259.pdf')
for page in doc:
      # Get the text on the page
      text = page.get_text()
      print(text)