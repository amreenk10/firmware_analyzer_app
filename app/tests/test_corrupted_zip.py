import io
import time
import unittest
from app.tests.test_base import BaseTestCase

class TestCorruptedZip(BaseTestCase):
    def test_upload_corrupted_zip_fails_gracefully(self):
        corrupted_data =io.BytesIO(b"NOT_A_REAL_ZIP_FILE_MARKER_DATA")
        response =self.client.post(
            '/analyze',
            data={'file': (corrupted_data, 'broken.zip')},
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 202)
        job_id=response.get_json()["job_id"]
        status_data={}
        for _ in range(10):
            status_data=self.client.get(f"/results/{job_id}").get_json()
            if status_data.get("status")=="failed":
                break
            time.sleep(0.1)

        self.assertEqual(status_data["status"],"failed")
        self.assertIn("error",status_data)

if __name__ == '__main__':
    unittest.main()
