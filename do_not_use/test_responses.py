import unittest
import responses

class TestResponses(unittest.TestCase):
    def test_get_response(self):
        print("running test_on_message")

        #the result will be a dictionary {"response":,"record"}

        #Greeting
        result = responses.get_response("Hi")
        self.assertEqual(result["response"],"Hello there! How can I help you ?")

        #Ask dates
        result = responses.get_response("dates")
        self.assertEqual(result["response"],"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you")

        result = responses.get_response("DATES")
        self.assertEqual(result["response"],"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you")

        result = responses.get_response("Dates")
        self.assertEqual(result["response"],"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you")

        result = responses.get_response("Date")
        self.assertEqual(result["response"],"Hey ~ Please provide the date you have (YYYY-MM-DD) and zipcode (i.e. 98087).  I can try to find if there's earlier date for you")


        #Ask something is not relevant
        result = responses.get_response("ABC")
        self.assertEqual(result["response"],'Do you mind rephrasing that? How can I help you?')



if __name__ == '__main__':
    unittest.main()
