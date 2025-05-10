from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import os

load_dotenv()

API_KEY = os.getenv("DEEPGRAM_KEY")

def speech_to_text(audio_file):
    try:
        deepgram = DeepgramClient(API_KEY)
        with open(audio_file, "rb") as file:
            buffer_data = file.read()
        payload = {"buffer": buffer_data}

        options = PrerecordedOptions(model="nova-2", smart_format=True)

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
        return transcript

    except Exception as e:
        print(f"Exception: {e}")
        return None
