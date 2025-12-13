"""
Seed database with sample doctors and patients
"""
from hospital_api import app, db
from models import Doctor, Patient
from datetime import datetime

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Add sample doctors
        doctors = [
            Doctor(
                name="Dr. Raj Kumar",
                specialty="General Medicine",
                phone="+919876543210",
                email="raj.kumar@hospital.com",
                clinic_name="City Health Clinic",
                available_days="Monday-Friday",
                available_time="9:00 AM - 5:00 PM",
                consultation_fee=500
            ),
            Doctor(
                name="Dr. Priya Sharma",
                specialty="Pediatrics",
                phone="+919876543211",
                email="priya.sharma@hospital.com",
                clinic_name="Children's Care Center",
                available_days="Monday-Saturday",
                available_time="10:00 AM - 6:00 PM",
                consultation_fee=600
            ),
            Doctor(
                name="Dr. Arun Nair",
                specialty="Cardiology",
                phone="+919876543212",
                email="arun.nair@hospital.com",
                clinic_name="Heart Care Hospital",
                available_days="Monday-Friday",
                available_time="8:00 AM - 4:00 PM",
                consultation_fee=1000
            ),
            Doctor(
                name="Dr. Sujit Reddy",
                specialty="Dermatology",
                phone="+919876543213",
                email="sujit.reddy@hospital.com",
                clinic_name="Skin & Beauty Clinic",
                available_days="Tuesday-Saturday",
                available_time="11:00 AM - 7:00 PM",
                consultation_fee=700
            ),
            Doctor(
                name="Dr. Meera Patel",
                specialty="Orthopedics",
                phone="+919876543214",
                email="meera.patel@hospital.com",
                clinic_name="Bone & Joint Center",
                available_days="Monday-Saturday",
                available_time="9:00 AM - 5:00 PM",
                consultation_fee=800
            )
        ]
        
        for doctor in doctors:
            db.session.add(doctor)
        
        # Add sample patients
        patients = [
            Patient(
                name="Ramesh Kumar",
                phone="+919098444187",
                email="ramesh@example.com",
                age=35,
                gender="Male",
                address="123 MG Road, Bangalore",
                medical_history="Diabetes"
            ),
            Patient(
                name="Anjali Singh",
                phone="+919098444188",
                email="anjali@example.com",
                age=28,
                gender="Female",
                address="456 Anna Nagar, Chennai"
            ),
            Patient(
                name="Vikram Joshi",
                phone="+919098444189",
                email="vikram@example.com",
                age=42,
                gender="Male",
                address="789 Park Street, Kolkata",
                medical_history="Hypertension"
            )
        ]
        
        for patient in patients:
            db.session.add(patient)
        
        db.session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   - Added {len(doctors)} doctors")
        print(f"   - Added {len(patients)} patients")

if __name__ == '__main__':
    seed_database()
