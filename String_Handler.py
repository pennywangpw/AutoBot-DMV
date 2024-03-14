import string

class StringHandler:
    def __init__(self):
        pass


    #remove punctuation marks
    def remove_punctuation(self,user_input_string):
        translator = str.maketrans('', '', string.punctuation)
        result = user_input_string.translate(translator)
        return result

    #combine user input and record
    def combine_userinput_record(self,response,user_message):
        #pull out previous record
        previous_user_input = response["record"].values()
        print("pull out previous record: ", previous_user_input)

        combined_user_input_str = ""

        for val in previous_user_input:
            if val != None:
                combined_user_input_str = combined_user_input_str + " " +  val

        #add current user input
        combined_user_input_str = combined_user_input_str + " " +  user_message

        print("整理好的combined_user_input_str: ",combined_user_input_str)
        return combined_user_input_str
