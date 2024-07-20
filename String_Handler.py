import string, re

class StringHandler:
    def __init__(self):
        pass


    #remove punctuation marks
    def remove_punctuation(self,user_input_string):
        print("移除標點符號: ",user_input_string)
        translator = str.maketrans('', '', string.punctuation)
        result = user_input_string.translate(translator)
        return result

    def extract_date_and_zipcode(self,user_input_string):
        remove_punctuation = re.sub(r'[^\w\s]'," ",user_input_string)
        print("移除其他標點符號： ",remove_punctuation)
        remove_space = remove_punctuation.split()
        return remove_space

    def lower_words(self,user_input_list):
        return [word.lower() for word in user_input_list]
        

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
