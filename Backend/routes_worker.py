from flask import Blueprint, request, jsonify
from model import db
from model import VaccinationRecord

worker_bp = Blueprint('worker', __name__)

@worker_bp.route('/add-record', methods=['POST'])
def add_vaccination_record():
    data = request.json
    record = VaccinationRecord(**data)
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Vaccination record added successfully"})

@worker_bp.route('/user-records/<user_id>', methods=['GET'])
def get_user_records(user_id):
    records = VaccinationRecord.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "vaccine_type": r.vaccine_type,
        "disease": r.disease,
        "dose_number": r.dose_number,
        "date_administered": r.date_administered,
        "hospital_id": r.hospital_id
    } for r in records])
