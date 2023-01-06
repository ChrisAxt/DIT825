from django.test import TestCase, Client
import pandas as pd
import unittest

from .retraining_utils import validator
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
class Retraining_pipeline_unit_tests(unittest.TestCase):
    '''
    Test suite for the methods relating to the dynamic retraining of the model.
    '''
    def setUp(self) -> None:
        test_data = [['YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.', 1, 'Somewhat factual but also opinionated', ['belated', 'birtherism'], 'https://eu.usatoday.com/story/tech/2020/02/03/youtube-google-wont-allow-deepfake-videos-2020-election-census/4648312002/', 'app/assets/media_bias_dataset.csv'], ['Another test scentence is here.', 1, 'Somewhat factual but also opinionated', ['belated', 'birtherism'], 'https://eu.usatoday.com/story/tech/2020/02/03/youtube-google-wont-allow-deepfake-videos-2020-election-census/4648312002/', 'app/assets/media_bias_dataset.csv'], [np.nan, 1, 'Somewhat factual but also opinionated', ['belated', 'birtherism'], 'https://eu.usatoday.com/story/tech/2020/02/03/youtube-google-wont-allow-deepfake-videos-2020-election-census/4648312002/', 'app/assets/media_bias_dataset.csv'], ['YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.', 'No agreement', 'Somewhat factual but also opinionated', ['belated', 'birtherism'], 'https://eu.usatoday.com/story/tech/2020/02/03/youtube-google-wont-allow-deepfake-videos-2020-election-census/4648312002/', 'app/assets/media_bias_dataset.csv'], ['YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.', 'Biased', 'Somewhat factual but also opinionated', ['belated', 'birtherism'], 'https://eu.usatoday.com/story/tech/2020/02/03/youtube-google-wont-allow-deepfake-videos-2020-election-census/4648312002/', 'app/assets/media_bias_dataset.csv'], ['YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.', 'Non-biased', 'Somewhat factual but also opinionated', ['belated', 'birtherism'], 'https://eu.usatoday.com/story/tech/2020/02/03/youtube-google-wont-allow-deepfake-videos-2020-election-census/4648312002/', 'app/assets/media_bias_dataset.csv']]
        columns = ['sentence', 'label_bias', 'label_opinion', 'bias_words', 'article_id', 'filename']
        self.testDataFrame = pd.DataFrame(test_data, columns=columns)

    def test_validator_cleans_data_correctly(self):
        correct_data = [['YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.', 1], ['Another test scentence is here.', 1], ['YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.', 1], ['YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.', 0]]
        correct_columns = ['sentence', 'Label_bias']
        correct_result = pd.DataFrame(correct_data, columns=correct_columns)
        cleaned = validator.prepare_data(self.testDataFrame)
        self.assertTrue(cleaned.reset_index(drop=True).equals(correct_result.reset_index(drop=True)))
    


    
if __name__ == '__main__':
    unittest.main()