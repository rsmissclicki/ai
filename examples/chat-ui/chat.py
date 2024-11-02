import os
import requests
import streamlit as st
import sys
import yaml
from dotenv import load_dotenv, find_dotenv

sys.path.append("../../../aisuite")
from aisuite.client import Client

# Configure Streamlit to use wide mode and hide the menu
st.set_page_config(layout="wide", menu_items={})

# Add heading with padding
st.markdown(
    "<div style='padding-top: 1rem;'><h2 style='text-align: center; color: #ffffff;'>Chat & Compare LLM responses</h2></div>",
    unsafe_allow_html=True,
)

# Add this near the top of the file, after st.set_page_config
st.markdown(
    """
    <style>
        /* Hide Streamlit's default top bar */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Add custom checkbox label size */
        .stCheckbox label    p {
            font-size: 14px !important;
        }
        
        /* Add custom select box content size */
        .stSelectbox div div div {
            font-size: 14px !important;
        }
        
        /* Add custom button text size */
        .stButton button {
            font-size: 14px !important;
        }
        
        /* Style for the text area - both normal and focused states */
        .stTextArea textarea {
            border-color: #333333 !important;
            box-shadow: none !important;
        }
        
        .stTextArea textarea:focus {
            border-color: #1E90FF !important;
            box-shadow: 0 0 0 1px #1E90FF !important;
        }
        
        #text_area_1:focus {
            border-color: #0066ff !important;
            box-shadow: 0 0 0 1px #0066ff !important;
        }
        
        /* Remove top padding/margin */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            margin-top: 0rem;
        }

        /* Remove padding from the app container */
        .appview-container {
            padding-top: 0rem;
        }
        
        /* Custom CSS for scrollable chat container */
        .chat-container {
            height: 600px;
            overflow-y: auto !important;
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }
        
        /* Ensure the container takes full width */
        .stMarkdown {
            width: 100%;
        }
        
        /* Style for chat messages to ensure they're visible */
        .chat-message {
            margin: 10px 0;
            padding: 10px;
        }
        #text_area_1 {
            min-height: 50px !important;
        } 
    </style>
""",
    unsafe_allow_html=True,
)

# Load configuration and initialize aisuite client
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
configured_llms = config["llms"]
load_dotenv(find_dotenv())
client = Client()


# Function to display chat history
def display_chat_history(chat_history, model_name):
    for message in chat_history:
        role_display = "User" if message["role"] == "user" else model_name
        role = "user" if message["role"] == "user" else "assistant"
        if role == "user":
            with st.chat_message(role, avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message(role, avatar="🤖"):
                st.write(message["content"])


# Helper function to query each LLM
def query_llm(model_config, chat_history):
    print(f"Querying {model_config['name']} with {chat_history}")
    try:
        model = model_config["provider"] + ":" + model_config["model"]
        response = client.chat.completions.create(model=model, messages=chat_history)
        print(
            f"Response from {model_config['name']}: {response.choices[0].message.content}"
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error querying {model_config['name']}: {e}")
        return "Error with LLM response."


# Initialize session states
if "chat_history_1" not in st.session_state:
    st.session_state.chat_history_1 = []
if "chat_history_2" not in st.session_state:
    st.session_state.chat_history_2 = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "use_comparison_mode" not in st.session_state:
    st.session_state.use_comparison_mode = False

# Top Section - Controls
col1, col2 = st.columns([1, 2])
with col1:
    st.session_state.use_comparison_mode = st.checkbox(
        "Enable Comparison Mode", value=True
    )

# Move LLM selection below comparison mode checkbox - now in columns
llm_col1, llm_col2 = st.columns(2)
with llm_col1:
    selected_model_1 = st.selectbox(
        "Choose LLM Model 1",
        [llm["name"] for llm in configured_llms],
        key="model_1",
        index=0 if configured_llms else 0,
    )
with llm_col2:
    if st.session_state.use_comparison_mode:
        selected_model_2 = st.selectbox(
            "Choose LLM Model 2",
            [llm["name"] for llm in configured_llms],
            key="model_2",
            index=1 if len(configured_llms) > 1 else 0,
        )

# Display Chat Histories first, always
# Middle Section - Display Chat Histories
if st.session_state.use_comparison_mode:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<span style='font-size: 14px'>Chat with LLM 1: {selected_model_1}</span>",
            unsafe_allow_html=True,
        )
        chat_container = st.container(height=500)
        with chat_container:
            display_chat_history(st.session_state.chat_history_1, selected_model_1)
    with col2:
        st.markdown(
            f"<span style='font-size: 14px'>Chat with LLM 2: {selected_model_2}</span>",
            unsafe_allow_html=True,
        )
        chat_container = st.container(height=500)
        with chat_container:
            display_chat_history(st.session_state.chat_history_2, selected_model_2)
else:
    st.markdown(
        f"<span style='font-size: 14px'>Chat with LLM: {selected_model_1}</span>",
        unsafe_allow_html=True,
    )
    chat_container = st.container(height=500)
    with chat_container:
        display_chat_history(st.session_state.chat_history_1, selected_model_1)

# Bottom Section - User Input
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    user_query = st.text_area(
        label="Enter your query",
        label_visibility="collapsed",
        placeholder="Enter your query...",
        key="query_input",
        height=80,
    )

    # Override st-e9 min-height for text area and add blue focus border
    st.markdown(
        """
        <style>
        #text_area_1 {
            min-height: 50px !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


with col2:
    send_button = False  # Initialize send_button
    if st.session_state.is_processing:
        st.markdown("Processing... ⏳")
    else:
        send_button = st.button("Send Query", use_container_width=True)

with col3:
    if st.button("Reset Chat", use_container_width=True):
        st.session_state.chat_history_1 = []
        st.session_state.chat_history_2 = []
        st.rerun()

# Handle send button click and processing
if send_button and user_query and not st.session_state.is_processing:
    # Set processing state
    st.session_state.is_processing = True

    # Append user's message to chat histories first
    st.session_state.chat_history_1.append({"role": "user", "content": user_query})
    if st.session_state.use_comparison_mode:
        st.session_state.chat_history_2.append({"role": "user", "content": user_query})

    st.rerun()

# Handle the actual processing
if st.session_state.is_processing and user_query:
    # Query the selected LLM(s)
    model_config_1 = next(
        llm for llm in configured_llms if llm["name"] == selected_model_1
    )
    response_1 = query_llm(model_config_1, st.session_state.chat_history_1)
    st.session_state.chat_history_1.append({"role": "assistant", "content": response_1})

    if st.session_state.use_comparison_mode:
        model_config_2 = next(
            llm for llm in configured_llms if llm["name"] == selected_model_2
        )
        response_2 = query_llm(model_config_2, st.session_state.chat_history_2)
        st.session_state.chat_history_2.append(
            {"role": "assistant", "content": response_2}
        )

    # Reset processing state
    st.session_state.is_processing = False
    st.rerun()
