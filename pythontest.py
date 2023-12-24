str= "update me with earlier dates"

def find_substr(str):
    if "dates" in str:
        return "yes, you find it"
    else:
        return "i can't find it"



print(find_substr(str))
