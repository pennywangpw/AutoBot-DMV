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
            print("here is check_datetime_formate_validation datetime: ",date_obj, type(date_obj))
            return date_obj
        except:
            return False

    # #date and zipcode input validation
    # def date_zipcode_input_validation(self,input_date,input_zipcode):
    #     if not isinstance(input_date,str):

    #         return "The input_date should be a string type with YYYY-MM-DD"
    #     elif not isinstance(input_zipcode, int):

    #         return "Invalid zipcode"
    #     else:
    #         try:
    #             date_obj = datetime.strptime(input_date, "%Y-%m-%d")

    #         except ValueError as e:
    #             return e

    # #return datetime and zipcode 
    # def check_zipcode_datetime_provided_and_valid(self,user_input):
    #     print("確認是否有zipcode and datetime")
    #     input_zipcode= None
    #     input_datetime= None
    #     for word in user_input:
    #         if self.check_length_zipcode_input_validtion(word):
    #             input_zipcode = int(word)
    #         else:
    #             datetime_obj = self.check_datetime_formate_validation(word)
    #             print("i don't understand what i get datetime_obj: ",datetime_obj)
    #             if datetime_obj is not None:
    #                 input_datetime = datetime_obj

    #     if input_zipcode != None and input_datetime != None:
    #         print(input_zipcode,input_datetime,type(input_zipcode),type(input_datetime))
    #         return input_zipcode,input_datetime




    def find_mile_range(self,user_input):
        mile_range = False
        for word in user_input:
            print("user intput word: ",word)
            #check if mile in word
            if "mile" in word and not word.startswith("m"):
                mile_range = word[0:word.find("mile")]
                break

            elif "mile" in word and word.startswith("m"):
                print("word word.find()): ",word, word.find("mile"))
                mile_range = user_input[user_input.index(word)-1]
                break


        return mile_range
