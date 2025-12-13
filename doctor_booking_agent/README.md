# Doctor Appointment Booking Voice AI Agent

A voice AI agent for scheduling doctor appointments using Dinodial Proxy API and Google Gemini for intelligent response generation.

## Project Structure

```
doctor_booking_agent/
├── src/
│   ├── __init__.py
│   ├── dinodial_client.py       # Dinodial API client
│   ├── gemini_handler.py        # Gemini AI integration
│   ├── agent.py                 # Main agent logic
│   └── prompts.py               # AI prompts and evaluation tools
├── config/                      # Configuration files
├── prompts/                     # Additional prompt templates
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```
3. Update `.env` with your credentials:
```
# Dinodial Configuration
ADMIN_TOKEN=your_admin_token_here
DINODIAL_BASE_URL=https://api-dinodial-proxy.cyces.co
PHONE_NUMBER=your_phone_number
TOKEN=your_generated_token

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
```

### Getting Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key to your `.env` file

## Usage

Run the agent:
```bash
python main.py
```

## Features

- ✅ Initiate appointment booking calls
- ✅ **Gemini-powered dynamic response generation**
- ✅ **Intelligent greeting personalization**
- ✅ **Context-aware prompts**
- ✅ Retrieve call history and details
- ✅ Access call recordings
- ✅ Structured evaluation of booking outcomes
- ✅ Multi-language support ready

## API Integration

### Dinodial Proxy API
- `POST /api/proxy/make-call/` - Initiate calls
- `GET /api/proxy/calls/list/` - List calls
- `GET /api/proxy/call/detail/{id}/` - Get call details
- `GET /api/proxy/call/recording/{id}/` - Get recordings

### Gemini AI
- Generates dynamic greetings
- Creates context-aware availability requests
- Produces confirmation messages
- Generates booking prompts
- Validates appointment data

## Using Gemini with the Agent

```python
from src.agent import DoctorBookingAgent

agent = DoctorBookingAgent()

# Generate greeting
greeting = agent.generate_greeting("John Doe")

# Generate availability request
availability_prompt = agent.generate_availability_request("Dr. Raj Kumar", "General Medicine")

# Generate confirmation
confirmation = agent.generate_confirmation(
    "John Doe", 
    "Dr. Raj Kumar", 
    "2025-12-20", 
    "10:00 AM",
    "APT-12345"
)

# Generate dynamic booking prompt
prompt = agent.generate_dynamic_prompt(
    "John Doe",
    "Dr. Raj Kumar",
    "General Medicine",
    "City Health Clinic"
)
```

## Notes

- Rate limit: 1 call per 5 minutes per token (Dinodial)
- Evaluation tool is blocking - call waits for completion
- VAD Engine: CAWL (default) or ANCHORITE
- Gemini responses are customized for voice/speech conversion
