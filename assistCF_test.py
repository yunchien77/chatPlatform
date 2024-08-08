import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import time
# If the answer comes from the document, please specify the document name and cite the referenced content.

# env variables
load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

# OpenAI API
client = AsyncOpenAI(api_key=my_key)

async def create_vector_store(file_paths):
    # Create a vector store called "CancerFree Documents"
    vector_store = await client.beta.vector_stores.create(name="CancerFree Documents")
    
    # Ready the files for upload to OpenAI
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = await client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    
    # print(f"Vector store created with status: {file_batch.status}")
    # print(f"File counts: {file_batch.file_counts}")
    return vector_store

async def create_assistant(vector_store):
    # Create the assistant
    assistant = await client.beta.assistants.create(
        name="Chat Cancerfree",
        instructions="""
        You will serve as the chatbot and senior analyst for CancerFree Biotech. Your task is to answer user questions based on the content of uploaded documents and provide in-depth insights.

        Task Description:
        1. Analyze Questions: Carefully analyze user questions to ensure complete understanding of their needs.
        2. Answer Based on Documents: Provide answers based on the content of the uploaded documents. 
        3. When Unanswerable: If the document content cannot answer the user's question, politely respond with "I don't know."
        4. Maintain Professionalism: Ensure that answers are professional and precise, providing users with accurate information.
        5. Provide Insights: Besides directly answering questions, offer relevant in-depth insights based on the document content to help users better understand the information.
        """,
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store.id]
            }
        }
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
    # print("Running assistant...")
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # wait for the run to complete
    while True:
        runInfo = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if runInfo.status == "completed":
            # print(f"Run completed")
            break
        elif runInfo.status == "failed":
            print(f"Run failed: {runInfo.last_error}")
            return None
        # print("Waiting 1sec...")
        await asyncio.sleep(1)

    # print("All done...")
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
    
         # Get all files from the documents folder
        documents_folder = "documents"
        file_paths = [os.path.join(documents_folder, f) for f in os.listdir(documents_folder) if os.path.isfile(os.path.join(documents_folder, f))]
        
        if not file_paths:
            print(f"{bcolors.FAIL}No files found in the documents folder.{bcolors.ENDC}")
            return

        # print(f"Found {len(file_paths)} files in the documents folder:")
        # for path in file_paths:
        #     print(f"- {path}")
        
        # Create vector store with documents
        vector_store = await create_vector_store(file_paths)
        
        # Create assistant and thread before entering the loop
        assistant = await create_assistant(vector_store)
        # print("Created assistant with id:" , f"{bcolors.HEADER}{assistant.id}{bcolors.ENDC}")
        thread = await client.beta.threads.create()
        # print("Created thread with id:" , f"{bcolors.HEADER}{thread.id}{bcolors.ENDC}")
        
    
        question = input("How may I help you today? (Type 'exit' to quit)\n")
        # if "exit" in question.lower():
        #     break
            
        # Add message to thread
        await add_message_to_thread(thread.id, question)
        message_content = await get_answer(assistant.id, thread)
        if message_content:
            # print(f"FYI, your thread is: {bcolors.HEADER}{thread.id}{bcolors.ENDC}")
            # print(f"FYI, your assistant is: {bcolors.HEADER}{assistant.id}{bcolors.ENDC}")
            print(f"{message_content}")
        else:
            print(f"{bcolors.FAIL}Failed to get an answer. Please try again.{bcolors.ENDC}")
        
        # print(f"{bcolors.OKGREEN}Thanks and happy to serve you{bcolors.ENDC}")

    asyncio.run(main())