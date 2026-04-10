from instructions.qwen_polish import PROMPT
from core.audio.llm_model import ask_qwen

def postprocess_text(text: str) -> str:
    """Strip whitespace and collapse multiple spaces."""
    import re
    text = text.strip()
    text = re.sub(r" {2,}", " ", text)
    
    text = PROMPT.format(text=text)
    
    text = ask_qwen(text)
    
    return text

