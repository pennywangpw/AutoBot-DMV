import datetime
from datetime import datetime

class ValidationHandler:
    def __init__(self):
        pass

    #check if the length of zipcode is correct
    def length_zipcode_input_validtion(self,zipcode):
        if len(zipcode) == 5:
            return True
        return False

    #date and zipcode input validation
    def date_zipcode_input_validation(self,input_date,input_zipcode):
        if not isinstance(input_date,str):

            return "The input_date should be a string type with YYYY-MM-DD"
        elif not isinstance(input_zipcode, int):

            return "Invalid zipcode"
        else:
            try:
                date_obj = datetime.strptime(input_date, "%Y-%m-%d")

            except ValueError as e:
                return e


    # V2 - date and zipcode input validation
    def date_zipcode_input_validation_V2(self,user_input):
        print(f"傳入function user_input list  {user_input} {type(user_input)}")

        if_date = False
        if_zipcode = False
        for word in user_input:
            print(f"每一個在user input裡面的word {word}")
            try:
                date_obj = datetime.strptime(word, "%Y%m%d")
                if_date = True
                print(f"可以改成date唷! {date_obj}")
                print("--------------------")
                continue
            except:
                try:
                    print(f"被檢查的string {word}")
                    #make sure word is number and if it's valid zipcode
                    int(word)
                    if self.length_zipcode_input_validtion(word):
                        if_zipcode = True
                        continue
                    else:
                        return "Zipcode should be 5 digits"
                except ValueError as e:
                    return "This is invalid input.\nPlease provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087)"

        if if_date == True and if_zipcode == True:
            return "pass"
        else:
            return "Sorry. This is invalid input.\nPlease provide the date you have (YYYY-MM-DD) AND zipcode (i.e. 98087)"
