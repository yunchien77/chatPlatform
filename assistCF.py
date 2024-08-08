import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

client = AsyncOpenAI(api_key=my_key)

async def get_assistant():
    assistants = await client.beta.assistants.list(order="desc", limit=100)
    
    existing_assistant = next((a for a in assistants.data if a.name == "Chat Cancerfree"), None)
    return existing_assistant

async def add_message_to_thread(thread_id, user_question):
    message = await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= user_question
    )
    return message

async def get_answer(assistant_id, thread):
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # wait for the run to complete
    while True:
        runInfo = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if runInfo.status == "completed":
            break
        elif runInfo.status == "failed":
            return None

        await asyncio.sleep(1)

    messages = await client.beta.threads.messages.list(thread.id)
    message_content = messages.data[0].content[0].text.value
    return message_content

async def assist(user_question):
    assistant = await get_assistant()

    thread = await client.beta.threads.create()

    await add_message_to_thread(thread.id, user_question)
    message_content = await get_answer(assistant.id, thread)
    
    if message_content:
        return message_content
    else:
        return "An error occurred while processing your request."
