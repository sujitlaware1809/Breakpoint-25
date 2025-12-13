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
    
    prompt = f"""You are a hospital appointment booking assistant. Speak naturally in English (Indian accent).

PATIENT: {phone_number}
{doctor_context if doctor_context else ''}

WORKFLOW:
1. Ask patient's FULL NAME (capture exactly as spoken - no placeholders)
2. Ask symptoms/health concern  
3. Match specialty: Fever/Cold→General Medicine, Heart→Cardiology, Skin→Dermatology, Joint→Orthopedics, Child→Pediatrics
4. Suggest doctor with specialty & timings
5. Ask preferred date/time
6. CONFIRM: "[Name], appointment with Dr.[Doctor], [Specialty], [Date] [Time] for [symptoms]"
7. Say "Please arrive 10 minutes early"

RULES:
- Capture patient's REAL name (not Verma/Kumar/generic)
- Match symptoms to CORRECT specialty (don't default to General Medicine)
- Keep responses short and conversational
- Show empathy: "I understand" / "I'm sorry to hear that"
- No filler words (okay, well, actually)

EXAMPLE:
"Hello! May I have your full name please?"
"Thank you [Name]. What brings you in today?"
"I understand. For [symptoms], I recommend our [Specialty] specialist."
"Dr.[Doctor] is available [date] at [times]. Which works for you?"
"Perfect! [Name], your appointment with Dr.[Doctor], [Specialty], on [date] at [time] for [symptoms] is confirmed. Please arrive 10 minutes early."
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
