import os
import requests
import json
from dotenv import load_dotenv

def test_direct_api():
    """Test the Gemini API directly using requests."""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    print(f"Testing with API key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Hello, this is a test."
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "No text found")
            print(f"API Response: {text[:100]}...")
            print("API test succeeded!")
        else:
            print(f"API Error: {response.text}")
    except Exception as e:
        print(f"Exception during API call: {str(e)}")

if __name__ == "__main__":
    test_direct_api()
