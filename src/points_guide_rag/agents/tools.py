"""Deterministic local tools available to ADK agents."""


def count_words(text: str) -> dict[str, int]:
    """Count the whitespace-delimited words in supplied text.

    Use this tool only when a user explicitly asks for a word count.

    Args:
        text: The text whose words should be counted.

    Returns:
        A dictionary containing the number of words.
    """
    return {"word_count": len(text.split())}
