import os
from openai import OpenAI
from dotenv import load_dotenv
import time

# 載入環境變數
load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=my_key)

# 緩存 Assistant 物件
_cached_assistant = None

def get_assistant():
    print('get assistant...')
    global _cached_assistant
    if _cached_assistant:
        print('exist! -> ', _cached_assistant)
        return _cached_assistant

    try:
        assistants = client.beta.assistants.list(order="desc", limit=100)
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

def add_message_to_thread(thread_id, user_question):
    print('add_message_to_thread...')
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_question
    )
    return message

def get_answer(assistant_id, thread):
    print("Thinking...")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # 等待運行完成
    while True:
        run_info = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_info.status == "completed":
            print(f"Run completed")
            break
        elif run_info.status == "failed":
            print(f"Run failed: {run_info.last_error}")
            return None
        print("Waiting 1sec...")
        time.sleep(1)

    print("All done...")
    messages = client.beta.threads.messages.list(thread.id)
    message_content = messages.data[0].content[0].text.value
    return message_content

def assist(user_question):
    try:
        assistant = get_assistant()
        if not assistant:
            return "Error: Unable to get assistant. Please try again later."

        thread = client.beta.threads.create()
        add_message_to_thread(thread.id, user_question)
        message_content = get_answer(assistant.id, thread)
        return message_content if message_content else "An error occurred while processing your request."
    except Exception as e:
        return f"An error occurred: {str(e)}"

