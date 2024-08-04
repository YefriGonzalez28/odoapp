from dental_clinic_app import db, app
from dental_clinic_app.models import User, Appointment

with app.app_context():
    db.create_all()
    print("Database tables created.")