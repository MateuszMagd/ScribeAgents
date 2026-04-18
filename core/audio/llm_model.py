import os

import torch
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()

MODEL_NAME = "Qwen/Qwen3.5-4B"
HF_TOKEN = os.getenv("HF_TOKEN")

_tokenizer = None
_model = None


def _get_model():
    """Load and cache the Qwen model and tokenizer on first call."""
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            token=HF_TOKEN,
            torch_dtype=torch.float16,
            device_map="auto",
        )
    return _tokenizer, _model


def ask_qwen(prompt: str) -> str:
    tokenizer, model = _get_model()
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.3,
        do_sample=True,
    )

    input_len = inputs["input_ids"].shape[1]
    return tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)


if __name__ == "__main__":
    import sys
    
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    
    from instructions.qwen_polish import PROMPT
    
    text = ask_qwen(PROMPT.format(text="Wlacz muze na jutub. Ta kielba jest zajebista. Jak ci sie nie podoba, to myk cyk cyk juz cie nie ma."))
    
    print(text)