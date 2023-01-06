import unittest
from os import path
import os.path
import pandas as pd

class TestInitialData(unittest.TestCase):
    # navigate to the directory where the data is stored and convert to dataframe
    p = "app/assets/media_bias_dataset_cleaned.csv"
    assert path.exists(p), "media_bias_cleaned.csv file does not exist"
    data = pd.read_csv(p)

    # test that the header columns are all present
    def test_data_headers(self):
        dataHeaders = ["sentence","news_link","outlet","topic","type", "label","Label_opinion","article","biased_words"]
        headers = list(self.data.columns.values)
        for i in range(len(dataHeaders)):
            self.assertEqual(headers[i], dataHeaders[i])

    # test that each sentence is unique
    def test_unique_sentences(self):
        self.assertEqual(len(self.data['sentence'].unique()), len(self.data['sentence']))
    
    # test that the sentence column has string in each row
    def test_sentence_column(self):
        for i in range(len(self.data['sentence'])):
            self.assertIsInstance(self.data['sentence'][i], str)

    # test that the outlet column has string in each row
    def test_outlet_column(self):
        for i in range(len(self.data['sentence'])):
            self.assertIsInstance(self.data['outlet'][i], str)
    
    # test that the topic column has string in each row
    def test_topic_column(self):
        for i in range(len(self.data['sentence'])):
            self.assertIsInstance(self.data['topic'][i], str)

    # test that there are no null values in the sentence column
    def test_sentence_null(self):
        self.assertFalse(self.data['sentence'].isnull().values.any())

    # test that the label_bias column has 'Biased', 'Non-biased', or 'No Agreement' in each row
    def test_label_bias_column(self):
        for i in range(len(self.data['sentence'])):
            self.assertIn(self.data['label'][i], ['Biased', 'Non-biased', 'No agreement'])
    

class TestPseudoLabelledData(unittest.TestCase):
    p = "app/assets/pseudo_labelled.csv"
    parent_dir = os.path.split(os.getcwd())[0]
    assert path.exists(p), "media_bias.csv file does not exist"
    data = pd.read_csv(p)

    # test that the header columns are all present
    def test_data_headers(self):
        dataHeaders = ["sentence", "pub_year", "news_link", "outlet", "pred", "label"]
        headers = list(self.data.columns.values)
        for i in range(len(dataHeaders)):
            self.assertEqual(headers[i], dataHeaders[i])
            
    # print sentence that isn't unique
    def test_unique_sentences_print(self):
        for i in range(len(self.data['sentence'])):
            if self.data['sentence'][i] in self.data['sentence'][:i]:
                print(self.data['sentence'][i])
        
    # test that the sentence column has string in each row
    def test_sentence_column(self):
        for i in range(len(self.data['sentence'])):
            self.assertIsInstance(self.data['sentence'][i], str)
    
    # test that the label is 0 or 1
    def test_label_column(self):
        for i in range(len(self.data['sentence'])):
            self.assertIn(self.data['label'][i], [0, 1])
    

if __name__ == '__main__':
    unittest.main()