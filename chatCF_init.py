import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import time

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

# OpenAI API
client = AsyncOpenAI(api_key=my_key)

async def create_vector_store(file_paths):
    vector_store = await client.beta.vector_stores.create(name="CancerFree Documents")
    
    file_streams = [open(path, "rb") for path in file_paths]
    
    file_batch = await client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    return vector_store

async def create_assistant(vector_store):
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

async def assist():
    # Get all files from the documents folder
    documents_folder = "documents"
    file_paths = [os.path.join(documents_folder, f) for f in os.listdir(documents_folder) if os.path.isfile(os.path.join(documents_folder, f))]
    
    if not file_paths:
        return "No documents found to answer the question."
    # Create vector store with documents
    vector_store = await create_vector_store(file_paths)

    # Create assistant and thread
    assistant = await create_assistant(vector_store)
    print("assistant create sucessfully!")

asyncio.run(assist())