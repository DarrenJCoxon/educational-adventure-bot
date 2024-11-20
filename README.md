## A Complete Guide Using Mistral AI and Streamlit

This guide will walk you through creating a fine-tuned chatbot for any purpose. We'll use an educational Choose Your Own Adventure bot as our example, but the principles apply to any fine-tuned chatbot.

## Download software requirements

You will need the following installed:

- Python 3 - https://www.python.org/downloads/
- VS Code - https://code.visualstudio.com/
- Git - https://git-scm.com/
- Github account to store the code - https://github.com

## Part 1: Planning Your Chatbot

1. Define Your Bot's Purpose
    - What specific task will your bot perform?
    - What makes it different from a general-purpose chatbot?
    - Example: Our CYOA bot provides interactive educational experiences with multiple choice paths
2. Plan the Conversation Flow
    - How should the bot respond?
    - What consistent patterns should it follow?
    - Example: Our bot follows this pattern:
        - Present educational content
        - Offer multiple choices
        - Track progress
        - Wait for user input

## Part 2: Creating Training Data

1. Create a JSONL file for training data. Each line should be a complete JSON object representing a conversation:

```
{"messages":[
    {"role":"system","content":"Your system prompt describing the bot's role"},
    {"role":"user","content":"Example user input"},
    {"role":"assistant","content":"Example bot response"}
]}
```

1. Key Requirements:
    - Minimum 8 training examples
    - Each example should demonstrate desired behavior
    - Include system prompts that clearly define behavior
    - Include diverse scenarios

Example for CYOA bot:

```
{"messages":[
    {"role":"system","content":"You are an educational choose-your-own-adventure guide. You MUST always stop after presenting choices to wait for user input."},
    {"role":"user","content":"I'd like to learn about chemistry."},
    {"role":"assistant","content":"Welcome to your Chemistry Adventure! 🧪\\n\\nLearning Objective: Understanding the fundamental building blocks of matter.\\n\\nYou're in a state-of-the-art chemistry lab. Where would you like to start?\\n\\nA) Atomic Structure Lab\\nB) Element Collection\\nC) Molecule Maker\\n\\nPlease choose A, B, or C to continue."}
]}
```

## Part 3: Fine-tuning Your Model

1. Go to [platform.mistral.ai](http://platform.mistral.ai/)
2. Create an account if needed
3. Navigate to "Fine-tune model"
4. Upload your training data:
    - Click "Add file" under "Training datasets"
    - Upload your JSONL file
    - Verify file is accepted (minimum 8 examples)
5. Configure Training Parameters:
    - Base model: Usually start with Mistral 7B
    - Learning rate: 0.0001 (default)
    - Epochs: 10 (adjust based on results)
6. Start Training:
    - Click "Next"
    - Review settings
    - Start fine-tuning
    - Save your model ID when training completes
7. Create an API key
    - Select API keys
    - Create a new API key
    - Copy the key and save it somewhere safe - you will not have access to it again

## Part 4: Creating the Chat Interface

1. Set Up Project:

```bash
mkdir chatbot_project
cd chatbot_project
mkdir .streamlit
```

1. Install Required Packages:

```bash
pip3 install mistralai streamlit
```

1. Create Secrets File (.streamlit/secrets.toml):

```toml
MISTRAL_API_KEY = "your_api_key_here"
```

1. Create App File ([app.py](http://app.py/)). Change “your_model_id_here” to your model ID (including speech marks). It will look something like this, and you’ll find it on the fine-tuned model page: “ft:open-mistral-7b:f00c4012:20241120:78b6c5b7”.

```python
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
                "your_model_id_here"  # Your model ID
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
```

## Part 5: Testing and Deployment

### 1. Creating .gitignore

First, create a `.gitignore` file in your project root:

```bash
touch .gitignore
```

Add these contents to `.gitignore`:

```
# Streamlit secrets
.streamlit/secrets.toml
```

## 2. Preparing for Deployment

1. Create a GitHub Repository:
    - Go to [github.com](http://github.com/)
    - Create a new repository with the same name as your local project
    - [D](http://readme.md/)o not choose READ ME

### **Step 3: Push Your Local Project to GitHub**

1. **Initialize Git in Your Project Directory**:
    
    Open your terminal or command prompt, navigate to your project directory, and run:
    
    ```bash
    git init
    ```
    
2. **Add Remote Repository**:
    
    ```bash
    git remote add origin https://github.com/your_username/your_project_name.git
    ```
    
    - Replace `your_username` with your GitHub username and your_project_name with your project name
    - Ensure the URL matches the one provided in your newly created GitHub repository.
3. **Add Files to Git**:
    
    ```bash
    git add .
    ```
    
4. **Commit Your Changes**:
    
    ```bash
    git commit -m "Initial commit"
    ```
    
5. **Push to GitHub**:
    
    ```bash
    git branch -M main
    git push -u origin main
    ```
    
    - You may be prompted to enter your GitHub credentials and set up a token for authentication (passwords no longer work).

## 3. Deploying to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with GitHub
3. Select your repository
4. Deploy the app

## 4. Setting Up Secrets in Streamlit Cloud

1. Go to your deployed app settings:
    - Click on the three dots menu (⋮) next to your app
    - Select "Settings"
2. Navigate to Secrets section:
    - Find "Secrets" in the left sidebar
    - Click "Edit Secrets"
3. Add your secret:

```toml
MISTRAL_API_KEY = "your_api_key_here"

```

Note: The secrets format in Streamlit Cloud must match exactly what you have in your local `.streamlit/secrets.toml` file.

## 5. Verifying Deployment

1. Check your app is running:
    - Visit your app's URL
    - Test basic functionality
    - Verify API connection
2. Monitor logs:
    - Click "Manage app" in Streamlit Cloud
    - Check "Logs" for any errors

## 6. Updating Your App

1. Make changes locally and test
2. Push changes to GitHub:

```bash
git add .
git commit -m "Description of changes"
git push
```

1. Streamlit Cloud will automatically redeploy
