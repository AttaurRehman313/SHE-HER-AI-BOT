import streamlit as st
import requests

# Set up the app's title
st.title("SHE-HER-AI-BOT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to send user query to Flask API and get a response
def get_response(query):
    try:
        response = requests.post('https://minervahubspot.hamzaworld.com/chat', json={'query': query})
        if response.status_code == 200:
            return response.text  # The response might be HTML
        else:
            return "Sorry, there was an error."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Function to display a chat message with custom styles for user and assistant
def display_message(role, content):
    if role == "user":
        st.markdown(f"""
            <div style="text-align: right;  color: black; background-color: #8db698; padding: 10px; border-radius: 10px; margin: 10px 0; width: fit-content; float: right; clear: both;">
                {content}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="text-align: left;  color: black; background-color: #bddabb; padding: 10px; border-radius: 10px; margin: 10px 0; width: fit-content; float: left; clear: both;">
                {content}
            </div>
            """, unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# Accept user input
if prompt := st.chat_input("Enter your query..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container (aligned to the right)
    display_message("user", prompt)
    
    # Show spinner while the response is being fetched
    with st.spinner("loading..."):
        # Get the AI response from the Flask API
        ai_response = get_response(prompt)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Display AI response in chat message container (aligned to the left)
    display_message("assistant", ai_response)
