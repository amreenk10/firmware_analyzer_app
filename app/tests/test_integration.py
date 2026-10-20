import os
import io
import time
import zipfile
import threading
import requests
import unittest
from app import create_app
from app.services.firmware_service import firmware_service

class TestFirmwareEndToEndIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['UPLOAD_FOLDER'] = os.path.abspath("./tmp/integration_uploads")
        cls.app.config['CSV_OUTPUT_FOLDER'] = os.path.abspath("./tmp/integration_reports")
        
        cls.host = "127.0.0.1"
        cls.port = 8585
        cls.base_url = f"http://{cls.host}:{cls.port}"
        cls.server_thread = threading.Thread(
            target=lambda: cls.app.run(host=cls.host, port=cls.port, debug=False, use_reloader=False),
            daemon=True
        )
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        firmware_service._jobs = {}

    def test_complete_uploaded_firmware_lifecycle(self):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("core/kernel.bin", "Auth sequence initiated: <Tkn999ABCDEtkn> match: <Tkn123PATCHTkn>")
            zip_file.writestr("drivers/net.cfg", "System token config: <Tkn123PATCHTkn>")
        zip_buffer.seek(0)

        payload = {'file': ('firmware.zip', zip_buffer, 'application/zip')}
        response = requests.post(f"{self.base_url}/analyze", files=payload)
        
        self.assertEqual(response.status_code, 202)
        job_data = response.json()
        self.assertIn("job_id", job_data)
        self.assertIn("poll_url", job_data)
        
        job_id = job_data["job_id"]
        terminal_state_reached = False
        status_data = {}
        
        for _ in range(15):
            status_response = requests.get(f"{self.base_url}/results/{job_id}")
            self.assertEqual(status_response.status_code, 200)
            status_data = status_response.json()
            
            if status_data.get("status") in ["completed", "failed"]:
                terminal_state_reached = True
                break
            time.sleep(0.2)

        self.assertTrue(terminal_state_reached, "The integration task timed out.")
        self.assertEqual(status_data.get("status"), "completed")
  
        results = status_data.get("results", {})
        self.assertEqual(results.get("<Tkn123PATCHTkn>"), 2)
        self.assertNotIn("<Tkn999ABCDEtkn>", results, "Lowercase tokens must be ignored.")

if __name__ == '__main__':
    unittest.main()
