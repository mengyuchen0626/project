import unittest
import os
import requests

class FlaskTests(unittest.TestCase):
    def setUp(self):
        os.environ['NO_PROXY'] = '0.0.0.0'
        self.text=""
        pass
    
    def tearDown(self):
        pass

    def test_1_index(self):
        responce = requests.get('http://localhost:5000')
        self.assertEqual(responce.status_code,200)
   
    def test_2_text(self):
        params = {
            'text':u'it is great'
        }
        responce = requests.post('http://localhost:5000',data=params)
        self.assertEqual(responce.status_code,200)

    def test_3_text(self):
        params = {
            'text':u'hello'
        }
        responce = requests.post('http://localhost:5000',data=params)
        self.assertEqual(responce.status_code,200)

if __name__ == '__main__':
    unittest.main()

    