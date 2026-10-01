"""Typed contracts for the public HTTP API."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints


class QuestionRequest(BaseModel):
    """A question submitted to the points-guide assistant."""

    model_config = ConfigDict(extra="forbid")

    question: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=1000),
    ]


class AnswerResponse(BaseModel):
    """The temporary response shape for the answers endpoint."""

    answer: str
    status: Literal["placeholder"]
