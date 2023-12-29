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


https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/516!56b48e272ba45819d81868f440fb30eb6c406b705436cf1d101d2ea2c75c/times?date=2023-12-27&services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=867712719559.5795



https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/516!56b48e272ba45819d81868f440fb30eb6c406b705436cf1d101d2ea2c75c/dates?services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=1549662125918.2773
https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/516!56b48e272ba45819d81868f440fb30eb6c406b705436cf1d101d2ea2c75c/dates?services[]=DL!b94ae07d48f4d0cff89b6fc0e0c9aea5fa2a47d11728311b7adccdef2c728&numberOfCustomers=1&ver=977125805110.5748
