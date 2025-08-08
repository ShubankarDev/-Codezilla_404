# admin_analysis.py

from model import db
from model import AllUsers, VaccinationRecord, Hospital
from sqlalchemy import func
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def get_basic_stats():
    total_users = AllUsers.query.count()
    total_vaccinated = db.session.query(VaccinationRecord.user_id).distinct().count()
    completion_percentage = round((total_vaccinated / total_users) * 100, 2) if total_users else 0

    vaccine_distribution = db.session.query(
        VaccinationRecord.vaccine_type, func.count(VaccinationRecord.id)
    ).group_by(VaccinationRecord.vaccine_type).all()

    hospital_distribution = db.session.query(
        Hospital.hospital_name, func.count(VaccinationRecord.id)
    ).join(VaccinationRecord, Hospital.id == VaccinationRecord.hospital_id).group_by(Hospital.hospital_name).all()

    return {
        "total_users": total_users,
        "total_vaccinated": total_vaccinated,
        "completion_percentage": completion_percentage,
        "vaccine_distribution": dict(vaccine_distribution),
        "hospital_distribution": dict(hospital_distribution),
    }

def get_trend_prediction():
    # Fetch records and convert to DataFrame
    records = VaccinationRecord.query.with_entities(
        VaccinationRecord.date_administered
    ).all()

    if not records:
        return []

    df = pd.DataFrame(records, columns=['date'])
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.dayofyear
    df_grouped = df.groupby('day').size().reset_index(name='count')

    X = df_grouped[['day']]
    y = df_grouped['count']

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.array([[X['day'].max() + i] for i in range(1, 8)])  # next 7 days
    predictions = model.predict(future_days)

    return {
        "future_days": future_days.flatten().tolist(),
        "predicted_counts": predictions.round(2).tolist()
    }
