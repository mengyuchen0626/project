import unittest 
import requests 
import time 
import os 

class FlaskTests(unittest.TestCase): 
    
    def setUp(self):
        os.environ['NO_PROXY'] = '0.0.0.0'
        pass
    
    def tearDown(self): 
        pass
    
    def test_index(self):
        params = {
            'text':u'it is great'
        }
        
        count = 1000
        since = time.time()
        
        for i in range(count):
            responce = requests.post('http://localhost:5000',data=params)
            self.assertEqual(responce.status_code,200) 
        
        spend = time.time()-since      
                     
        print("Requests number: ",count) 
        print("Time use: ",spend," seconds") 
            
if __name__ == '__main__':
    unittest.main()