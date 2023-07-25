import re
import fitz

doc = fitz.open('DEC7259.pdf')

text = ''
for page in doc:
    text+= page.get_text()
    
regex = r"(([$-+])?([\d][,\][ ]?)+([.])(( )?[\d]( )?){2})"


# Find all matches of the regular expression in the string
matches = re.findall(regex, text)
flattened_result = [match[0] for match in matches]
# Print the matches
print(flattened_result)
print(len(flattened_result))