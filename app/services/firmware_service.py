import os
import uuid
import zipfile
import tarfile
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor
from app.config import Config

class FirmwareService:
    def __init__(self):
        self._executor=ThreadPoolExecutor(max_workers=Config.CONCURRENCY)
        self._jobs = {}

    def create_job(self)-> str:
        job_id = str(uuid.uuid4())
        self._jobs[job_id]={"status": "processing", "results": {}}
        return job_id

    def get_job_status(self,job_id:str)->dict:
        return self._jobs.get(job_id)

    def start_analysis_async(self,job_id:str,zip_path:str,upload_folder: str,csv_folder:str):
        self._executor.submit(
            self._background_worker,
            job_id,
            zip_path,
            upload_folder,
            csv_folder
        )

    def _background_worker(self, job_id: str, zip_path: str,upload_folder:str,csv_folder:str):
        from .analyzer import analyze_firmware

        extract_dir = os.path.join(upload_folder,f"extracted_{job_id}")
        csv_output_path = os.path.join(csv_folder,f"report_{job_id}.csv")
        try:
            if not os.path.exists(zip_path):
                raise FileNotFoundError(f"Uploaded archive not found at: {zip_path}")

            if zipfile.is_zipfile(zip_path):
                with zipfile.ZipFile(zip_path,'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
            elif tarfile.is_tarfile(zip_path):
                with tarfile.open(zip_path,'r:*') as tar_ref:
                    tar_ref.extractall(extract_dir)
                
            else:
                raise ValueError("Unsupported archive format. Please provide a valid .zip or .tar archive.")
        
            global_stats=analyze_firmware(extract_dir, csv_output_path)
        
            self._jobs[job_id]={
                "status": "completed",
                "results": global_stats
            }
        except Exception as e:
            print(f"[ERROR] Background worker failed for job {job_id}:")
            traceback.print_exc()
            self._jobs[job_id]={
                "status": "failed",
                "error": str(e)
            }
        finally:
            self._cleanup_files(zip_path, extract_dir)

    def _cleanup_files(self, zip_path: str, extract_dir: str):
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)



firmware_service = FirmwareService()

