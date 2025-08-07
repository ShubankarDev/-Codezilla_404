from flask import Blueprint, request, jsonify
from db import db
from models import Hospital, VaccinationRecord

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/hospitals', methods=['GET'])
def get_all_hospitals():
    hospitals = Hospital.query.all()
    return jsonify([{"id": h.id, "hospital_id": h.hospital_id, "hospital_name": h.hospital_name} for h in hospitals])

@admin_bp.route('/user-records/<user_id>', methods=['GET'])
def get_user_records(user_id):
    records = VaccinationRecord.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "vaccine_type": r.vaccine_type,
        "disease": r.disease,
        "dose_number": r.dose_number,
        "date_administered": r.date_administered,
        "hospital_id": r.hospital_id
    } for r in records])
