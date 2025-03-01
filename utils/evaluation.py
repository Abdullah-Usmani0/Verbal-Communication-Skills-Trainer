import functools
from utils.config_loader import load_config
import streamlit as st


# ---------------------------
# Caching for Evaluation Responses (Avoid Reloading Model)
# ---------------------------
@functools.lru_cache(maxsize=128)
def cached_generate_response(prompt):
    """Caches AI responses to avoid redundant computation."""
    return st.session_state.llm.invoke(prompt).content

# ---------------------------
# Load Configuration & State
# ---------------------------
config = load_config()
prompts = config["evaluation_prompts"]

def evaluate_chat(user_message):
    user_message=" ".join([msg for _, msg in st.session_state.chat_history])
    prompt = prompts["chat"].replace("{user_message}", user_message)
    return cached_generate_response(prompt)

def evaluate_impromptu(prompt_text, user_response):
    prompt = (prompts["impromptu_speaking"]
              .replace("{prompt_text}", prompt_text)
              .replace("{user_response}", user_response))
    return cached_generate_response(prompt)

def evaluate_storytelling(user_story):
    prompt = prompts["storytelling"].replace("{user_story}", user_story)
    return cached_generate_response(prompt)

def evaluate_conflict(prompt_text, user_response):
    prompt = (prompts["conflict_resolution"]
              .replace("{prompt_text}", prompt_text)
              .replace("{user_response}", user_response))
    return cached_generate_response(prompt)

def evaluate_presentation(user_input):
    prompt = prompts["presentation"].replace("{user_input}", user_input)
    return cached_generate_response(prompt)
