import requests

assistant_id=""

url = "https://api.openai.com/v1/assistants/{assistant_id}"
headers = {
    "Authorization": "Bearer sk-proj-ZzVlrkW0MQFLEQMySCERT3BlbkFJZrOlcamn3duS2FBPv4Y0",
    "OpenAI-Beta": "assistants=v2"
}

response = requests.delete(url, headers=headers)
if response.status_code == 200:
    print("Assistant deleted successfully.")
else:
    print(f"Failed to delete assistant: {response.status_code}, {response.text}")