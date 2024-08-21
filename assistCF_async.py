import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

client = AsyncOpenAI(api_key=my_key)

# 緩存 Assistant 物件
_cached_assistant = None

async def get_assistant():
    print('get assistant...')
    global _cached_assistant
    if _cached_assistant:
        print('exist! -> ', _cached_assistant)
        return _cached_assistant

    try:
        assistants = await client.beta.assistants.list(order="desc", limit=100)
        print('assistants get!')
        print(assistants)
        existing_assistant = next((a for a in assistants.data if a.name == "Chat Cancerfree"), None)
        if existing_assistant:
            _cached_assistant = existing_assistant
            print('cancerfree chat assistant get!')
            return existing_assistant
    except Exception as e:
        print(f"Error getting assistant: {e}")
    return None

# async def get_assistant():
#     print('get assistant...')
#     assistants = await client.beta.assistants.list(order="desc", limit=100)
#     print('assistants get!')
#     print(assistants)
#     existing_assistant = next((a for a in assistants.data if a.name == "Chat Cancerfree"), None)
#     print('cancerfree chat assistant get!')
#     return existing_assistant

# asyncio.run(get_assistant())

async def add_message_to_thread(thread_id, user_question):
    print('add_message_to_thread...')
    message = await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= user_question
    )
    return message

async def get_answer(assistant_id, thread):
    print("Thinking...")
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # wait for the run to complete
    while True:
        runInfo = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if runInfo.status == "completed":
            print(f"Run completed")
            break
        elif runInfo.status == "failed":
            print(f"Run failed: {runInfo.last_error}")
            return None
        print("Waiting 1sec...")
        await asyncio.sleep(1)

    print("All done...")
    messages = await client.beta.threads.messages.list(thread.id)
    message_content = messages.data[0].content[0].text.value
    return message_content


# async def assist(user_question):
#     try:
#         assistant = await get_assistant()
#         print('assistant get back!')
#         if not assistant:
#             return "Error: Unable to get assistant. Please try again later."

#         thread = await client.beta.threads.create()
#         print('thresds create!')
#         print(thread)
#         await add_message_to_thread(thread.id, user_question)
#         message_content = await get_answer(assistant.id, thread)
#         return message_content if message_content else "An error occurred while processing your request."
#     except Exception as e:
#         return f"An error occurred: {str(e)}"


async def assist(user_question):
    try:
        assistant = await get_assistant()
        if not assistant:
            return "Error: Unable to get assistant. Please try again later."

        thread = await asyncio.wait_for(client.beta.threads.create(), timeout=30)
        await add_message_to_thread(thread.id, user_question)
        message_content = await asyncio.wait_for(get_answer(assistant.id, thread), timeout=60)
        return message_content if message_content else "An error occurred while processing your request."
    except asyncio.TimeoutError:
        return "Error: The request timed out. Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"

