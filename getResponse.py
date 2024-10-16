from dotenv import load_dotenv
import os
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

def get_gemini_completions(prompt, model):
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key = api_key)

    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)

    print(response.text)
    return response.text


def get_openai_completions(prompt, model="gpt-4o-mini"):
    print(f"model: {model}")

    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "assistant", "content": "You will serve as the chatbot and senior analyst. Your task is to answer user questions."},
        {"role": "user", "content": prompt}]
    )
    # print("my response: ", completion.choices[0].message.content)
    return completion.choices[0].message.content
