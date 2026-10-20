from flask import Blueprint,jsonify
from app.services.firmware_service import firmware_service

results_bp=Blueprint('results',__name__)
@results_bp.route('/results/<job_id>',methods=['GET'])

def get_results(job_id):
    job_data=firmware_service.get_job_status(job_id)

    if not job_data:
        return jsonify({"error":f"JOB ID '{job_id}' not found"}),404

    return jsonify(job_data),200