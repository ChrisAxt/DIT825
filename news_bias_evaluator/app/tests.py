from django.test import TestCase, Client
import unittest

from .utils import * 

class UserInputTestCase(unittest.TestCase):
    def setUp(self):
        self.testInput = "This is my test string. What do you think of it? I think it's awesome! This is a string without a sentence ending char"
        self.sentenceList = extractSentences(self.testInput)

    def test_extractSentences_period(self):
        self.assertEqual(self.sentenceList[0], "This is my test string." ,"Failed to extract sentence ending in period")
        
    def test_extractSentences_question(self):
        self.assertEqual(self.sentenceList[1], "What do you think of it?" ,"Failed to extract sentence ending in question mark")

    def test_extractSentences_exclamation(self):
        self.assertEqual(self.sentenceList[2], "I think it's awesome!" ,"Failed to extract sentence ending in exclamation mark")

    def test_extractSentences_none(self):
        self.assertEqual(self.sentenceList[3], "This is a string without a sentence ending char" ,"Failed to extract sentence ending without a sentence ending char")

    #def test_sendRequest(self):
    #    predictionList = sendRequest(self.sentenceList)
    #    self.assertEqual(len(self.sentenceList),  len(predictionList['predictions']), "Failed to send the request to the model")


class Article_and_sentence_validation(TestCase):
    '''
    Test suite for the methods checking important attributes for Article and LabeledSentence 
    when created via import of CSV file. 
    '''

    def test_news_link_is_valid(self):
        news_link_test = "https://www.freecodecamp.org/news/python-lowercase-how-to-use-the-string-lower-function/"
        self.assertTrue(is_valid_news_link(news_link_test))

    def test_news_link_is__not_valid(self):
        news_link_test = "freecodecamp.org/news/python-lowercase-how-to-use-the-string-lower-function"
        self.assertFalse(is_valid_news_link(news_link_test))
    
    def test_sentence_is_not_empty_should_be_true(self):
        sentence_test = "This is a sentence!"
        self.assertTrue(is_non_empty_sentence(sentence_test))

    def test_sentence_is_empty_should_be_false(self):
        sentence_test = ""
        self.assertFalse(is_non_empty_sentence(sentence_test))

    def test_sentence_is_blank_should_be_false(self):
        sentence_test = "  "
        self.assertFalse(is_non_empty_sentence(sentence_test))

    def test_is_valid_label_bias_should_be_true(self):
        label_bias_test = "BIASED"
        self.assertTrue(is_valid_label_bias(label_bias_test))

    def test_is_valid_label_bias_should_be_true(self):
        label_bias_test = "non-BIASED"
        self.assertTrue(is_valid_label_bias(label_bias_test))
    
    def test_is_not_valid_label_bias_should_be_false(self):
        label_bias_test = "No agreement"
        self.assertFalse(is_valid_label_bias(label_bias_test))
    
    def test_is_empty_label_bias_should_be_false(self):
        label_bias_test = ""
        self.assertFalse(is_valid_label_bias(label_bias_test))
    
    def test_is_0_label_bias_should_be_true(self):
        label_bias_test = "0"
        self.assertTrue(is_valid_label_bias(label_bias_test))

    def test_is_1_label_bias_should_be_true(self):
        label_bias_test = "1"
        self.assertTrue(is_valid_label_bias(label_bias_test))

    def test_convert_label_bias_should_be_0(self):
        label_bias_test = "Non-biAsed"
        self.assertEqual(convert_label_bias(label_bias_test), '0')

    def test_convert_label_bias_should_be_1(self):
        label_bias_test = "BiaseD"
        self.assertEqual(convert_label_bias(label_bias_test), '1')

    def test_convert_label_bias_should_be_0(self):
        label_bias_test = "0"
        self.assertEqual(convert_label_bias(label_bias_test), '0')

    def test_convert_label_bias_should_be_1(self):
        label_bias_test = "1"
        self.assertEqual(convert_label_bias(label_bias_test), '1')
    
if __name__ == '__main__':
    unittest.main()