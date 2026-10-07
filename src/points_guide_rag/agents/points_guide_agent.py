"""The first, deliberately minimal Google ADK agent definition."""

from google.adk.agents import Agent

from .tools import count_words

root_agent = Agent(
    name="points_guide_tool_lab",
    model="gemini-flash-latest",
    description="A learning agent that demonstrates one deterministic local tool.",
    instruction=(
        "You are a tool-use learning agent. Use count_words when the user explicitly asks "
        "for a word count. Do not provide points or travel advice in this lab."
    ),
    tools=[count_words],
)
