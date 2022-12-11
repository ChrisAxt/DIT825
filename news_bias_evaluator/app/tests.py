from django.test import TestCase
import unittest

# Create your tests here.
class TestMethods(unittest.TestCase):
    # placeholder test
    def test_article_column(self):
        for i in range(0,100):
            self.assertIsInstance('this is a string', str)
    
if __name__ == '__main__':
    unittest.main()