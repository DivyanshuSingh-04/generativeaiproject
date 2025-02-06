import openai
import os
from colorama import Fore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"
messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a response from OpenAI
def generate_response(user_input):
    messages.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(  # Corrected the method call
            model=MODEL_ENGINE,
            messages=messages
        )
        # Add assistant's response to messages
        assistant_message = response.choices[0].message
        messages.append(assistant_message)
        return assistant_message
    except Exception as e:
        return {"content": f"Error: {e}"}

# Main function to handle user interaction
def main():
    print(Fore.CYAN + "Bot: Hello, I am a helpful assistant. Type 'exit' to quit." + Fore.RESET)

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Get a response from the assistant
        message_response = generate_response(user_input)
        print(Fore.CYAN + "Bot: " + message_response["content"] + Fore.RESET)

if __name__ == "__main__":
    main()
