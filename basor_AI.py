import google.generativeai as genai
from dotenv import load_dotenv
import os
import discord
import requests
import json
import threading
import time
from flask import Flask

# Load environment variables
load_dotenv()

# Setup Discord client
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

# Get API keys and tokens
basor = os.getenv('BASOR_TOKEN')
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Debug print to verify API key (remove in production)
print(f"API Key loaded: {gemini_api_key[:5]}...{gemini_api_key[-5:] if gemini_api_key else 'None'}")

# Configure Gemini API
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Initialize Flask app for keep-alive mechanism
app = Flask(__name__)

@app.route('/')
def home():
    return "Basor AI is running!"

@app.route('/health')
def health():
    return "OK", 200

def test_gemini_api():
    """Test the Gemini API directly to verify the key works."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Hello, testing the API connection.")
        return True, "API connection successful"
    except Exception as e:
        return False, f"API test failed: {str(e)}"

def direct_gemini_request(prompt):
    """Make a direct request to the Gemini API without the client library."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "No response")
    else:
        return f"Error: {response.status_code} - {response.text}"

def split_message(message, max_length=2000):
    """Split a message into chunks of a specified maximum length."""
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

# Keep-alive function that pings our own app
def keep_alive():
    app_url = os.getenv('APP_URL', 'http://localhost:8000')
    while True:
        try:
            response = requests.get(f"{app_url}/health")
            print(f"Keep-alive ping sent, status: {response.status_code}")
        except Exception as e:
            print(f"Keep-alive error: {str(e)}")
        # Sleep for 10 minutes before the next ping
        time.sleep(600)  # 600 seconds = 10 minutes

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # Test the API on startup
    success, message = test_gemini_api()
    print(f"API Test: {message}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!halo basor'):
        await message.channel.send('waalikumsalam, saya basor AI')
    
    if message.content.startswith('!bye'):
        await message.channel.send('Untuk progress tidak perlu ke kelas, langsung k ruang dosen sesuai jadwal perkuliahan.')
    
    if message.content.startswith('!basor'):
        question = message.content[len('!basor '):]
        await message.channel.send(f"Processing your question: {question}")
        
        try:
            # Try using the client library first
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(question)
                response_text = response.text
            except Exception as e:
                # If client library fails, try direct API request
                print(f"Client library failed: {e}")
                await message.channel.send(f"Using fallback method...")
                response_text = direct_gemini_request(question)
            
            # Split the response into chunks if it's too long
            for chunk in split_message(response_text):
                await message.channel.send(chunk)
        except Exception as e:
            await message.channel.send(f"Sorry, I couldn't generate a response. Error: {str(e)}")

# Start the keep-alive thread
def start_keep_alive():
    thread = threading.Thread(target=keep_alive)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_keep_alive()
    client.run(token=basor)