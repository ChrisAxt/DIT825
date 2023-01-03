from django.test import TestCase
import unittest

from .utils import * 

class UserInputTestCase(unittest.TestCase):
    def setUp(self):
        self.testInput = "This is my test string. What do you think of it? I think it's awesome! This is a string without a sentence ending char"
        self.sentenceList = extractSentences(self.testInput)
        self.model_name = "projects/dit825/models/simple_model/versions/simple_model_1672423164"

    def test_extractSentences_period(self):
        self.assertEqual(self.sentenceList[0], "This is my test string." ,"Failed to extract sentence ending in period")
        
    def test_extractSentences_question(self):
        self.assertEqual(self.sentenceList[1], "What do you think of it?" ,"Failed to extract sentence ending in question mark")

    def test_extractSentences_exclamation(self):
        self.assertEqual(self.sentenceList[2], "I think it's awesome!" ,"Failed to extract sentence ending in exclamation mark")

    def test_extractSentences_none(self):
        self.assertEqual(self.sentenceList[3], "This is a string without a sentence ending char" ,"Failed to extract sentence ending without a sentence ending char")

    def test_sendRequest(self):
        predictionList = sendRequest(self.sentenceList, self.model_name)
        self.assertEqual(len(self.sentenceList),  len(predictionList), "Failed to send the request to the model")

    
if __name__ == '__main__':
    unittest.main()