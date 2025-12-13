"""
Dinodial Proxy API Client for Doctor Booking Agent
"""
import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class DinodialClient:
    """Client for interacting with Dinodial Proxy API"""
    
    def __init__(self):
        self.base_url = os.getenv('DINODIAL_BASE_URL', 'https://api-dinodial-proxy.cyces.co')
        self.admin_token = os.getenv('ADMIN_TOKEN')
        self.token = os.getenv('TOKEN')
    
    def _get_headers(self, use_admin: bool = False) -> Dict[str, str]:
        """Get authorization headers"""
        token = self.admin_token if use_admin else self.token
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def generate_token(self, phone_number: str) -> Dict[str, Any]:
        """Generate a token for a phone number (admin only)"""
        endpoint = f'{self.base_url}/api/proxy/token/generate/'
        payload = {'phone_number': phone_number}
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=self._get_headers(use_admin=True)
        )
        return response.json()
    
    def initiate_call(self, prompt: str, evaluation_tool: Dict[str, Any], 
                     vad_engine: str = 'CAWL') -> Dict[str, Any]:
        """Initiate a call with the given prompt and evaluation tool"""
        endpoint = f'{self.base_url}/api/proxy/make-call/'
        payload = {
            'prompt': prompt,
            'evaluation_tool': evaluation_tool,
            'vad_engine': vad_engine
        }
        
        response = requests.post(
            endpoint,
            json=payload,
            headers=self._get_headers(use_admin=False)
        )
        return response.json()
    
    def get_call_list(self) -> Dict[str, Any]:
        """Get list of calls for the token"""
        endpoint = f'{self.base_url}/api/proxy/calls/list/'
        
        response = requests.get(
            endpoint,
            headers=self._get_headers(use_admin=False)
        )
        return response.json()
    
    def get_call_detail(self, call_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific call"""
        endpoint = f'{self.base_url}/api/proxy/call/detail/{call_id}/'
        
        response = requests.get(
            endpoint,
            headers=self._get_headers(use_admin=False)
        )
        return response.json()
    
    def get_call_recording(self, call_id: int) -> Dict[str, Any]:
        """Get recording URL for a call"""
        endpoint = f'{self.base_url}/api/proxy/call/recording/{call_id}/'
        
        response = requests.get(
            endpoint,
            headers=self._get_headers(use_admin=False)
        )
        return response.json()
