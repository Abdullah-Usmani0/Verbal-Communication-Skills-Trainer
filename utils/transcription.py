import shutil
import subprocess
import os
from models.model_loader import load_whisper_model

def transcribe_audio(file_path):
    """Transcribes an audio file using Whisper."""
    model_whisper = load_whisper_model()

    # Ensure FFmpeg is available
    if not shutil.which("ffmpeg"):
        return "Error: FFmpeg not found! Please install FFmpeg and add it to your system PATH."

    # Convert file format if necessary
    converted_file = file_path.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-i", file_path, converted_file, "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Transcribe using Whisper
    try:
        result = model_whisper.transcribe(converted_file)
        return result["text"]
    except Exception as e:
        return f"Error during transcription: {e}"
