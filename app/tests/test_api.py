import os
import requests
import time
import unittest

BASE_URL="http://127.0.0.1:8080"

class TestFirmwareExternalAPI(unittest.TestCase):
    def test_end_to_end_upload_pipeline(self):
        self.assertTrue(os.path.exists("firmware.zip"),"Error: firmware.zip is missing from your project root folder!")

        print("\n--- Sending firmware file ---")
        with open("firmware.zip", "rb") as f:
            response=requests.post(f"{BASE_URL}/analyze",files={"file": f})
        self.assertEqual(response.status_code,202,f"Expected 202 Accepted, got {response.status_code}")

        job_data=response.json()
        print("Server Response:",job_data)
        self.assertIn("job_id",job_data)
        job_id=job_data["job_id"]

        print("\n--- Polling for results ---")
        terminal_state_reached=False
        
        for i in range(15):
            status_response=requests.get(f"{BASE_URL}/results/{job_id}")
            self.assertEqual(status_response.status_code, 200)
            
            status_data=status_response.json()
            print(f"Poll #{i+1}: Status Data ->",status_data)
            
            if status_data.get("status") in ["completed", "failed"]:
                print(f"\nTask reached a terminal state: {status_data.get('status').upper()}")
                terminal_state_reached=True
                break
            time.sleep(1)

        self.assertTrue(terminal_state_reached,"The background job did not finish processing within 15 seconds.")

if __name__ == '__main__':
    unittest.main()
