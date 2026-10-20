import os
import csv
import unittest
from app.tests.test_base import BaseTestCase
from app.services.analyzer import analyze_firmware

class TestFirmwareAnalyzer(BaseTestCase):
    def test_analyze_firmware_creates_correct_csv_and_sorts(self):
        source_dir=os.path.join(self.app.config['UPLOAD_FOLDER'],"dummy_fw")
        os.makedirs(source_dir,exist_ok=True)
        
        file_a_path =os.path.join(source_dir,"file_a.txt")
        with open(file_a_path, "w") as f:
            f.write("<Tkn111AAAAATkn>\n<Tkn222BBBBBTkn>\n<Tkn111AAAAATkn>") 

        file_b_path=os.path.join(source_dir, "file_b.txt")
        with open(file_b_path,"w") as f:
            f.write("<Tkn111AAAAATkn>") 

        csv_output=os.path.join(self.app.config['CSV_OUTPUT_FOLDER'],"test_report.csv")
        global_stats=analyze_firmware(source_dir, csv_output)
        
        self.assertEqual(global_stats["<Tkn111AAAAATkn>"],3)
        self.assertEqual(global_stats["<Tkn222BBBBBTkn>"], 1)
        
        self.assertTrue(os.path.exists(csv_output))
        with open(csv_output,'r',newline='',encoding='utf-8') as f:
            reader= list(csv.DictReader(f))
            self.assertEqual(len(reader), 3)
            
            self.assertEqual(reader[0]['Path'],'file_a.txt')
            self.assertEqual(int(reader[0]['Occurrences']), 1)
            self.assertEqual(reader[0]['Token'],'<Tkn222BBBBBTkn>')

if __name__ == '__main__':
    unittest.main()
