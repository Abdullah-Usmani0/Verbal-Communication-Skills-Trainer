import argparse 
import streamlit as st
import random
import os

from models.model_loader import load_whisper_model, load_ollama_model
from utils.transcription import transcribe_audio
from utils.evaluation import evaluate_chat, evaluate_impromptu, evaluate_storytelling, evaluate_conflict, evaluate_presentation
from utils.config_loader import load_config

# ---------------------------
# Load Configuration & State
# ---------------------------
st.set_page_config(page_title="Verbal Communication Skills Trainer", layout="wide")
config = load_config()

# CLI Model Selection (Defaults to Mistral)
parser = argparse.ArgumentParser(description="Run Streamlit app with a selected LLM model.")
parser.add_argument("--model", type=str, default="mistral", help="LLM model to use (e.g., 'mistral', 'llama-13b').")
args, _ = parser.parse_known_args()

# Store Model in Session State
if "model_name" not in st.session_state:
    st.session_state.model_name = args.model

# Load Models
whisper_model = load_whisper_model()
if "llm" not in st.session_state:
    st.session_state.llm = load_ollama_model(st.session_state.model_name)

# ---------------------------
# Helper Function for User Input
# ---------------------------
def get_user_input(input_method):
    """Handles user input: text or voice."""
    if input_method == "Text":
        return st.text_area("Enter your response:", height=150)
    else:
        audio_file = st.file_uploader("Upload your voice recording (wav, mp3, or m4a)", type=["wav", "mp3", "m4a"])
        if audio_file:
            temp_file = "temp_voice_input.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio_file.read())
            transcription = transcribe_audio(temp_file)
            st.success("Transcription Complete!")
            st.write("**Transcribed Text:**", transcription)
            os.remove(temp_file)
            return transcription
        return ""

# ---------------------------
# Streamlit UI
# ---------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #997B2F;
        color: #F0F0F0;s
    }
    .sidebar .sidebar-content, .sidebar p, .sidebar h1, .sidebar h2, .sidebar h3, .sidebar label {
    color: #FFD700 !important; }

    .stButton>button {
        background-color: #FF9800;
        color: white;
        border-radius: 12px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #E68900;
    }
    .stTextArea textarea {
        background-color: #252525;
        color: #FFFFFF;
        border-radius: 8px;
    }
    .stFileUploader > div {
        background-color: #252525;
        color: #F0F0F0;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] * {
        color: #BA6B06 !important;  
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("✨ Verbal Communication Skills Trainer")
st.markdown("""
This application helps you refine your verbal communication skills through AI-driven feedback.
Engage in chat or voice training across various communication scenarios.
""")

st.sidebar.markdown("""
## How It Works
- Select a module from the sidebar.
- Choose an input method: Text or Voice.
- Submit your response and receive AI-based evaluation feedback.

### Modules
- **Chat**: Casual conversation practice.
- **Training Modules**: Impromptu Speaking, Storytelling, Conflict Resolution.
- **Presentation Assessment**: Detailed feedback on structured presentations.
""")

# Sidebar for navigation among modules
module_option = st.sidebar.selectbox("Select Module", ["Chat", "Training Modules", "Presentation Assessment"])


# --- Chat Interface with History ---
if module_option == "Chat":
    st.header("💬 Chat with AI Coach")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_input_method = st.radio("Choose input method", ["Text", "Voice"], key="chat_input")
    user_message = get_user_input(chat_input_method)

    if st.button("Send Message"):
        if user_message:
            with st.spinner("Processing..."):
                # Append user message
                st.session_state.chat_history.append(("User", user_message))
                
                # Get AI response
                response = evaluate_chat(st.session_state.chat_history)

                # Append AI response
                st.session_state.chat_history.append(("AI", response))

    # Display chat history
    for role, message in reversed(st.session_state.chat_history):
        with st.container():
            bg_color = "#252525" if role == "User" else "#333333"
            text_color = "#FFD700" if role == "User" else "#80C0FF"
            
            st.markdown(
                f"""
                <div style="background-color:{bg_color}; padding:10px; border-radius:10px; margin-bottom:5px;">
                    <p style="color:{text_color};"><b>{role}:</b> {message}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# --- Training Modules ---
if "impromptu_prompt" not in st.session_state:
    st.session_state.impromptu_prompt = random.choice(config["impromptu_prompts"])

if "conflict_prompt" not in st.session_state:
    st.session_state.conflict_prompt = random.choice(config["conflict_prompts"])
    
if module_option == "Training Modules":
    st.header("🎯 Training Modules")
    training_choice = st.selectbox("Choose Training Activity", ["Impromptu Speaking", "Storytelling", "Conflict Resolution"])
    training_input_method = st.radio("Choose input method", ["Text", "Voice"], key="training_input")

    if training_choice == "Impromptu Speaking":
            st.subheader("💡 Impromptu Speaking")
            st.info(f"Your Prompt: **{st.session_state.impromptu_prompt}**")

            if st.button("New Prompt"):
                st.session_state.impromptu_prompt = random.choice(config["impromptu_prompts"])
                st.rerun()  # Ensures the updated prompt replaces the old one

            user_response = get_user_input(training_input_method)
            if st.button("Submit Response"):
                if user_response:
                    with st.spinner("Evaluating..."):
                        evaluation = evaluate_impromptu(st.session_state.impromptu_prompt, user_response)
                    st.text_area("Evaluation:", evaluation, height=200)
                else:
                    st.warning("Please provide a response.")

    elif training_choice == "Storytelling":
        st.subheader("📖 Storytelling")
        user_story = get_user_input(training_input_method)
        if st.button("Submit Story"):
            if user_story:
                with st.spinner("Evaluating..."):
                    evaluation = evaluate_storytelling(user_story)
                st.text_area("Evaluation:", evaluation, height=200)
            else:
                st.warning("Please provide a story.")

    elif training_choice == "Conflict Resolution":
        st.subheader("⚔️ Conflict Resolution")
        st.info(f"Scenario: **{st.session_state.conflict_prompt}**")

        if st.button("New Scenario"):
            st.session_state.conflict_prompt = random.choice(config["conflict_prompts"])
            st.rerun()  # Ensures the updated scenario replaces the old one

        user_response = get_user_input(training_input_method)
        if st.button("Submit Response"):
            if user_response:
                with st.spinner("Evaluating..."):
                    evaluation = evaluate_conflict(st.session_state.conflict_prompt, user_response)
                st.text_area("Evaluation:", evaluation, height=200)
            else:
                st.warning("Please provide a response.")

# --- Presentation Assessment ---
if module_option == "Presentation Assessment":
    st.header("📝 Presentation Assessment")
    presentation_input_method = st.radio("Choose input method", ["Text", "Voice"], key="presentation_input")
    user_input = get_user_input(presentation_input_method)
    
    if st.button("Assess Presentation"):
        if user_input:
            with st.spinner("Analyzing..."):
                evaluation = evaluate_presentation(user_input)
            st.text_area("Assessment Report:", evaluation, height=200)
        else:
            st.warning("Please provide presentation content.")

#-----------------------------------------
