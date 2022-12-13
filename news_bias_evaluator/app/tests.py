from django.test import TestCase
import unittest

from .utils import * 

class UserInputTestCase(unittest.TestCase):
    def setUp(self):
        self.testInput = "This is my test string. What do you think of it? I think it's awesome!"
        self.sentenceList = extractSentences(self.testInput)

    def test_extractSentences_period(self):
        self.assertEqual(self.sentenceList[0], "This is my test string." ,"Failed to extract sentence ending in period")
        
    def test_extractSentences_question(self):
        self.assertEqual(self.sentenceList[1], "What do you think of it?" ,"Failed to extract sentence ending in question mark")

    def test_extractSentences_exclamation(self):
        self.assertEqual(self.sentenceList[2], "I think it's awesome!" ,"Failed to extract sentence ending in exclamation mark")

    #def test_sendRequest(self):
    #    predictionList = sendRequest(self.sentenceList)
    #    self.assertEqual(len(self.sentenceList),  len(predictionList['predictions']), "Failed to send the request to the model")

    
if __name__ == '__main__':
    unittest.main()