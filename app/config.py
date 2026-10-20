import os

class Config:
    CONCURRENCY = int(os.environ.get("CONCURRENCY", 4))
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.abspath("./tmp/firmware_uploads"))
    CSV_OUTPUT_FOLDER = os.environ.get("CSV_OUTPUT_FOLDER", os.path.abspath("./tmp/firmware_reports"))

