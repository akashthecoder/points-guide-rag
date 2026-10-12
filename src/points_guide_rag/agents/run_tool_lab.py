"""Run the first ADK tool-use lab against Vertex AI from a local terminal."""

import asyncio
import os

from google.adk import Runner
from google.adk.events import Event
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .points_guide_agent import root_agent

APP_NAME = "points_guide_tool_lab"
USER_ID = "local_developer"
DEFAULT_PROMPT = "How many words are in: The quick brown fox jumps over the lazy dog?"
REQUIRED_VERTEX_ENVIRONMENT = (
    "GOOGLE_GENAI_USE_VERTEXAI",
    "GOOGLE_CLOUD_PROJECT",
    "GOOGLE_CLOUD_LOCATION",
)


def validate_vertex_environment() -> None:
    """Ensure the process is explicitly configured to use Vertex AI."""
    missing = [name for name in REQUIRED_VERTEX_ENVIRONMENT if not os.environ.get(name)]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(
            f"Missing Vertex AI environment variables: {names}. "
            "Set them in your terminal before running this module."
        )

    if os.environ["GOOGLE_GENAI_USE_VERTEXAI"].lower() != "true":
        raise RuntimeError("GOOGLE_GENAI_USE_VERTEXAI must be set to true.")


async def run_prompt(prompt: str) -> list[Event]:
    """Run one prompt through an in-memory ADK session and return its trace events."""
    validate_vertex_environment()
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)
    user_message = types.Content(role="user", parts=[types.Part(text=prompt)])
    events: list[Event] = []

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=user_message,
    ):
        events.append(event)

    return events


def main() -> None:
    """Run the controlled tool-use prompt and print its ADK event trace."""
    events = asyncio.run(run_prompt(DEFAULT_PROMPT))
    for event in events:
        print(event.model_dump_json(exclude_none=True))


if __name__ == "__main__":
    main()
