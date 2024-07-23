import datetime
from datetime import datetime

class ValidationHandler:
    def __init__(self):
        pass

    #check if the word can be changed to number
    def check_convert_into_num(self,word):
        res = False
        try:
            int(word)
            res =  True
        except:
            return res
        return res

    #check if the length of zipcode is correct
    def check_length_zipcode_input_validtion(self,word):
        if len(word) == 5:
            return True
        return False

    #check if datetime formate
    def check_datetime_formate_validation(self,word):
        try:
            date_obj = datetime.strptime(word, "%Y%m%d")
            return date_obj
        except:
            return False

    def find_mile_range(self,user_input):
        mile_range = False
        for word in user_input:
            #check if mile in word
            if "mile" in word and not word.startswith("m"):
                mile_range = word[0:word.find("mile")]
                break

            elif "mile" in word and word.startswith("m"):
                mile_range = user_input[user_input.index(word)-1]
                break


        return mile_range
