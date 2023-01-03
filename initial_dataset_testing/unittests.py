import unittest
from os import path
import os.path
import pandas as pd

class TestInitialData(unittest.TestCase):
    # navigate to the directory where the data is stored and convert to dataframe
    p = "./notebooks/toy_model/media_bias.csv"
    parent_dir = os.path.split(os.getcwd())[0]
    assert path.exists(parent_dir + p), "media_bias.csv file does not exist"
    data = pd.read_csv(parent_dir + p)

    # test that the header columns are all present
    def test_data_headers(self):
        dataHeaders = ["","sentence","news_link","outlet","topic","type","group_id","num_sent","Label_bias","Label_opinion","article","biased_words4"]
        headers = list(self.data.columns.values)
        for i in range(1,12):
            self.assertEqual(headers[i], dataHeaders[i])

    # test that the data is the correct length
    def test_data_rows(self):
        self.assertEqual(len(self.data), 1700)
    
    # test that the sentence column has string in each row
    def test_sentence_column(self):
        for i in range(0,100):
            self.assertIsInstance(self.data['sentence'][i], str)

    # test that the outlet column has string in each row
    def test_outlet_column(self):
        for i in range(0,100):
            self.assertIsInstance(self.data['outlet'][i], str)

    # test that the topic column has string in each row
    def test_topic_column(self):
        for i in range(0,100):
            self.assertIsInstance(self.data['topic'][i], str)
    
    # test that the type column has string in each row
    def test_type_column(self):
        for i in range(0,100):
            self.assertIsInstance(self.data['type'][i], str)

    # test that the article column has string in each row
    def test_article_column(self):
        for i in range(0,100):
            self.assertIsInstance(self.data['article'][i], str)
    
if __name__ == '__main__':
    unittest.main()