def postprocess_text(text: str) -> str:
    """Clean up raw transcription output.

    Current steps:
    - Strip leading/trailing whitespace.
    - Collapse multiple consecutive spaces into one.

    Args:
        text: Raw text returned by the STT model.

    Returns:
        Cleaned text string.
    """
    import re
    text = text.strip()
    text = re.sub(r" {2,}", " ", text)
    return text
