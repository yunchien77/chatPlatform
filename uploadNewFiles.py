import requests
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=my_key)

vector_store_id = os.getenv('VECTOR_STORE_ID')

def get_vector_store():
    url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}"
    headers = {
        "Authorization": f"Bearer {my_key}",
        "OpenAI-Beta": "assistants=v2"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:  
        vector_store_info = response.json()
        print("Vector Store Info:", vector_store_info)
        return vector_store_info
    else:
        print(f"Failed to get vector store info. Status: {response.status_code}, Response: {response.text()}")
        return None

def upload_folder(folder_path):
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not file_paths:
        print("No documents found to upload.")
        return

    # Get vector store information before uploading files
    get_vector_store()

    file_streams = [open(path, "rb") for path in file_paths]
    
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )

    for file_stream in file_streams:
        file_stream.close()

    return file_batch

# Example usage:
# upload_folder("/path/to/your/folder")
