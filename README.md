# Verbal Communication Skills Trainer with Open-Source LLM

This repository contains a wrapper application around an open-source LLM that helps learners improve their verbal communication skills. The application supports chat and voice interactions, training modules (Impromptu Speaking, Storytelling, Conflict Resolution), and presentation assessments with detailed feedback.

> **Note:** This project uses **Ollama** for downloading and running the LLM, and **Whisper** for speech-to-text conversion. By default, it uses **Mistral-7B**.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Code Structure](#architecture--code-structure)
- [Setup Instructions](#setup-instructions)
  - [Environment Setup](#environment-setup)
  - [Downloading the LLM via Ollama](#downloading-the-llm-via-ollama)
  - [Installing FFmpeg for Whisper](#installing-ffmpeg-for-whisper)
- [Usage](#usage)
  - [Running the Streamlit App](#running-the-streamlit-app)
  - [Using CLI Model Selection](#using-cli-model-selection)
- [Optimization Choices](#optimization-choices)
- [Testing & Use Cases](#testing--use-cases)
- [Further Improvements](#further-improvements)
- [License](#license)

---

## 📖 Overview

This project wraps an open-source LLM (**Mistral-7B** by default) to create an interactive training tool for improving verbal communication skills. It integrates both **text and voice inputs**:

- **Chat Interface:** Allows users to chat with an AI coach.
- **Training Modules:** Includes **Impromptu Speaking, Storytelling, and Conflict Resolution** exercises.
- **Presentation Assessment:** Evaluates **presentation scripts or voice recordings**.

---

## 🔥 Features

- **Model Loading & Caching:**
  - Uses `@st.cache_resource` (Streamlit caching) to **load models only once per session**.
  - Uses `functools.lru_cache` to **cache AI responses for common prompts**.

- **Voice Integration:**
  - Uses **Whisper** for speech-to-text conversion.
  - Converts audio (MP3) to WAV using **FFmpeg**.

- **Configurable & Extensible:**
  - Model selection is configurable via **CLI flags**.
  - Training prompts and evaluation templates are stored in a **configuration file (`config.json`)**.

- **Optimizations:**
  - **Preloading and caching of models** reduce latency.
  - **Response caching** avoids duplicate calls to the LLM.

---

### Project Structure

```bash
verbal-communication-trainer/
│
├── models/
│   └── model_loader.py        # Loads the Whisper and LLM models
│
├── utils/
│   ├── config_loader.py      # Loads configuration and evaluation prompts
│   ├── evaluation.py         # Evaluation functions with response caching
│   └── transcription.py      # Handles audio transcription via Whisper & FFmpeg
│
├── config.json               # Configuration file with prompts and training scenarios
├── main.py                   # Entry point for the Streamlit app with CLI model selection
├── requirements.txt          # Python dependencies
├── Test Samples              #Sample Audio and text file for testing the app  
└── README.md                 # Project documentation   
```

---

## ⚙️ Setup Instructions

### 1️⃣ Environment Setup

#### Create a Virtual Environment
```bash
python -m venv verbal_env
```
Activate the environment:

**Windows:**
```bash
verbal_env\Scripts\activate
```

**Mac/Linux:**
```bash
source verbal_env/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 2️⃣ Downloading the LLM via Ollama
We use **Ollama** to manage and run LLMs. The default model is **Mistral-7B**, chosen for:
- Performance: Balanced size vs. capability
- Availability: Open-source and actively maintained
- Optimization: Compatible with caching strategies

#### Install Ollama
Follow the installation instructions from [ollama.com](https://ollama.com).

#### Download Models
```bash
ollama pull mistral
```
To use a different model (e.g., LLaMA-13B):
```bash
ollama pull llama-13b
```

---

### 3️⃣ Installing FFmpeg for Whisper
**FFmpeg** is required for audio processing.

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org).
2. Extract files and add the `bin` directory to your system PATH.

#### Mac (Homebrew)
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt-get install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

---

## 🚀 Usage

### Running the Streamlit App
```bash
streamlit run main.py -- --model mistral
```
Replace **"mistral"** with your desired model name.

### CLI Model Selection
```bash
streamlit run main.py -- --model llama-13b
```

---

## ⚡ Optimization Choices

- **Model Caching:** Prevents reloading models on every request
- **Response Caching:** Speeds up frequent AI responses
- **Pre-Generated Prompts:** Stored in `config.json` for faster runtime

---

## 🏆 Use Cases

### 1️⃣ Chat Interface
- **Input:** "How do I improve my tone when speaking?"
- **Output:** AI provides tone & clarity feedback

### 2️⃣ Training Modules
- **Impromptu Speaking:** Random prompts with fluency assessment
- **Storytelling:** Engagement & coherence evaluation
- **Conflict Resolution:** Diplomatic response assessment

### 3️⃣ Presentation Assessment
- **Input:** Audio or text scripts
- **Output:** Detailed feedback reports

---

## 🔮 Further Improvements
- Multi-model support
- Enhanced error handling
- Multi-user sessions
- Text-to-Speech (TTS) integration

---

## 📜 License
This project is licensed under the **MIT License**.

