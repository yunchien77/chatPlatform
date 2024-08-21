import os
from openai import OpenAI, AsyncOpenAI
import openai
from dotenv import load_dotenv
import asyncio
import time
import aiohttp

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

client = AsyncOpenAI(api_key=my_key)

async def get_assistant():
    assistants = await client.beta.assistants.list(order="desc", limit=100)
    
    existing_assistant = next((a for a in assistants.data if a.name == "Chat Cancerfree"), None)
    return existing_assistant
        
async def list_uploaded_files():
    assistant = await get_assistant()
    all_files = await client.files.list()
    assistant_files = [file for file in all_files.data if file.purpose == "assistants"]
    # return assistant_files
    return [{"id": file.id, "name": file.filename} for file in assistant_files]

async def delete_file(file_id):
    try:
        url = f"https://api.openai.com/v1/files/{file_id}"
        headers = {
            "Authorization": f"Bearer {my_key}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.status == 200:
                    print(f"Deleted file")
                else:
                    print(f"Failed to delete file")
    except Exception as e:
        print(f"Failed to delete file. Error: {str(e)}")


async def delete_all_files():
    files = await list_uploaded_files()
    for file in files:
        try:
            url = f"https://api.openai.com/v1/files/{file['id']}"
            headers = {
                "Authorization": f"Bearer {my_key}"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as response:
                    if response.status == 200:
                        print(f"Deleted file: {file['name']}")
                    else:
                        print(f"Failed to delete file: {file['name']}. Error: {response.status}")
        except Exception as e:
            print(f"Failed to delete file: {file['name']}. Error: {str(e)}")

#print(asyncio.run(list_uploaded_files()))

asyncio.run(delete_file('file-tdskYbuVlNkxe8jVddYU61vy'))
# 
# 