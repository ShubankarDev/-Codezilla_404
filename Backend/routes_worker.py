from flask import Blueprint, request, jsonify
from db import db
from models import VaccinationRecord

worker_bp = Blueprint('worker', __name__)

@worker_bp.route('/add-record', methods=['POST'])
def add_vaccination_record():
    data = request.json
    record = VaccinationRecord(**data)
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Vaccination record added successfully"})
