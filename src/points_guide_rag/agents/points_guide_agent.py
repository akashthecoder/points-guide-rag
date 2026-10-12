"""The first, deliberately minimal Google ADK agent definition."""

from google.adk.agents import Agent

from .tools import count_words

TOOL_LAB_MODEL = "gemini-3.5-flash-lite"

root_agent = Agent(
    name="points_guide_tool_lab",
    model=TOOL_LAB_MODEL,
    description="A learning agent that demonstrates one deterministic local tool.",
    instruction=(
        "You are a tool-use learning agent. Use count_words when the user explicitly asks "
        "for a word count. Do not provide points or travel advice in this lab."
    ),
    tools=[count_words],
)
