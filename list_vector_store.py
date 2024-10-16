import requests
import os
from dotenv import load_dotenv

# Set your OpenAI API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define the endpoint and headers
url = "https://api.openai.com/v1/vector_stores"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v2"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    vector_stores = response.json()  # Parse JSON response
    print(vector_stores)  # Output the vector stores
else:
    print(f"Error: {response.status_code} - {response.text}")