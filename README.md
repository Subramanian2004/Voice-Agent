# Butcher — Personal Voice Agent

A voice assistant that runs entirely on your laptop: you talk to it, it thinks locally, it talks back, and it's starting to be able to actually *do things* on your machine — open apps, read files, click, and type, all with your explicit confirmation before anything real happens.

No cloud APIs, no API keys, no cost. Whisper for hearing, a local LLM (via Ollama) for thinking, Piper for speaking.

## Status: early / actively being built

This is a personal project, built incrementally. It works, but it's early — treat it as a foundation you're extending, not a finished product.

### What's working now
- **Voice in** — push-to-talk recording, transcribed locally with `faster-whisper` (no audio ever leaves the laptop)
- **Reasoning** — a local LLM (`llama3.2` via Ollama) with conversation memory, deciding when to call tools
- **Voice out** — replies synthesized and spoken locally with Piper TTS
- **Laptop tools**, each one a narrow, single-purpose function the agent can call:
  - `list_directory` — list files/folders at a path
  - `read_text_file` — read a small text file
  - `open_application` — launch a desktop app by name
  - `get_screen_resolution` — check screen size before clicking
  - `click_at(x, y)` — click a screen coordinate
  - `type_text(text)` — type text at the current cursor
  - `press_key(key)` — press a single key
- **Safety gate on real actions** — `click_at`, `type_text`, and `press_key` all print exactly what they're about to do and require you to type `yes` in the terminal first. Nothing clicks or types without explicit approval.
- **Desktop launcher** — `start_agent.bat` so you don't need to open a code editor to run it

### Known limitations right now
- Clicking requires exact pixel coordinates you supply — the agent can't yet "see" the screen and find a button on its own (no vision model in the loop yet)
- Small local models can occasionally invent a tool call for something it doesn't actually have a tool for; the system prompt explicitly tells it not to, but it's not foolproof — always watch what it's about to do
- Whisper's smallest model can mishear things in a noisy room — worth upgrading to a larger Whisper model if accuracy matters more than speed for you

## Roadmap / what's next

- [ ] **Screen-aware clicking** — feed a screenshot to a vision-capable model so it can find and click things by description ("click the blue Subscribe button") instead of needing raw coordinates
- [ ] **Wake word / hands-free mode** — replace the press-ENTER trigger with always-listening wake-word detection
- [ ] **More laptop tools** — file writing/editing, running scripts, browser tab control, calendar/email integration — added deliberately, one at a time
- [ ] **Action logging** — a local log of every real action taken (clicks, typed text, opened apps) for accountability and easy review
- [ ] **Lower-latency option** — swap in a hosted STT/TTS pair (e.g. AssemblyAI + Cartesia) for near-instant responses when internet + a little cost is acceptable, while keeping the fully-local mode as default

## Architecture

Your voice
│
▼
faster-whisper (local STT)
│ transcript
▼
LangChain agent + Ollama LLM (local reasoning + tool calls)
│ reply text │ tool calls (confirmed before running)
▼ ▼
Piper (local TTS) laptop actions (open app, click, type...)
│
▼
Spoken reply


## Tech stack

| Piece | Tool | Why |
|---|---|---|
| Speech-to-text | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Local, free, fast enough on CPU |
| LLM / reasoning | [Ollama](https://ollama.com) running `llama3.2` | Local, free, supports tool-calling |
| Agent framework | [LangChain](https://python.langchain.com) + LangGraph | Tool orchestration + conversation memory |
| Text-to-speech | [Piper](https://github.com/OHF-Voice/piper1-gpl) | Local, free, low-latency |
| Laptop control | Python stdlib + [pyautogui](https://pyautogui.readthedocs.io) | Open apps, click, type |

## Setup

1. **Install [Ollama](https://ollama.com)**, then pull a tool-calling model:

ollama pull llama3.2

2. **Clone this repo and set up Python:**

git clone https://github.com/Subramanian2004/butcher-voice-agent.git
cd butcher-voice-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

3. **Download a Piper voice:**

python -m piper.download_voices en_US-lessac-medium

   Move the resulting `.onnx` and `.onnx.json` files into the `voices/` folder.

## Running it

Either:

cd src
python main.py

or double-click `start_agent.bat` in the project root.

Press ENTER, speak, press ENTER again to stop. Say "exit" to quit.

## Project structure

butcher-voice-agent/
├── requirements.txt
├── .env.example
├── start_agent.bat # double-click launcher
├── voices/ # Piper voice model goes here (gitignored)
└── src/
├── config.py # env-driven settings
├── stt.py # local Whisper speech-to-text
├── tts.py # local Piper text-to-speech
├── tools.py # everything Butcher can actually DO
├── agent.py # LangChain agent, system prompt, memory
└── main.py # ties it all together in a loop


## Safety & privacy notes

- Everything runs locally — no audio, transcripts, or screen data are sent anywhere
- Any action that touches your mouse/keyboard requires explicit terminal confirmation before it runs
- New tools should stay narrow and single-purpose — avoid ever adding a catch-all "run any command" tool
- `.env` and the `venv/` folder are gitignored; nothing sensitive is meant to be committed

## License

Personal project — no license specified yet.
