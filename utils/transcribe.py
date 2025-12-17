from openai import OpenAI
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
import sys

load_dotenv()
client = OpenAI()


def transcribe_audio_openai(
    audio_path: str,
    language: str = "en",
) -> List[Dict]:
    """
    Transcribe audio using OpenAI Whisper API.
    """

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,
            response_format="srt",
            temperature=0.0,
        )

    return transcript


if __name__ == "__main__":
    audio_file = sys.argv[1] 
    segments = transcribe_audio_openai(audio_file)

    print(segments)