import os
from openai import OpenAI, AsyncOpenAI
#import openai
from dotenv import load_dotenv
import asyncio
import time

# env variables
load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

# OpenAI API
client = AsyncOpenAI(api_key=my_key)


async def create_assistant():
    # Create the assistant
    assistant = await client.beta.assistants.create(
        name="Chat Cancerfree",
        instructions="""
        You will serve as the chatbot and senior analyst for CancerFree Biotech. Your task is to answer user questions based on the content of uploaded documents and provide in-depth insights.

        Task Description:
        1. Analyze Questions: Carefully analyze user questions to ensure complete understanding of their needs.
        2. Answer Based on Documents: Provide answers based on the content of the uploaded documents. If the answer comes from the document, please specify the document name and cite the referenced content.
        3. When Unanswerable: If the document content cannot answer the user's question, politely respond with "I don't know."
        4. Maintain Professionalism: Ensure that answers are professional and precise, providing users with accurate information.
        5. Provide Insights: Besides directly answering questions, offer relevant in-depth insights based on the document content to help users better understand the information.
        """,
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}],
        #file_ids=[file.id]
    )
    return assistant

async def add_message_to_thread(thread_id, user_question):
    # Create a message inside the thread
    message = await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= user_question
    )
    return message


async def get_answer(assistant_id, thread):
    print("Thinking...")
    # run assistant
    print("Running assistant...")
    run =  await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # wait for the run to complete
    while True:
        runInfo = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if runInfo.completed_at:
            # elapsed = runInfo.completed_at - runInfo.created_at
            # elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            print(f"Run completed")
            break
        print("Waiting 1sec...")
        time.sleep(1)

    print("All done...")
    # Get messages from the thread
    messages = await client.beta.threads.messages.list(thread.id)
    message_content = messages.data[0].content[0].text.value
    return message_content


if __name__ == "__main__":
    async def main():
        # Colour to print
        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
    
        # Create assistant and thread before entering the loop
        assistant = await create_assistant()
        print("Created assistant with id:" , f"{bcolors.HEADER}{assistant.id}{bcolors.ENDC}")
        thread = await client.beta.threads.create()
        print("Created thread with id:" , f"{bcolors.HEADER}{thread.id}{bcolors.ENDC}")
        
        question = input("How may I help you today? \n")
        if "exit" in question.lower():
            break
            
        # Add message to thread
        await add_message_to_thread(thread.id, question)
        message_content = await get_answer(assistant.id, thread)
        print(f"FYI, your thread is: , {bcolors.HEADER}{thread.id}{bcolors.ENDC}")
        print(f"FYI, your assistant is: , {bcolors.HEADER}{assistant.id}{bcolors.ENDC}")
        print(message_content)
        
        # while True:
        #     question = input("How may I help you today? \n")
        #     if "exit" in question.lower():
        #         break
            
        #     # Add message to thread
        #     await add_message_to_thread(thread.id, question)
        #     message_content = await get_answer(assistant.id, thread)
        #     print(f"FYI, your thread is: , {bcolors.HEADER}{thread.id}{bcolors.ENDC}")
        #     print(f"FYI, your assistant is: , {bcolors.HEADER}{assistant.id}{bcolors.ENDC}")
        #     print(message_content)
        # print(f"{bcolors.OKGREEN}Thanks and happy to serve you{bcolors.ENDC}")
    asyncio.run(main())