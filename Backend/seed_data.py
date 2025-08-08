import random
from faker import Faker
from werkzeug.security import generate_password_hash
from model import db, AllUsers, Hospital, Worker, VaccinationRecord

fake = Faker()

def seed_data():

    # --- Seed Hospitals ---
    hospitals = []
    for i in range(5):
        hospital = Hospital(
            hospital_id=f"HOSP{i+1}",
            hospital_name=fake.company()
        )
        hospitals.append(hospital)
        db.session.add(hospital)

    # --- Seed Users ---
    roles = [ "worker", "user"]
    users = []
    for i in range(20):
        role = random.choice(roles)
        user = AllUsers(
            role=role,
            user_id=f"user{i+1}",
            password=generate_password_hash("password123"),
            email=f"user{i+1}@example.com"
        )
        users.append(user)
        db.session.add(user)

    db.session.commit()

    # --- Seed Workers (only for users with role = worker) ---
    for user in users:
        if user.role == "worker":
            worker = Worker(
                user_id=user.user_id,
                organization=fake.company(),
                hospital_id=random.choice(hospitals).hospital_id
            )
            db.session.add(worker)

    db.session.commit()

    # --- Seed Vaccination Records (for all users) ---
    vaccine_types = ["Covaxin", "Covishield", "Pfizer", "Moderna"]
    diseases = ["COVID-19", "Hepatitis B", "Influenza", "HPV"]

    for user in users:
        for _ in range(random.randint(1, 3)):  
            record = VaccinationRecord(
                user_id=user.user_id,
                vaccine_type=random.choice(vaccine_types),
                disease=random.choice(diseases),
                dose_number=random.randint(1, 3),
                date_administered=str(fake.date_between(start_date="-2y", end_date="today")),
                hospital_id=random.choice(hospitals).hospital_id
            )
            db.session.add(record)

    db.session.commit()
    print("✅ Database seeded successfully!")
