from flask import Blueprint, request, jsonify
from db import db
from models import Hospital, VaccinationRecord

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/hospitals', methods=['GET'])
def get_all_hospitals():
    hospitals = Hospital.query.all()
    return jsonify([{"id": h.id, "hospital_id": h.hospital_id, "hospital_name": h.hospital_name} for h in hospitals])

