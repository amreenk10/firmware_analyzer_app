import os
import unittest
from app.tests.test_base import BaseTestCase
from app.services.analyzer import analyze_firmware

class TestEmptyDirectory(BaseTestCase):
    def test_analyzer_handles_empty_directories(self):
        empty_dir=os.path.join(self.app.config['UPLOAD_FOLDER'],"empty_fw")
        os.makedirs(empty_dir, exist_ok=True)

        csv_output=os.path.join(self.app.config['CSV_OUTPUT_FOLDER'],"empty_report.csv")
        global_stats=analyze_firmware(empty_dir, csv_output)
        
        self.assertEqual(len(global_stats), 0)
        self.assertTrue(os.path.exists(csv_output))

if __name__ == '__main__':
    unittest.main()
