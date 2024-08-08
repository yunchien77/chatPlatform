#import openai
from dotenv import load_dotenv
import os
#from google.cloud import aiplatform
#from vertexai.language_models import ChatModel
#import anthropic

from openai import OpenAI

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=my_key)

# gpt-4o-mini
# gpt-4o-mini-2024-07-18
# gpt-4o
# gpt-4o-2024-05-13
# gpt-4o-2024-08-06
# gpt-4-turbo
# gpt-4-turbo-2024-04-09
# gpt-4-turbo-preview
# gpt-4-0125-preview
# gpt-4-1106-preview
# gpt-4
# gpt-4-0613
# gpt-4-0314
# gpt-3.5-turbo-0125
# gpt-3.5-turbo
# gpt-3.5-turbo-1106
# gpt-3.5-turbo-instruct	



def get_openai_completions(prompt, model="gpt-4o-mini"):
    print(f"model: {model}")
    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "assistant", "content": "You will serve as the chatbot for CancerFree Biotech. Your task is to answer user questions."},
        {"role": "user", "content": prompt}]
    )
    # print("my response: ", completion.choices[0].message.content)
    return completion.choices[0].message.content