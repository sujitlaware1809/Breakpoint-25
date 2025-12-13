"""
Doctor Appointment Booking Voice AI Agent
Direct Dinodial Proxy Integration - No External Dependencies
"""
from typing import Dict, Any, Optional
from src.dinodial_client import DinodialClient
from src.prompts import get_booking_prompt, get_evaluation_tool

class DoctorBookingAgent:
    """Voice AI agent for doctor appointment booking"""
    
    def __init__(self):
        self.client = DinodialClient()
    
    def create_booking_call(self, phone_number: str, doctor_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Initiate a voice call for doctor appointment booking
        
        Args:
            phone_number: Patient phone number
            doctor_info: Optional doctor information to include in context
        
        Returns:
            Response from Dinodial API
        """
        # Get the appointment booking prompt
        prompt = get_booking_prompt(phone_number, doctor_info)
        
        # Get evaluation tool configuration
        evaluation_tool = get_evaluation_tool()
        
        # Initiate the call
        response = self.client.initiate_call(
            prompt=prompt,
            evaluation_tool=evaluation_tool,
            vad_engine='CAWL'
        )
        
        return response
    
    def get_booking_status(self, call_id: int) -> Dict[str, Any]:
        """Get the status and details of a booking call"""
        return self.client.get_call_detail(call_id)
    
    def get_call_recording(self, call_id: int) -> Dict[str, Any]:
        """Get the recording of a booking call"""
        return self.client.get_call_recording(call_id)
    
    def list_calls(self) -> Dict[str, Any]:
        """List all booking calls"""
        return self.client.get_call_list()
