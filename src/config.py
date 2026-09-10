"""Central place for environment-driven config."""

import os

# Project root = the folder above src/, regardless of where the script is run from
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_VOICE_PATH = os.path.join(_PROJECT_ROOT, "voices", "en_US-lessac-medium.onnx")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
PIPER_VOICE_PATH = os.getenv("PIPER_VOICE_PATH", _DEFAULT_VOICE_PATH)
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base.en")