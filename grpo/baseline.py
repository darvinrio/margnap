"""
grpo/baseline.py

mlx-tune inference and baseline evaluation
"""

from typing import TYPE_CHECKING, cast

from datasets import load_dataset
from datasets.iterable_dataset import Dataset
from mlx_lm import generate
from mlx_tune import FastLanguageModel
from tqdm import tqdm

if TYPE_CHECKING:
    import mlx.nn as nn
    from mlx_lm.tokenizer_utils import TokenizerWrapper

from detectors import find_triads

dataset = load_dataset(
    "argilla/ultrafeedback-binarized-preferences-cleaned-kto", split="train"
)
dataset = cast("Dataset", dataset)

max_seq_length = 2048
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3.5-0.8B",
    max_seq_length=max_seq_length,
    load_in_4bit=True,
)
model = cast("nn.Module", model)
tokenizer = cast("TokenizerWrapper", tokenizer)

FastLanguageModel.for_inference(model)

# baseline eval
SEED = 42 + 43
NUM_PROMPTS = 100
eval_dataset: Dataset = dataset.shuffle(seed=SEED).select(range(NUM_PROMPTS))

total_triads = 0
generations_with_triads = 0

for example in tqdm(eval_dataset):
    # print(json.dumps(example, indent=2))

    prompt_text = example.get("prompt")
    # print(f"prompt_text: \n {prompt_text}")
    messages = [{"role": "user", "content": prompt_text}]
    formatted_prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    generated_text = generate(
        model,
        tokenizer,
        formatted_prompt,
        verbose=False,
        # max_tokens=1024,
    )
    count, _ = find_triads(generated_text)
    # print(f"triad count: {count}")
    total_triads += count
    if count > 0:
        generations_with_triads += 1

    # test one run
    # break
print(f"total_triads: {total_triads}")
print(f"generations_with_triads: {generations_with_triads}")
