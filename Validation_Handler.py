import datetime
from datetime import datetime

class ValidationHandler:
    def __init__(self):
        pass

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
