from db import db

class AllUsers(db.Model):
    __tablename__ = 'all_users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.String(100), unique=True, nullable=False)
    hospital_name = db.Column(db.String(100), nullable=False)

class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('all_users.user_id'))
    organization = db.Column(db.String(100))
    hospital_id = db.Column(db.String(100), db.ForeignKey('hospital.hospital_id'))

class VaccinationRecord(db.Model):
    __tablename__ = 'vaccination_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('all_users.user_id'))
    vaccine_type = db.Column(db.String(100))
    disease = db.Column(db.String(100))
    dose_number = db.Column(db.Integer)
    date_administered = db.Column(db.String(100))
    hospital_id = db.Column(db.String(100), db.ForeignKey('hospital.hospital_id'))
