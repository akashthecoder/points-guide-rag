"""Tests for the local Vertex AI tool-lab runner configuration."""

import pytest

from points_guide_rag.agents.run_tool_lab import validate_vertex_environment


def test_validate_vertex_environment_rejects_missing_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GOOGLE_GENAI_USE_VERTEXAI", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_LOCATION", raising=False)

    with pytest.raises(RuntimeError, match="Missing Vertex AI environment variables"):
        validate_vertex_environment()


def test_validate_vertex_environment_accepts_explicit_vertex_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "rag-project-511419")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    validate_vertex_environment()
