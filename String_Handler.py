import string, re

class StringHandler:
    def __init__(self):
        pass


    #remove punctuation marks
    def remove_punctuation(self,user_input_string):
        remove_punctuation = re.sub(r'[^\w\s]'," ",user_input_string)
        remove_space = remove_punctuation.split()
        return remove_punctuation

    #combine user input and record
    def combine_userinput_record(self,response,user_message):
        #pull out previous record
        previous_user_input = response["record"].values()

        combined_user_input_str = ""

        for val in previous_user_input:
            if val != None:
                combined_user_input_str = combined_user_input_str + " " +  val

        #add current user input
        combined_user_input_str = combined_user_input_str + " " +  user_message

        return combined_user_input_str
