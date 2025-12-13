"""
Prompt templates for Doctor Booking Agent
"""
from typing import Dict, Any, Optional

def get_booking_prompt(phone_number: str, doctor_info: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate the AI prompt for doctor appointment booking
    
    Args:
        phone_number: Patient phone number
        doctor_info: Optional doctor information
    
    Returns:
        XML-formatted prompt for the voice AI
    """
    doctor_context = ""
    if doctor_info:
        doctor_context = f"""
    <doctor_info>
        <name>{doctor_info.get('name', 'Available Doctor')}</name>
        <specialty>{doctor_info.get('specialty', 'General Practitioner')}</specialty>
        <clinic>{doctor_info.get('clinic', 'Healthcare Clinic')}</clinic>
        <available_slots>{doctor_info.get('slots', '10 AM - 5 PM')}</available_slots>
    </doctor_info>
    """
    
    prompt = f"""Hospital booking assistant. Speak naturally in Indian English.

PATIENT: {phone_number}
{doctor_context if doctor_context else ''}

CRITICAL: Get BOTH first AND last name. If patient says only "Rahul", ask "And your surname?" NO single names.

WORKFLOW:
1. "Your first name?" → "And last name?"
2. session_notes: append "Name: [First] [Last]"
3. "What brings you in today?"
4. session_notes: append "Symptoms: [details]"
5. Match: Fever→General Medicine, Chest→Cardiology, Skin→Dermatology, Joint→Orthopedics
6. Check time: Current={datetime.now().strftime('%I:%M %p')}. Doctor hours: 10 AM-5 PM
   - If patient asks 5PM+ or past time: "Doctor closes at 5 PM. Tomorrow at [time]?"
   - If slot taken: "[Time] booked. Try [next slot]?"
7. Suggest: "Dr.[Name], [Specialty], free at [realistic times]"
8. Get preference: "Today, tomorrow, or which date?"
9. CONFIRM: "[Full Name], Dr.[Doctor], [Date] [Time] for [symptoms]"
10. "Arrive 10 min early. SMS confirmation coming."
11. end_call with "Appointment booked"

RULES:
- Get BOTH names. "Verma" alone = NOT valid
- Time logic: Don't offer past times or after 5 PM
- Explain if unavailable: "5 PM passed" or "slot booked"
- Under 15 words per response
"""
    return prompt

def get_evaluation_tool() -> Dict[str, Any]:
    """Optimized evaluation tool for hackathon - captures key data with minimal tokens"""
    return {
        "name": "call_outcomes",
        "behavior": "BLOCKING",
        "parameters": {
            "type": "OBJECT",
            "required": ["appointment_confirmed", "patient_name", "specialty_needed", "symptoms"],
            "properties": {
                "appointment_confirmed": {
                    "type": "BOOLEAN",
                    "description": "Appointment booked successfully"
                },
                "patient_name": {
                    "type": "STRING",
                    "description": "Patient's exact full name (first + last, as spoken - NO placeholders)"
                },
                "symptoms": {
                    "type": "STRING",
                    "description": "Health problem/symptoms described"
                },
                "specialty_needed": {
                    "type": "STRING",
                    "description": "Medical specialty: Cardiology|Dermatology|Pediatrics|Orthopedics|General Medicine|ENT (match to symptoms)"
                },
                "preferred_doctor": {
                    "type": "STRING",
                    "description": "Doctor name chosen"
                },
                "appointment_date": {
                    "type": "STRING",
                    "description": "Date (YYYY-MM-DD)"
                },
                "appointment_time": {
                    "type": "STRING",
                    "description": "Time slot"
                },
                "special_notes": {
                    "type": "STRING",
                    "description": "Allergies/special requirements"
                }
            }
        },
        "description": "Capture appointment details: name, symptoms, specialty, doctor, date, time"
    }
