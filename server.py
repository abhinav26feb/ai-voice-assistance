import base64
import json
import os

from flask import Flask, render_template, request
from flask_cors import CORS

from worker import (
    speech_to_text,
    text_to_speech,
    ollama_process_message,
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text_route():
    print("Processing speech-to-text...")

    audio_binary = request.data

    text = speech_to_text(audio_binary)

    response = app.response_class(
        response=json.dumps({"text": text}),
        status=200,
        mimetype="application/json",
    )

    return response


@app.route("/process-message", methods=["POST"])
def process_message_route():

    user_message = request.json["userMessage"]
    print("User Message:", user_message)

    voice = request.json["voice"]
    print("Voice:", voice)

    ollama_response_text = ollama_process_message(user_message)

    ollama_response_text = os.linesep.join(
        [
            line
            for line in ollama_response_text.splitlines()
            if line
        ]
    )

    ollama_response_speech = text_to_speech(
        ollama_response_text,
        voice,
    )

    ollama_response_speech = base64.b64encode(
        ollama_response_speech
    ).decode("utf-8")

    response = app.response_class(
        response=json.dumps(
            {
                "ollamaResponseText": ollama_response_text,
                "ollamaResponseSpeech": ollama_response_speech,
            }
        ),
        status=200,
        mimetype="application/json",
    )

    return response


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )