"""
Doctor Appointment Booking Agent - Direct Dinodial Proxy
Simple & Fast - No External Dependencies
"""
import sys
from src.agent import DoctorBookingAgent

def main():
    """Main function - Fast & Direct"""
    agent = DoctorBookingAgent()
    
    print("🏥 Doctor Booking Voice AI Agent")
    print("=" * 50)
    
    # Get phone number
    phone_number = input("Enter patient phone number: ").strip()
    if not phone_number:
        print("❌ Phone number required")
        sys.exit(1)
    
    # Get doctor info
    doctor_name = input("Enter doctor name: ").strip() or "Dr. Raj Kumar"
    specialty = input("Enter specialty: ").strip() or "General Medicine"
    clinic = input("Enter clinic name: ").strip() or "City Health Clinic"
    
    print(f"\n🔄 Initiating booking call...")
    print(f"   Phone: {phone_number}")
    print(f"   Doctor: {doctor_name} ({specialty})")
    print(f"   Clinic: {clinic}\n")
    
    doctor_info = {
        'name': doctor_name,
        'specialty': specialty,
        'clinic': clinic,
    }
    
    try:
        # Make the booking call via Dinodial Proxy
        response = agent.create_booking_call(phone_number, doctor_info)
        
        print("📞 Response:")
        print(f"   Status: {response.get('status')}")
        
        if response.get('status') == 'success':
            call_id = response['data']['id']
            print(f"   ✅ Call initiated!")
            print(f"   Call ID: {call_id}")
            print(f"   Message: {response['data']['message']}")
        else:
            error_msg = response.get('data', {}).get('message', 'Unknown')
            error_detail = response.get('data', {}).get('detail', '')
            print(f"   ❌ Error: {error_msg}")
            if error_detail:
                print(f"   Details: {error_detail}")
            
            # Debug: Print full response
            print(f"\n   Debug - Full Response:")
            import json
            print(f"   {json.dumps(response, indent=2)}")
    
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 50 + "\n")

if __name__ == '__main__':
    main()

