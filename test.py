import unittest
import pandas as pd
from main import *

df = pd.DataFrame()
class Testing(unittest.TestCase):
    
    
    def test_filepath(self):

        filepath_1 = 'wrong_filename.csv'
        result = csv_to_dataframe(filepath_1)
        self.assertIsNone(result)
    
    def test_developer(self):
        
        result = developer_dataframe(df)
        self.assertIsNone(result)
        
    def test_countrylist(self):
    
        result = generate_country_list(df)
        self.assertIsNone(result)
        
    def test_continentlist(self):
        countries = ['France','Germany','France']
        expected = ['France','Germany']
        test_dict = {'Europe':expected}
        
        result = continent_classification(countries)
        
        self.assertCountEqual(result,test_dict)
        
    def test_continentlist_empty(self):
        countries = []
        
        result = continent_classification(countries)
        
        self.assertFalse(result)
        
    def test_question_one(self):
        result = question_one(df)
        
        self.assertEqual(result,0)
        
    def test_question_two(self):
        result = question_two(df,[])
        
        self.assertIsNone(result)
        
    def test_question_three(self):
        result = question_two(df,[])
        
        self.assertIsNone(result)
        
    def test_question_four(self):
        result = question_two(df,[])
        
        self.assertIsNone(result)
        
    def test_question_five(self):
        result = question_two(df,[])
        
        self.assertIsNone(result)
        
    def test_question_six(self):
        result = question_two(df,[])
        
        self.assertIsNone(result)
        

if __name__ == '__main__':
    unittest.main()