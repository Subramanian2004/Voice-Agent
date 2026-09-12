"""Central place for environment-driven config."""

import os

# Project root = the folder above src/, regardless of where the script is run from
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_VOICE_PATH = os.path.join(_PROJECT_ROOT, "voices", "en_US-lessac-medium.onnx")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
VISION_MODEL = os.getenv("VISION_MODEL", "moondream")
PIPER_VOICE_PATH = os.getenv("PIPER_VOICE_PATH", _DEFAULT_VOICE_PATH)
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base.en")

# Voice-activity detection tuning for automatic (hands-free) listening.
SILENCE_THRESHOLD = float(os.getenv("SILENCE_THRESHOLD", "0.01"))
SILENCE_DURATION = float(os.getenv("SILENCE_DURATION", "6.0"))
MAX_WAIT_FOR_SPEECH = float(os.getenv("MAX_WAIT_FOR_SPEECH", "15.0"))