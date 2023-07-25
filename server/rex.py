import re

text = "Sample text with numbers like 100.00, $4,566.45, 3 9 . 0 0, and - $23, 909. 78. +5 . 0 0"

# Create a regular expression to match all numbers in the string
regex = r"(([$-+])?([\d][,\][ ]?)+([.])(( )?[\d]( )?){2})"


# Find all matches of the regular expression in the string
matches = re.findall(regex, text)
flattened_result = [match[0].replace(' ','') for match in matches]
# Print the matches
print(flattened_result)