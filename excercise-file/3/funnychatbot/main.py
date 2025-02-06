import os
import openai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your OpenAI key is stored in the environment

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"
MESSAGE_SYSTEM = "You are a helpful assistant."


# Moderate function to check for inappropriate content
def moderate(user_input):
    response = openai.Moderation.create(input=user_input)
    return response["results"][0]["flagged"]

# Function to generate chat completions
def generate_chat_completion(messages):
    try:
        completion = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=messages,
            temperature=0.7,
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
def main():
    st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
    st.title("🤖 AI Chatbot")

    # Sidebar Menu
    st.sidebar.title("Menu")
    mode = st.sidebar.radio("Select Mode", ["Normal Chat", "Funny Chat", "Exit"])

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": MESSAGE_SYSTEM}]

    # Display chat history at the start
    display_chat()

    # Chat Modes
    if mode == "Normal Chat":
        st.header("Normal Chat")
        user_input = st.text_input("You:", placeholder="Type your message here...")
        if user_input:
            if moderate(user_input):
                st.error("Your message has been flagged for moderation. Please avoid inappropriate language.")
            else:
                # Add user input to messages
                st.session_state.messages.append({"role": "user", "content": user_input})
                # Get chatbot response
                response = generate_chat_completion(st.session_state.messages)
                # Add response to messages
                st.session_state.messages.append({"role": "assistant", "content": response})
                # Display chat history
                display_chat()

    elif mode == "Funny Chat":
        st.header("Funny Chat")
        st.write("This mode will give humorous replies.")
        user_input = st.text_input("You:", placeholder="Type something funny...")
        if user_input:
            if moderate(user_input):
                st.error("Your message has been flagged for moderation. Please avoid inappropriate language.")
            else:
                # Add user input to messages with a "funny" system role
                st.session_state.messages.append({"role": "user", "content": user_input})
                funny_system_message = {"role": "system", "content": "You are a funny assistant!"}
                response = generate_chat_completion([funny_system_message] + st.session_state.messages)
                # Add response to messages
                st.session_state.messages.append({"role": "assistant", "content": response})
                # Display chat history
                display_chat()

    elif mode == "Exit":
        st.sidebar.success("Thank you for using the chatbot!")
        st.stop()

# Function to display chat history
def display_chat():
    st.markdown("### Chat History")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"**AI:** {msg['content']}")

if __name__ == "__main__":
    main()
