import openai
from dotenv import load_dotenv

load_dotenv
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"
MESSAGE_SYSTEM = "You are a helpful assistant"
messages = [{"role": "system", "content": MESSAGE_SYSTEM}]


def moderate(user_input):
    response = openai.moderation.create(input=user_input)
    return response.result[0].flagged

def generate_chat_completion(user_input,messages):
    flagged = moderate(user_input)
    print(f"Flagged: {flagged}")

    if flagged:
        return ":red [Your comment has een flagged for moderation. Please refrain from using inappropriate language.]"
    completion =  openai.ChatCompletion.create(
        model=MODEL_ENGINE,
        messages=messages,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return completion.choices[0].message.content