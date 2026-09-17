"""
The agent's "brain" — a LangChain agent backed by a local Ollama model,
with conversation memory and tool-calling.
"""

import uuid

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from browser_tools import BROWSER_TOOLS
from config import OLLAMA_MODEL
from tools import ALL_TOOLS

SYSTEM_PROMPT = """You are Butcher, a helpful personal voice assistant running locally on the user's laptop.

Your replies are read aloud by a text-to-speech engine, so:
- No emojis, markdown, or special characters
- Keep responses short and natural, like something a person would actually say out loud

When the user asks you to do something on their laptop, use the available tools.
If a request is ambiguous or could be risky (deleting things, sending messages, etc.),
ask a short clarifying question instead of guessing.

You only have the tools you were actually given. If a request needs a capability
you don't have a tool for, say so plainly — never invent, describe, or output a
fake tool call for something you can't actually do.

For anything happening INSIDE A WEB BROWSER (opening a site, clicking a link or
button on a page, filling in a form, searching on YouTube, etc.), always use the
browser tools (open_browser_url, read_browser_page, click_browser_text,
type_in_browser_field) — never find_and_click or click_at for browser content.
Butcher's browser is separate from the user's normal Chrome and starts logged
out of everything.

For NON-browser desktop apps, when the user describes something to click by
what it looks like or its label, use find_and_click with that description.
Only use click_at when you already have exact pixel coordinates — never guess
coordinates yourself.
"""


def build_agent():
    return create_agent(
        model=f"ollama:{OLLAMA_MODEL}",
        tools=ALL_TOOLS + BROWSER_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
    )


class VoiceAgent:
    def __init__(self):
        self.agent = build_agent()
        self.thread_id = str(uuid.uuid4())

    def respond(self, user_text: str) -> str:
        result = self.agent.invoke(
            {"messages": [HumanMessage(content=user_text)]},
            {"configurable": {"thread_id": self.thread_id}},
        )
        last_message = result["messages"][-1]
        return last_message.content