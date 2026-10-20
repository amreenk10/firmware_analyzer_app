import os
from flask import Blueprint, request, jsonify, current_app
from app.services.firmware_service import firmware_service

analyze_bp = Blueprint('analyze',__name__)

@analyze_bp.route('/analyze',methods=['POST'])
def upload_firmware():
    if 'file' not in request.files:
        return jsonify({"error":"No file part in the request payload"}),400

    file=request.files['file']
    if file.filename=="":
        return jsonify({"error":"No file selected for upload"}),400

    upload_folder=current_app.config['UPLOAD_FOLDER']
    csv_folder=current_app.config['CSV_OUTPUT_FOLDER']

    os.makedirs(upload_folder,exist_ok=True)
    os.makedirs(csv_folder,exist_ok=True)

    job_id=firmware_service.create_job()
    zip_path=os.path.join(upload_folder,f"{job_id}.zip")
    file.save(zip_path)
    firmware_service.start_analysis_async(
        job_id,
        zip_path,
        upload_folder,
        csv_folder
    )
    return jsonify({
        "message":"firmware analysis successfully queued asynchronously",
        "job_id":job_id,
        "poll_url":f"/results/{job_id}"
    }), 202
