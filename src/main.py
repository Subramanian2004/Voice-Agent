"""
Butcher — personal voice agent, entry point.

Loop: listen -> transcribe -> agent thinks/acts -> speak reply.
Everything runs locally: Whisper for STT, Ollama for the LLM, Piper for TTS.
"""

from dotenv import load_dotenv

load_dotenv()

from agent import VoiceAgent
from stt import SpeechToText
from tts import TextToSpeech

EXIT_WORDS = {"exit", "quit", "stop"}


def main():
    print("Loading Butcher... (first run may take a minute)")
    stt = SpeechToText()
    tts = TextToSpeech()
    agent = VoiceAgent()

    print("\nButcher is ready and listening. Say 'exit' or 'quit' to stop.\n")

    while True:
        user_text = stt.listen()

        if not user_text:
            print("(didn't catch that, try again)")
            continue

        print(f"You said: {user_text}")

        if user_text.strip().lower() in EXIT_WORDS:
            print("Goodbye!")
            break

        reply = agent.respond(user_text)
        print(f"Butcher: {reply}")
        tts.speak(reply)


if __name__ == "__main__":
    main()