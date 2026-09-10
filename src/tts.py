"""
Local text-to-speech using the official piper-tts Python package
(https://github.com/OHF-Voice/piper1-gpl).

Install with: pip install piper-tts
Download a voice with: python -m piper.download_voices en_US-lessac-medium
"""

import io
import wave

import sounddevice as sd
import soundfile as sf
from piper import PiperVoice

from config import PIPER_VOICE_PATH


class TextToSpeech:
    def __init__(self, voice_model: str = PIPER_VOICE_PATH):
        self.voice = PiperVoice.load(voice_model)

    def speak(self, text: str) -> None:
        text = text.strip()
        if not text:
            return

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)

        buffer.seek(0)
        data, samplerate = sf.read(buffer, dtype="float32")
        sd.play(data, samplerate)
        sd.wait()
