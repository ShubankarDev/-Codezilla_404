from flask import Blueprint, request, jsonify
from model import db
from model import VaccinationRecord

user_bp = Blueprint('user', __name__)

@user_bp.route('/my-records/<user_id>', methods=['GET'])
def view_user_records(user_id):
    records = VaccinationRecord.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "vaccine_type": r.vaccine_type,
        "disease": r.disease,
        "dose_number": r.dose_number,
        "date_administered": r.date_administered,
        "hospital_id": r.hospital_id
    } for r in records])
