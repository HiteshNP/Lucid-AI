import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv('.env.local')

# Set your ElevenLabs API key
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
# If not using the .env file, you can set the API key directly
# ELEVENLABS_API_KEY = "sk_fb214b75397751299a0abea5119d7779675989c5f8405cf7"

# URL to fetch voices
url = "https://api.elevenlabs.io/v1/voices"

# Headers for the request
headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Accept": "application/json"
}

# Send GET request to fetch voices
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    voices = response.json()["voices"]
    # Print the list of voices with their IDs
    for voice in voices:
        print(f"Voice Name: {voice['name']}, Voice ID: {voice['voice_id']}")
        print()
else:
    print(f"Failed to fetch voices: {response.status_code} - {response.text}")
