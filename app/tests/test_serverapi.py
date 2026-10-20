import io
import zipfile
import time
import unittest
from app.tests.test_base import BaseTestCase

class TestServerAPI(BaseTestCase):
    def test_async_upload_and_polling_lifecycle(self):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("firmware.bin", "Testing tokens: <Tkn777XXXXXTkn> <Tkn777XXXXXTkn>")
        zip_buffer.seek(0)

        response = self.client.post(
            '/analyze',
            data={'file': (zip_buffer, 'firmware.zip')},
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 202)
        data = response.get_json()
        self.assertIn("job_id", data)
        
    
        poll_url = data["poll_url"]
        status_data = {}
        
        for _ in range(20):
            poll_response = self.client.get(poll_url)
            self.assertEqual(poll_response.status_code, 200)
            status_data = poll_response.get_json()
            if status_data.get("status") in ["completed", "failed"]:
                break
            time.sleep(0.1)
        self.assertEqual(status_data.get("status"), "completed")
        self.assertEqual(status_data["results"].get("<Tkn777XXXXXTkn>"), 2)
