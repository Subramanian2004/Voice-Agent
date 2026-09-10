"""
Local speech-to-text using faster-whisper.

Hands-free: listening starts automatically and stops on its own once you've
gone quiet for SILENCE_DURATION seconds. Runs entirely on your laptop, no
API key or internet needed.
"""

import time

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

from config import (
    MAX_WAIT_FOR_SPEECH,
    SILENCE_DURATION,
    SILENCE_THRESHOLD,
    WHISPER_MODEL_SIZE,
)

CHUNK_SECONDS = 0.2  # how often volume is checked while listening


class SpeechToText:
    def __init__(self, model_size: str = WHISPER_MODEL_SIZE, device: str = "cpu", compute_type: str = "int8"):
        print(f"Loading Whisper model '{model_size}'...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.sample_rate = 16000
        self.chunk_frames = int(self.sample_rate * CHUNK_SECONDS)

    def _record_until_silence(self) -> np.ndarray:
        print("\nListening... (go ahead, it'll stop after you pause)")

        chunks = []
        speech_started = False
        last_loud_time = time.time()
        start_time = time.time()

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32") as stream:
            while True:
                data, _ = stream.read(self.chunk_frames)
                chunks.append(data.copy())

                volume = float(np.sqrt(np.mean(data.astype(np.float64) ** 2)))
                now = time.time()

                if volume > SILENCE_THRESHOLD:
                    last_loud_time = now
                    if not speech_started:
                        speech_started = True

                if speech_started and (now - last_loud_time) >= SILENCE_DURATION:
                    break

                if not speech_started and (now - start_time) >= MAX_WAIT_FOR_SPEECH:
                    break

        print("Got it, transcribing...")
        if not chunks:
            return np.array([], dtype=np.float32)
        return np.concatenate(chunks, axis=0).flatten()

    def transcribe(self, audio: np.ndarray) -> str:
        if audio.size == 0:
            return ""
        segments, _ = self.model.transcribe(audio, language="en")
        return " ".join(segment.text.strip() for segment in segments).strip()

    def listen(self) -> str:
        """Block until you've spoken and gone quiet, then return the transcript."""
        audio = self._record_until_silence()
        return self.transcribe(audio)