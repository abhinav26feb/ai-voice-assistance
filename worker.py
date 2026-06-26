import requests


def speech_to_text(audio_binary):
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + "/speech-to-text/api/v1/recognize"

    params = {
        "model": "en-US_Multimedia"
    }

    response = requests.post(
        api_url,
        params=params,
        data=audio_binary
    ).json()

    print("speech to text response:", response)

    text = "null"

    while bool(response.get("results")):
        text = (
            response.get("results")
            .pop()
            .get("alternatives")
            .pop()
            .get("transcript")
        )

    return text


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

    result = response.json()

    return result["response"]


def text_to_speech(text, voice=""):
    return b""
    # base_url = "https://sn-watson-tts.labs.skills.network"
    #
    # api_url = (
    #     base_url +
    #     "/text-to-speech/api/v1/synthesize?output=output_text.wav"
    # )
    #
    # if voice != "" and voice != "default":
    #     api_url += "&voice=" + voice
    #
    # headers = {
    #     "Accept": "audio/wav",
    #     "Content-Type": "application/json"
    # }
    #
    # json_data = {
    #     "text": text
    # }
    #
    # response = requests.post(
    #     api_url,
    #     headers=headers,
    #     json=json_data
    # )
    #
    # return response.content