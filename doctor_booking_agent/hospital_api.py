"""
Complete Hospital Booking Management System API
Patient Portal + Doctor Dashboard + Admin Panel
"""
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import db, Doctor, Patient, Appointment, CallLog, DoctorAvailability
from src.agent import DoctorBookingAgent
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)

db.init_app(app)

# Initialize agent
agent = DoctorBookingAgent()

# Create tables
with app.app_context():
    db.create_all()
    print("[OK] Database initialized")

# ==================== PATIENT ENDPOINTS ====================

@app.route('/api/patient/register', methods=['POST'])
def register_patient():
    """Register a new patient"""
    try:
        data = request.json
        
        # Check if patient exists
        existing = Patient.query.filter_by(phone=data['phone']).first()
        if existing:
            return jsonify({
                'status': 'success',
                'data': {'id': existing.id, 'message': 'Patient already registered'}
            }), 200
        
        patient = Patient(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email'),
            age=data.get('age'),
            gender=data.get('gender'),
            address=data.get('address'),
            medical_history=data.get('medical_history')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'data': {'id': patient.id, 'message': 'Patient registered successfully'}
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'data': {'message': str(e)}}), 500

@app.route('/api/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient details"""
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({
        'status': 'success',
        'data': {
            'id': patient.id,
            'name': patient.name,
            'phone': patient.phone,
            'email': patient.email,
            'age': patient.age,
            'gender': patient.gender,
            'address': patient.address,
            'medical_history': patient.medical_history
        }
    })

@app.route('/api/patient/phone/<phone>', methods=['GET'])
def get_patient_by_phone(phone):
    """Get patient by phone number"""
    patient = Patient.query.filter_by(phone=phone).first()
    if not patient:
        return jsonify({'status': 'error', 'data': {'message': 'Patient not found'}}), 404
    
    return jsonify({
        'status': 'success',
        'data': {
            'id': patient.id,
            'name': patient.name,
            'phone': patient.phone,
            'email': patient.email
        }
    })

# ==================== DOCTOR ENDPOINTS ====================

@app.route('/api/doctor/register', methods=['POST'])
def register_doctor():
    """Register a new doctor"""
    try:
        data = request.json
        
        doctor = Doctor(
            name=data['name'],
            specialty=data['specialty'],
            phone=data.get('phone'),
            email=data.get('email'),
            clinic_name=data.get('clinic_name'),
            available_days=data.get('available_days', 'Mon-Fri'),
            available_time=data.get('available_time', '9 AM - 5 PM'),
            consultation_fee=data.get('consultation_fee', 500)
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'data': {'id': doctor.id, 'message': 'Doctor registered successfully'}
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'data': {'message': str(e)}}), 500

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    specialty = request.args.get('specialty')
    
    query = Doctor.query
    if specialty:
        query = query.filter_by(specialty=specialty)
    
    doctors = query.all()
    
    return jsonify({
        'status': 'success',
        'data': [{
            'id': d.id,
            'name': d.name,
            'specialty': d.specialty,
            'clinic_name': d.clinic_name,
            'available_time': d.available_time,
            'consultation_fee': d.consultation_fee
        } for d in doctors]
    })

@app.route('/api/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get doctor details"""
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify({
        'status': 'success',
        'data': {
            'id': doctor.id,
            'name': doctor.name,
            'specialty': doctor.specialty,
            'phone': doctor.phone,
            'email': doctor.email,
            'clinic_name': doctor.clinic_name,
            'available_days': doctor.available_days,
            'available_time': doctor.available_time,
            'consultation_fee': doctor.consultation_fee
        }
    })

@app.route('/api/doctor/<int:doctor_id>/appointments', methods=['GET'])
def get_doctor_appointments(doctor_id):
    """Get all appointments for a doctor"""
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).order_by(Appointment.appointment_date.desc()).all()
    
    return jsonify({
        'status': 'success',
        'data': [{
            'id': a.id,
            'patient_name': a.patient.name,
            'patient_phone': a.patient.phone,
            'appointment_date': a.appointment_date.isoformat(),
            'appointment_time': a.appointment_time,
            'status': a.status,
            'reason': a.reason,
            'confirmation_number': a.confirmation_number
        } for a in appointments]
    })

# ==================== APPOINTMENT ENDPOINTS ====================

@app.route('/api/appointment/book', methods=['POST'])
def book_appointment():
    """Book an appointment with voice call"""
    try:
        data = request.json
        
        # Get or create patient
        patient = Patient.query.filter_by(phone=data['patient_phone']).first()
        if not patient:
            patient = Patient(
                name=data.get('patient_name', 'Unknown'),
                phone=data['patient_phone']
            )
            db.session.add(patient)
            db.session.flush()
        
        # Get doctor
        doctor = Doctor.query.get(data['doctor_id'])
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        # Create appointment
        confirmation_num = f"APT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Parse date and time (with defaults)
        appointment_date = data.get('appointment_date') or data.get('date') or datetime.now().strftime('%Y-%m-%d')
        appointment_time = data.get('appointment_time') or data.get('time') or '10:00 AM'
        
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
            appointment_time=appointment_time,
            reason=data.get('reason'),
            symptoms=data.get('symptoms'),
            special_notes=data.get('special_notes'),
            confirmation_number=confirmation_num,
            status='scheduled'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        # Initiate voice call
        doctor_info = {
            'name': doctor.name,
            'specialty': doctor.specialty,
            'clinic': doctor.clinic_name
        }
        
        call_response = agent.create_booking_call(data['patient_phone'], doctor_info)
        
        # Log the call
        if call_response.get('status') == 'success':
            call_log = CallLog(
                call_id=call_response['data'].get('id'),
                phone_number=data['patient_phone'],
                appointment_id=appointment.id,
                status='in_progress'
            )
            db.session.add(call_log)
            
            appointment.call_id = str(call_response['data'].get('id'))
            appointment.call_status = 'initiated'
            
            db.session.commit()
        
        return jsonify({
            'appointment_id': appointment.id,
            'confirmation_number': confirmation_num,
            'call_id': call_response['data'].get('id') if call_response.get('status') == 'success' else None,
            'call_status': call_response.get('status'),
            'message': 'Appointment booked and call initiated'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error booking appointment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointment/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get appointment details"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    return jsonify({
        'status': 'success',
        'data': {
            'id': appointment.id,
            'patient': {
                'id': appointment.patient.id,
                'name': appointment.patient.name,
                'phone': appointment.patient.phone
            },
            'doctor': {
                'id': appointment.doctor.id,
                'name': appointment.doctor.name,
                'specialty': appointment.doctor.specialty,
                'clinic': appointment.doctor.clinic_name
            },
            'appointment_date': appointment.appointment_date.isoformat(),
            'appointment_time': appointment.appointment_time,
            'status': appointment.status,
            'reason': appointment.reason,
            'symptoms': appointment.symptoms,
            'special_notes': appointment.special_notes,
            'confirmation_number': appointment.confirmation_number,
            'call_id': appointment.call_id,
            'call_status': appointment.call_status,
            'call_recording_url': appointment.call_recording_url
        }
    })

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Get all appointments with filters"""
    status = request.args.get('status')
    date_str = request.args.get('date')
    
    query = Appointment.query
    
    if status:
        query = query.filter_by(status=status)
    if date_str:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        query = query.filter_by(appointment_date=target_date)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).all()
    
    return jsonify({
        'status': 'success',
        'data': [{
            'id': a.id,
            'patient_name': a.patient.name,
            'doctor_name': a.doctor.name,
            'date': a.appointment_date.isoformat(),
            'time': a.appointment_time,
            'status': a.status,
            'confirmation_number': a.confirmation_number
        } for a in appointments]
    })

@app.route('/api/appointment/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'cancelled'
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': {'message': 'Appointment cancelled successfully'}
    })

# ==================== CALL MANAGEMENT ====================

@app.route('/api/calls', methods=['GET'])
def get_calls():
    """Get all call logs"""
    calls = CallLog.query.order_by(CallLog.created_at.desc()).all()
    
    return jsonify({
        'status': 'success',
        'data': [{
            'id': c.id,
            'call_id': c.call_id,
            'phone_number': c.phone_number,
            'status': c.status,
            'duration': c.duration,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in calls]
    })

# ==================== DASHBOARD STATS ====================

@app.route('/api/stats/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    
    today = date.today()
    today_appointments = Appointment.query.filter_by(appointment_date=today).count()
    
    pending_appointments = Appointment.query.filter_by(status='scheduled').count()
    completed_appointments = Appointment.query.filter_by(status='completed').count()
    
    return jsonify({
        'status': 'success',
        'data': {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_appointments': total_appointments,
            'today_appointments': today_appointments,
            'pending_appointments': pending_appointments,
            'completed_appointments': completed_appointments
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'service': 'Hospital Management System'}), 200

# ==================== DOCTOR AUTHENTICATION ====================

@app.route('/api/doctor/login', methods=['POST'])
def doctor_login():
    """Doctor login"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        doctor = Doctor.query.filter_by(email=email).first()
        
        if not doctor or not doctor.password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if check_password_hash(doctor.password, password):
            session['doctor_id'] = doctor.id
            return jsonify({
                'success': True,
                'doctor': {
                    'id': doctor.id,
                    'name': doctor.name,
                    'email': doctor.email,
                    'specialty': doctor.specialty,
                    'clinic_name': doctor.clinic_name
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctor/set-password', methods=['POST'])
def set_doctor_password():
    """Set doctor password (for initial setup)"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        doctor = Doctor.query.filter_by(email=email).first()
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        doctor.password = generate_password_hash(password)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password set successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== DOCTOR AVAILABILITY MANAGEMENT ====================

@app.route('/api/doctor/<int:doctor_id>/availability', methods=['GET'])
def get_doctor_availability(doctor_id):
    """Get doctor's availability slots"""
    try:
        start_date = request.args.get('start_date', date.today().isoformat())
        end_date = request.args.get('end_date', (date.today() + timedelta(days=7)).isoformat())
        
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        slots = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor_id,
            DoctorAvailability.date >= start,
            DoctorAvailability.date <= end
        ).all()
        
        return jsonify({
            'success': True,
            'slots': [{
                'id': slot.id,
                'date': slot.date.isoformat(),
                'time_slot': slot.time_slot,
                'is_booked': slot.is_booked,
                'max_patients': slot.max_patients
            } for slot in slots]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctor/<int:doctor_id>/availability', methods=['POST'])
def add_doctor_availability(doctor_id):
    """Add availability slots for doctor"""
    try:
        data = request.json
        date_str = data.get('date')
        time_slots = data.get('time_slots', [])  # List of time slots
        
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        added_slots = []
        for time_slot in time_slots:
            # Check if slot already exists
            existing = DoctorAvailability.query.filter_by(
                doctor_id=doctor_id,
                date=appointment_date,
                time_slot=time_slot
            ).first()
            
            if not existing:
                slot = DoctorAvailability(
                    doctor_id=doctor_id,
                    date=appointment_date,
                    time_slot=time_slot,
                    max_patients=data.get('max_patients', 1)
                )
                db.session.add(slot)
                added_slots.append(time_slot)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Added {len(added_slots)} availability slots',
            'slots_added': added_slots
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctor/<int:doctor_id>/availability/<int:slot_id>', methods=['DELETE'])
def delete_availability_slot(doctor_id, slot_id):
    """Delete an availability slot"""
    try:
        slot = DoctorAvailability.query.filter_by(id=slot_id, doctor_id=doctor_id).first()
        if not slot:
            return jsonify({'error': 'Slot not found'}), 404
        
        if slot.is_booked:
            return jsonify({'error': 'Cannot delete booked slot'}), 400
        
        db.session.delete(slot)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Slot deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctor/<int:doctor_id>/toggle-availability', methods=['POST'])
def toggle_doctor_availability(doctor_id):
    """Toggle doctor's overall availability status"""
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        doctor.is_available = not doctor.is_available
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_available': doctor.is_available,
            'message': f'Doctor is now {"available" if doctor.is_available else "unavailable"}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== GET AVAILABLE DOCTORS FOR BOOKING ====================

@app.route('/api/doctors/available', methods=['GET'])
def get_available_doctors():
    """Get currently available doctors with their next available slots"""
    try:
        specialty = request.args.get('specialty')
        date_str = request.args.get('date', date.today().isoformat())
        
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        query = Doctor.query.filter_by(is_available=True)
        if specialty:
            query = query.filter_by(specialty=specialty)
        
        doctors = query.all()
        
        result = []
        for doctor in doctors:
            # Get available slots for this doctor
            available_slots = DoctorAvailability.query.filter(
                DoctorAvailability.doctor_id == doctor.id,
                DoctorAvailability.date >= query_date,
                DoctorAvailability.is_booked == False
            ).order_by(DoctorAvailability.date, DoctorAvailability.time_slot).limit(5).all()
            
            result.append({
                'id': doctor.id,
                'name': doctor.name,
                'specialty': doctor.specialty,
                'clinic_name': doctor.clinic_name,
                'consultation_fee': doctor.consultation_fee,
                'available_slots': [{
                    'date': slot.date.isoformat(),
                    'time': slot.time_slot
                } for slot in available_slots]
            })
        
        return jsonify({
            'success': True,
            'doctors': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== CALL RESULT SYNC ====================

@app.route('/api/call/sync/<call_id>', methods=['POST'])
def sync_call_results(call_id):
    """Sync call evaluation results with database"""
    try:
        # Get call details from Dinodial
        call_detail = agent.get_booking_status(int(call_id))
        
        if call_detail.get('status') != 'success':
            return jsonify({'error': 'Failed to fetch call details'}), 400
        
        call_data = call_detail['data']
        evaluation_result = call_data.get('evaluation_result', {})
        
        # Find the call log and appointment
        call_log = CallLog.query.filter_by(call_id=call_id).first()
        if not call_log or not call_log.appointment_id:
            return jsonify({'error': 'Call or appointment not found'}), 404
        
        appointment = Appointment.query.get(call_log.appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Update patient information from evaluation results
        patient = appointment.patient
        
        # Update patient name if provided in evaluation
        if evaluation_result.get('patient_name') and evaluation_result['patient_name'] != 'Unknown':
            patient.name = evaluation_result['patient_name']
        
        # Update appointment details
        if evaluation_result.get('symptoms'):
            appointment.symptoms = evaluation_result['symptoms']
        
        if evaluation_result.get('special_notes'):
            appointment.special_notes = evaluation_result['special_notes']
        
        # Update doctor if specialty changed
        if evaluation_result.get('specialty_needed'):
            specialty = evaluation_result['specialty_needed']
            # Try to find a doctor with matching specialty
            matching_doctor = Doctor.query.filter_by(specialty=specialty, is_available=True).first()
            if matching_doctor:
                appointment.doctor_id = matching_doctor.id
        
        # Update appointment time if provided
        if evaluation_result.get('appointment_date'):
            try:
                appointment.appointment_date = datetime.strptime(
                    evaluation_result['appointment_date'], '%Y-%m-%d'
                ).date()
            except:
                pass
        
        if evaluation_result.get('appointment_time'):
            appointment.appointment_time = evaluation_result['appointment_time']
        
        # Update call log
        call_log.status = call_data.get('status', 'completed')
        call_log.duration = call_data.get('duration')
        call_log.evaluation_result = str(evaluation_result)
        
        # Update appointment status
        if evaluation_result.get('appointment_confirmed') == True:
            appointment.status = 'confirmed'
            appointment.call_status = 'completed'
        else:
            appointment.status = 'pending'
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Call results synced successfully',
            'data': {
                'patient_name': patient.name,
                'doctor': appointment.doctor.name,
                'specialty': appointment.doctor.specialty,
                'symptoms': appointment.symptoms,
                'appointment_date': appointment.appointment_date.isoformat(),
                'appointment_time': appointment.appointment_time
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/webhook/call-completed', methods=['POST'])
def call_completed_webhook():
    """Webhook endpoint for Dinodial to notify when call is completed"""
    try:
        data = request.json
        call_id = data.get('call_id')
        
        if not call_id:
            return jsonify({'error': 'call_id required'}), 400
        
        # Sync the results
        return sync_call_results(str(call_id))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

