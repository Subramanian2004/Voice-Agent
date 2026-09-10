# Personal Voice Agent (local-first starter)

A push-to-talk voice assistant that runs entirely on your laptop:
**faster-whisper** (speech-to-text) → **Ollama** (LLM agent) → **Piper** (text-to-speech).

No API keys, no cost, works offline. Talk to it, it replies out loud, and it can
already peek at your filesystem / open apps as a first taste of "doing tasks" —
you'll add more tools over time in `src/tools.py`.

## 1. Install Ollama (the agent's brain)

- Download from https://ollama.com and install it
- Pull a tool-calling-capable model:
  ```
  ollama pull llama3.2
  ```

## 2. Python setup

```
cd voice-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

`piper-tts` is installed as part of `requirements.txt` — no separate binary download needed.

## 3. Download a Piper voice

```
python -m piper.download_voices en_US-lessac-medium
```

This downloads `en_US-lessac-medium.onnx` and `.onnx.json` into your current folder.
Move both files into the `voices/` folder (or update `PIPER_VOICE_PATH` in `.env`
to wherever they landed).

## 4. Run it

```
cd src
python main.py
```

Press ENTER, speak, press ENTER again to stop recording. The agent transcribes,
thinks (and can call tools), replies out loud, and loops. Say "exit" to quit.

## Project layout

```
voice-agent/
├── requirements.txt
├── .env.example
├── voices/              # put your Piper voice model(s) here
└── src/
    ├── config.py        # env-driven settings
    ├── stt.py            # local Whisper speech-to-text
    ├── tts.py            # local Piper text-to-speech
    ├── tools.py           # what the agent can actually DO on your laptop
    ├── agent.py           # LangChain agent + memory
    └── main.py            # ties it all together in a loop
```

## Where to go next

- **More tools**: add functions to `src/tools.py` (send an email, create a
  calendar event, run a script, control Spotify...) and register them in
  `ALL_TOOLS`. Keep each tool narrow and named for exactly one action —
  avoid a catch-all "run any shell command" tool.
- **Wake word / hands-free**: swap the ENTER-press trigger in `stt.py` for a
  wake-word library (e.g. `openWakeWord`) or simple voice-activity detection.
- **Lower latency / better voices**: swap AssemblyAI (streaming STT) and
  Cartesia (streaming TTS) in for the local pieces once you want to move off
  free/local — see the LangChain voice-agent docs this was based on:
  https://docs.langchain.com/oss/python/langchain/voice-agent
- **Safety**: any tool you add is something the agent can decide to call on
  its own from a spoken instruction — review new tools before wiring them in,
  especially ones that delete, send, or spend anything.
