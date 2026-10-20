import os
import shutil
import unittest
from app import create_app
from app.services.firmware_service import firmware_service

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app()
        self.app.config['TESTING']=True
        self.app.config['UPLOAD_FOLDER']=os.path.abspath("./tmp/test_uploads")
        self.app.config['CSV_OUTPUT_FOLDER']=os.path.abspath("./tmp/test_reports")
        self.client = self.app.test_client()
        
        self._clean_dirs()
        os.makedirs(self.app.config['UPLOAD_FOLDER'],exist_ok=True)
        os.makedirs(self.app.config['CSV_OUTPUT_FOLDER'],exist_ok=True)

    def tearDown(self):
        self._clean_dirs()
        firmware_service._jobs={}

    def _clean_dirs(self):
        for folder in ['UPLOAD_FOLDER','CSV_OUTPUT_FOLDER']:
            path=self.app.config.get(folder)
            if path and os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
