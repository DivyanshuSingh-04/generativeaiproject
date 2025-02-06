import os
import openai
import tiktoken
from colorama import Fore
from dotenv import load_dotenv

# Load the environment variables - set up the OpenAI API client
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure your API key is loaded

# Set up the model
language_model = "gpt-3.5-turbo"  # Or "gpt-4", depending on the model you want to use

def get_tokens(user_input: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    token_integers = encoding.encode(user_input)
    tokens_usage = len(token_integers)

    tokenized_input = list(
        map(
            lambda x: encoding.decode_single_token_bytes(x).decode("utf-8"),
            encoding.encode(user_input),
        )
    )
    print(f"Encoding: cl100k_base")
    print(f"Total tokens: {tokens_usage}")
    print(f"Tokenized input: {tokenized_input}")
    return tokens_usage


def start():
    print("MENU")
    print("====")
    print("[1]- Ask a question")
    print("[2]- Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        ask()
    elif choice == "2":
        exit()
    else:
        print("Invalid choice")
        start()


def ask():
    """Ask a question and get a response from the model."""
    instructions = (
        "Type your question and press ENTER. Type 'x' to go back to the MAIN menu.\n"
    )
    print(Fore.BLUE + "\n\x1B[3m" + instructions + "\x1B[0m" + Fore.RESET)

    while True:
        user_input = input("Q: ")

        # Exit the loop if user types 'x'
        if user_input.lower() == "x":
            start()
            break  # Exit the loop after returning to the menu
        else:
            # Get the token count
            get_tokens(user_input)

            try:
                # Get chat model completion using openai.ChatCompletion.create
                completion = openai.ChatCompletion.create(
                    model=language_model,
                    messages=[{"role": "user", "content": user_input}],
                    max_tokens=100,
                    temperature=0,
                )
                response = completion["choices"][0]["message"]["content"]
                print(Fore.GREEN + f"A: {response}" + Fore.RESET)
            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Fore.RESET)

            print(Fore.WHITE + "\n------------------------------------------\n" + Fore.RESET)

if __name__ == "__main__":
    start()
