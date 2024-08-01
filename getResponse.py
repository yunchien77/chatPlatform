import openai
#from google.cloud import aiplatform
#from vertexai.language_models import ChatModel
#import anthropic

openai.api_key = 'sk-proj-ZzVlrkW0MQFLEQMySCERT3BlbkFJZrOlcamn3duS2FBPv4Y0'

def get_openai_completions(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    return result
'''
def get_gemini_response(prompt, model="gemini-1.0-pro"):
    chat_model = ChatModel.from_pretrained(model)
    chat = chat_model.start_chat()
    response = chat.send_message(prompt)
    return response.text

client = anthropic.Client(api_key="your-api-key")
def get_claude_response(prompt, model="claude-2.0"):
    response = client.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
        model=model,
        max_tokens_to_sample=300
    )
    return response.completion

if __name__ == "__main__":
    prompt = "Hello, how are you?"
    result = get_openai_completions(prompt)
    print(result)
'''