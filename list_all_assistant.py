import aiohttp
import asyncio

api_key = "sk-proj-ZzVlrkW0MQFLEQMySCERT3BlbkFJZrOlcamn3duS2FBPv4Y0"

async def list_assistants():
    url = "https://api.openai.com/v1/assistants"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # print("Response data:", data)  # 打印返回的數據
                return data
            else:
                print(f"Failed to list assistants. Status code: {response.status}")
                response_text = await response.text()
                # print(f"Response: {response_text}")
                return None

async def main():
    assistants = await list_assistants()
    if assistants:
        # 這裡要檢查一下assitants的結構
        if isinstance(assistants, list):
            for assistant in assistants:
                print(f"Assistant ID: {assistant['id']}, Name: {assistant['name']}")
        else:
            print(f"Unexpected data format: {assistants}")

asyncio.run(main())