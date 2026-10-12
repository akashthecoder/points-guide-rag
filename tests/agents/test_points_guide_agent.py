"""Tests for the first ADK tool-use learning slice."""

from points_guide_rag.agents.points_guide_agent import TOOL_LAB_MODEL, root_agent
from points_guide_rag.agents.tools import count_words


def test_count_words_counts_whitespace_delimited_words() -> None:
    assert count_words("The quick  brown fox\n jumps") == {"word_count": 5}


def test_root_agent_registers_the_count_words_tool() -> None:
    tool_names = {tool.__name__ for tool in root_agent.tools}

    assert root_agent.name == "points_guide_tool_lab"
    assert root_agent.model == TOOL_LAB_MODEL
    assert tool_names == {"count_words"}
