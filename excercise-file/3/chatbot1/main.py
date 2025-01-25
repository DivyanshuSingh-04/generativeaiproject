import openai
import os
from dotenv import load_dotenv
from colorama import Fore

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"
MESSAGE_SYSTEM = "You are a helpful assistant"

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is loaded

# Validate API key
if not openai.api_key:
    print("Error: OpenAI API key not found. Please set it in your environment variables.")
    exit()

# Chat history
messages = [{"role": "system", "content": MESSAGE_SYSTEM}]


def generate_chat_completion(user_input):
    """
    Generate a response from the OpenAI API based on user input.
    """
    try:
        # Add user input to the conversation history
        messages.append({"role": "user", "content": user_input})
        
        # Call OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=messages,
        )
        
        # Extract the assistant's reply
        assistant_reply = response.choices[0].message["content"]
        
        # Add assistant reply to the conversation history
        messages.append({"role": "assistant", "content": assistant_reply})
        
        # Display assistant's reply
        print(Fore.GREEN + "AI: " + assistant_reply + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Fore.RESET)


def main():
    """
    Main menu for the chatbot program.
    """
    while True:
        print("\n")
        print("----------------------------------------\n")
        print(" *** 🤖 WELCOME TO THE AI-CHATBOT *** ")
        print("\n----------------------------------------")
        print("\n================* MENU *================\n")
        print("[1]- Start Chat")
        print("[2]- Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            start_chat()
        elif choice == "2":
            print(Fore.CYAN + "Goodbye!" + Fore.RESET)
            exit()
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)


def start_chat():
    """
    Start a new chat session.
    """
    global messages
    print("\nStarting a new chat session. To end the chat, type 'x'.")
    print("---------------------")
    
    # Reset chat history for a new conversation
    messages = [{"role": "system", "content": MESSAGE_SYSTEM}]
    
    while True:
        user_input = input(Fore.WHITE + "You: " + Fore.RESET)
        
        if user_input.lower() == "x":
            print(Fore.CYAN + "\nEnding chat and returning to the main menu.\n" + Fore.RESET)
            break
        elif user_input.strip() == "":
            print(Fore.RED + "Input cannot be empty. Please enter something." + Fore.RESET)
        else:
            generate_chat_completion(user_input)


if __name__ == "__main__":
    main()
