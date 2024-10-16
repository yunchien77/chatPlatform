import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

async def list_assistants():
    url = "https://api.openai.com/v1/assistants"
    headers = {
        "Authorization": f"Bearer {my_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # print("Response data:", data)  
                return data
            else:
                print(f"Failed to list assistants. Status code: {response.status}")
                response_text = await response.text()
                # print(f"Response: {response_text}")
                return None

async def main():
    assistants = await list_assistants()
    if assistants:
        print(f"{assistants}")

asyncio.run(main())