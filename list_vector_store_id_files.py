import requests
import os
from dotenv import load_dotenv

# Set your OpenAI API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define the vector store ID
vector_store_id = "vs_JM1dTqQtLHpkE5HSdwzh22C8"  # Replace with your actual vector store ID

# Define the endpoint and headers
url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}/files"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v2"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    files = response.json()  # Parse JSON response
    print(response.text)  # Output the list of files
else:
    print(f"Error: {response.status_code} - {response.text}")