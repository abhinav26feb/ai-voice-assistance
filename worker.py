import asyncio
import subprocess
import os
import tempfile

import edge_tts
import requests
import whisper

whisper_model = whisper.load_model("base")


def speech_to_text(audio_binary):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        temp_audio.write(audio_binary)
        webm_path = temp_audio.name

    wav_path = webm_path.replace(".webm", ".wav")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            webm_path,
            wav_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    result = whisper_model.transcribe(wav_path)

    os.remove(webm_path)
    os.remove(wav_path)

    return result["text"].strip()


def ollama_process_message(user_message):
    """
    Using Ollama instead of OpenAI
    """

    prompt = (
        "Act like a helpful personal assistant. "
        "Answer questions clearly and concisely.\n\n"
        f"User: {user_message}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["response"]


async def text_to_speech(text, voice="default"):

    voice_map = {
        "default": "en-US-AriaNeural",
        "female": "en-US-AriaNeural",
        "male": "en-US-GuyNeural"
    }

    selected_voice = voice_map.get(
        voice,
        "en-US-AriaNeural"
    )

    communicate = edge_tts.Communicate(
        text=text,
        voice=selected_voice
    )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as temp_audio:

        output_path = temp_audio.name

    await communicate.save(output_path)

    with open(output_path, "rb") as f:
        audio = f.read()

    os.remove(output_path)

    return audio