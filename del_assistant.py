import requests
from dotenv import load_dotenv
import os

load_dotenv()

assistant_id=""
my_key = os.getenv('OPENAI_API_KEY')

url = "https://api.openai.com/v1/assistants/{assistant_id}"
headers = {
    "Authorization": f"Bearer {my_key}",
    "OpenAI-Beta": "assistants=v2"
}

response = requests.delete(url, headers=headers)
if response.status_code == 200:
    print("Assistant deleted successfully.")
else:
    print(f"Failed to delete assistant: {response.status_code}, {response.text}")