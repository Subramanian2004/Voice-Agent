"""
Local speech-to-text using faster-whisper.

Push-to-talk style: press ENTER to start recording, press ENTER again to stop.
Runs entirely on your laptop, no API key or internet needed.
"""

import queue
import threading

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

from config import WHISPER_MODEL_SIZE


class SpeechToText:
    def __init__(self, model_size: str = WHISPER_MODEL_SIZE, device: str = "cpu", compute_type: str = "int8"):
        print(f"Loading Whisper model '{model_size}'...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.sample_rate = 16000

    def _record_until_enter(self) -> np.ndarray:
        print("\nPress ENTER to start speaking...")
        input()
        print("Recording... press ENTER again to stop.")

        audio_queue: queue.Queue = queue.Queue()
        chunks = []
        stop_flag = threading.Event()

        def audio_callback(indata, frames, time_info, status):
            audio_queue.put(indata.copy())

        def wait_for_enter():
            input()
            stop_flag.set()

        listener = threading.Thread(target=wait_for_enter, daemon=True)

        with sd.InputStream(
            samplerate=self.sample_rate, channels=1, dtype="float32", callback=audio_callback
        ):
            listener.start()
            while not stop_flag.is_set():
                try:
                    chunks.append(audio_queue.get(timeout=0.1))
                except queue.Empty:
                    continue

        print("Stopped recording. Transcribing...")
        if not chunks:
            return np.array([], dtype=np.float32)
        return np.concatenate(chunks, axis=0).flatten()

    def transcribe(self, audio: np.ndarray) -> str:
        if audio.size == 0:
            return ""
        segments, _ = self.model.transcribe(audio, language="en")
        return " ".join(segment.text.strip() for segment in segments).strip()

    def listen(self) -> str:
        """Block until the user records something, then return the transcript."""
        audio = self._record_until_enter()
        return self.transcribe(audio)
