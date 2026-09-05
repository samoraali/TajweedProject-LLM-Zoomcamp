from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

from .prompt import SYSTEM_PROMPT


load_dotenv()


DEFAULT_MODEL = "gpt-5.6-luna"


def get_client() -> OpenAI:
    """Create an OpenAI client using the environment API key."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. "
            "Add it to your .env file."
        )

    return OpenAI(api_key=api_key)


def generate_answer(
    query: str,
    user_prompt: str,
    model: str | None = None,
) -> str:
    """Generate a grounded Arabic answer from retrieved context."""

    client = get_client()

    model_name = model or os.getenv(
        "OPENAI_MODEL",
        DEFAULT_MODEL,
    )

    response = client.responses.create(
        model=model_name,
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )

    return response.output_text