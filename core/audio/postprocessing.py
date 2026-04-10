def postprocess_text(text: str) -> str:
    """Strip whitespace and collapse multiple spaces."""
    import re
    text = text.strip()
    text = re.sub(r" {2,}", " ", text)
    return text

