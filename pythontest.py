# str= "update me with earlier dates"

# def find_substr(str):
#     if "dates" in str:
#         return "yes, you find it"
#     else:
#         return "i can't find it"



# print(find_substr(str))


import string

def remove_punctuation(input_string):
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result

# Sample string with punctuation marks and spaces
text = "Hello, world! This is a sample string with punctuation. And spaces!"

# Remove punctuation from the string
output = remove_punctuation(text)

# Print the original and modified strings
print("Original string:", text)
print("String without punctuation:", output)
