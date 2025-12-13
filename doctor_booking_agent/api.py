"""
Flask API Backend for Doctor Booking Agent
Connects Next.js frontend with Dinodial Voice AI
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.agent import DoctorBookingAgent
import os

app = Flask(__name__)
CORS(app)

# Initialize agent
agent = DoctorBookingAgent()

@app.route('/api/booking/initiate', methods=['POST'])
def initiate_booking():
    """Initiate a doctor booking call"""
    try:
        data = request.json
        phone_number = data.get('phone_number')
        doctor_info = data.get('doctor_info', {})
        
        if not phone_number:
            return jsonify({
                'status': 'error',
                'data': {'message': 'Phone number is required'}
            }), 400
        
        # Initiate call through agent
        response = agent.create_booking_call(phone_number, doctor_info)
        
        return jsonify(response), 200 if response.get('status') == 'success' else 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': {'message': str(e)}
        }), 500

@app.route('/api/booking/calls', methods=['GET'])
def get_calls():
    """Get list of all calls"""
    try:
        response = agent.list_calls()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': {'message': str(e)}
        }), 500

@app.route('/api/booking/call/<int:call_id>', methods=['GET'])
def get_call_detail(call_id):
    """Get details of a specific call"""
    try:
        response = agent.get_booking_status(call_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': {'message': str(e)}
        }), 500

@app.route('/api/booking/recording/<int:call_id>', methods=['GET'])
def get_recording(call_id):
    """Get recording URL for a call"""
    try:
        response = agent.get_call_recording(call_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': {'message': str(e)}
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Doctor Booking API'}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
