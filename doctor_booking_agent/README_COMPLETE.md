# Doctor Appointment Booking System with Voice AI

Complete hospital management system with AI-powered voice appointment booking using Dinodial API.

## 🎯 Features

### For Patients:
- **Voice AI Booking**: Agent calls patients and books appointments
- Agent asks for: Name, symptoms, preferred specialty, timing
- Real-time doctor availability checking
- Instant appointment confirmation

### For Doctors:
- **Doctor Dashboard**: Login and manage schedule
- **Availability Management**: Add/remove time slots
- **Toggle Availability**: Mark yourself available/unavailable
- **View Appointments**: See all bookings with patient details
- **Call Details**: View call recordings and transcripts

### Voice AI Agent Flow:
1. Greets patient and asks for name
2. Asks about health problem/symptoms
3. Suggests appropriate specialty
4. Shows available doctors with timing
5. Confirms appointment details
6. Updates doctor's dashboard automatically

## 🚀 Quick Start

### 1. Backend Setup (Flask API)

```bash
# Install dependencies
cd doctor_booking_agent
pip install -r requirements.txt

# Seed database with doctors and availability
python seed_enhanced.py

# Start Flask backend
python hospital_api.py
```

Backend runs on: **http://localhost:5000**

### 2. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://localhost:3000**

## 🔐 Doctor Login Credentials

All doctors use password: `password123`

- **Dr. Raj Kumar** (General Medicine)
  - Email: rajkumar@hospital.com
  - Fee: ₹500

- **Dr. Priya Sharma** (Pediatrics)
  - Email: priya@hospital.com
  - Fee: ₹600

- **Dr. Arun Nair** (Cardiology)
  - Email: arun@hospital.com
  - Fee: ₹1000

- **Dr. Sujit Reddy** (Dermatology)
  - Email: sujit@hospital.com
  - Fee: ₹700

- **Dr. Meera Patel** (Orthopedics)
  - Email: meera@hospital.com
  - Fee: ₹800

## 📱 Application Pages

- **Patient Booking**: http://localhost:3000
- **Doctor Dashboard**: http://localhost:3000/doctor-login
- **Admin Panel**: http://localhost:3000/admin

## 🔧 API Endpoints

### Patient Endpoints
- `POST /api/appointment/book` - Book appointment with voice call
- `GET /api/doctors` - List all doctors
- `GET /api/doctors/available` - Get available doctors with slots

### Doctor Endpoints
- `POST /api/doctor/login` - Doctor login
- `GET /api/doctor/{id}/appointments` - Get doctor's appointments
- `POST /api/doctor/{id}/availability` - Add availability slots
- `DELETE /api/doctor/{id}/availability/{slot_id}` - Remove slot
- `POST /api/doctor/{id}/toggle-availability` - Toggle available status

## 🤖 Voice AI Configuration

The agent is configured to:
- Speak naturally in English (India)
- Show empathy when patients describe symptoms
- Suggest appropriate doctors based on symptoms
- Confirm all details before booking
- Provide clear next steps

## 📊 Database Models

- **Doctor**: Profile, specialty, availability, fees
- **Patient**: Contact info, medical history
- **Appointment**: Booking details, call status
- **CallLog**: Voice call recordings and transcripts
- **DoctorAvailability**: Time slot management

## 🎬 Booking Flow

1. Patient fills form on frontend
2. Frontend calls `/api/booking`
3. Backend creates appointment in database
4. Backend initiates Dinodial voice call
5. Agent calls patient and confirms details
6. Appointment updates with call status
7. Doctor sees booking on dashboard

## 🔄 Real-time Updates

- Doctors can add slots from dashboard
- Patient booking shows only available slots
- Booked slots automatically marked as unavailable
- Dashboard refreshes with new appointments

## 📞 Test Phone Number

Update `.env` with your test number:
```
PHONE_NUMBER=+918098444187
```

## 🛠️ Development

- Backend: Flask + SQLAlchemy + SQLite
- Frontend: Next.js + React
- Voice AI: Dinodial Proxy API
- Database: SQLite (hospital_booking.db)

## 📝 Environment Variables

**Backend (.env):**
```
ADMIN_TOKEN=dXNlcjEyMy1zZXNzaW9uLXRva2Vu
DINODIAL_BASE_URL=https://api-dinodial-proxy.cyces.co
PHONE_NUMBER=+918098444187
TOKEN=Jy8p+XvE9CbP0oXJkbdiPpF2VOn8d+1YCYSkPfG65HU=
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 🎯 Hackathon Notes

- Built for Breakpoint Dinodial Voice AI Hackathon
- Complete hospital management system
- AI-powered appointment booking
- Doctor availability management
- Real-time dashboard updates

## 📧 Support

Check the logs in:
- Flask: Terminal output
- Next.js: Browser console
- Database: `hospital_booking.db`

---

**Made with ❤️ for Breakpoint Hackathon 2025**
