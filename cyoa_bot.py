from mistralai import Mistral
import streamlit as st

# Initialize the Mistral client with the API key from secrets
client = Mistral(api_key=st.secrets["MISTRAL_API_KEY"])

def run_conversation(messages, model_id):
    """Run a conversation with the model"""
    response = client.chat.complete(
        model=model_id,
        messages=messages
    )
    return response.choices[0].message.content

# Streamlit interface
st.title("Educational Adventure Bot 🎓")
st.write("Welcome to your personalized learning journey! Choose a subject and start exploring.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are an educational choose-your-own-adventure guide. You MUST always stop after presenting choices to wait for user input. Never continue the story without user selection."
        }
    ]

# Display chat history
for message in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if prompt := st.chat_input("What would you like to learn about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        try:
            response = run_conversation(
                st.session_state.messages,
                "ft:open-mistral-7b:f00b4002:20241120:78b6c5a8"  # Your model ID
            )
            st.write(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add a reset button
if st.button("Start New Adventure"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are an educational choose-your-own-adventure guide. You MUST always stop after presenting choices to wait for user input. Never continue the story without user selection."
        }
    ]
    st.rerun()