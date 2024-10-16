import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=my_key)

def get_assistant():
    assistants = client.beta.assistants.list(order="desc", limit=100)
    existing_assistant = next((a for a in assistants.data if a.name == "Chat Cancerfree"), None)
    return existing_assistant
        
def list_uploaded_files():
    assistant = get_assistant()
    all_files = client.files.list()
    assistant_files = [file for file in all_files.data if file.purpose == "assistants"]
    return [{"id": file.id, "name": file.filename} for file in assistant_files]

def delete_file(file_id):
    try:
        response = client.files.delete(file_id)
        if response.deleted:
            print(f"Deleted file: {file_id}")
            return {"status": "success", "message": f"File {file_id} deleted successfully"}
        else:
            print(f"Failed to delete file: {file_id}")
            return {"status": "error", "message": f"Failed to delete file {file_id}"}
    except Exception as e:
        print(f"Failed to delete file: {file_id}. Error: {str(e)}")
        return {"status": "error", "message": f"Failed to delete file. Error: {str(e)}"}

def delete_all_files():
    files = list_uploaded_files()
    for file in files:
        delete_file(file['id'])

# 如果需要测试
# print(list_uploaded_files())
# delete_file('file-tdskYbuVlNkxe8jVddYU61vy')