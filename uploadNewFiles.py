# import aiohttp
# import asyncio
# from dotenv import load_dotenv
# import os
# from openai import OpenAI, AsyncOpenAI

# # Load environment variables
# load_dotenv()
# my_key = os.getenv('OPENAI_API_KEY')
# client = AsyncOpenAI(api_key=my_key)

# async def upload_folder(file_paths, vector_store_id):
#     file_streams = [open(path, "rb") for path in file_paths]
#     file_batch = await client.beta.vector_stores.file_batches.upload_and_poll(
#         vector_store_id=vector_store.id, files=file_streams
#     )
#     return vector_store

# if __name__ == "__main__":
#     vector_store_id = "vs_JM1dTqQtLHpkE5HSdwzh22C8"

#     folder_path = "uploads"  # Replace with the path to your folder
#     file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
#     if not file_paths:
#         print("No documents found to upload.")
#     asyncio.run(upload_folder(file_paths, vector_store_id))

import aiohttp
import asyncio
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')
client = AsyncOpenAI(api_key=my_key)

async def get_vector_store(vector_store_id):
    url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}"
    headers = {
        "Authorization": f"Bearer {my_key}",
        "OpenAI-Beta": "assistants=v2"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                vector_store_info = await response.json()
                print("Vector Store Info:", vector_store_info)
                return vector_store_info
            else:
                print(f"Failed to get vector store info. Status: {response.status}, Response: {await response.text()}")

async def upload_folder(file_paths, vector_store_id):
    # Get vector store information before uploading files
    await get_vector_store(vector_store_id)

    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = await client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )
    
    for file_stream in file_streams:
        file_stream.close()
    
    return file_batch

if __name__ == "__main__":
    vector_store_id = "vs_JM1dTqQtLHpkE5HSdwzh22C8"

    folder_path = "uploads"  # Replace with the path to your folder
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not file_paths:
        print("No documents found to upload.")
    else:
        asyncio.run(upload_folder(file_paths, vector_store_id))
