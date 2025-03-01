import whisper
from langchain_ollama import ChatOllama
import functools
import streamlit as st

# ---------------------------
# Load Whisper Model (Speech-to-Text)
# ---------------------------
@st.cache_resource(show_spinner=True)
def load_whisper_model():
    """Load the Whisper ASR model (cached to prevent reloading)."""
    return whisper.load_model("base")

# ---------------------------
# Load LLM Model (Ollama-based)
# ---------------------------
@st.cache_resource(show_spinner=False)
def load_ollama_model(model_name="mistral"):
    """Load the selected LLM model (cached for efficiency)."""
    return ChatOllama(model=model_name)
