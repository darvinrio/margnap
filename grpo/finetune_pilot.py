"""
grpo/finetune_pilot.py

Attempt at local fine-tuning
"""

import json
from typing import TYPE_CHECKING, cast

from datasets import load_dataset
from mlx_tune import FastLanguageModel, GRPOConfig, GRPOTrainer

if TYPE_CHECKING:
    import mlx.nn as nn
    from datasets.iterable_dataset import Dataset
    from mlx_lm.tokenizer_utils import TokenizerWrapper

from detectors import find_triads

SEED = 42

# DATASET
dataset = load_dataset(
    "argilla/ultrafeedback-binarized-preferences-cleaned-kto", split="train"
)
dataset = cast("Dataset", dataset)


def format_dataset(example: dict) -> dict:
    """format"""
    return {"prompt": [{"role": "user", "content": example["prompt"]}]}


training_dataset = dataset  # .map(format_dataset)

# MODEL
max_seq_length = 2048
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3.5-0.8B",
    max_seq_length=max_seq_length,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing=True,
    random_state=SEED,
)
model = cast("nn.Module", model)
tokenizer = cast("TokenizerWrapper", tokenizer)


def triad_reward_func(prompts: list[str], completions: list[list[dict]]) -> list[float]:
    """
    Reward function that penalizes responses that contain triads of bad patterns.

    Args:
        prompts: List of input prompts.
        completions: List of model completions.
        **kwargs: Additional keyword arguments.
        violation_penalty: Penalty factor for each triad violation. Defaults to 0.3.

    Returns:
        List of reward scores for each prompt-completion pair.
    """
    VIOLATION_PENALTY: float = 0.3
    INVALID_SCORE_FLOOR: float = -1.0
    VALID_SCORE: float = 1.0

    rewards = []
    for prompt, completion in zip(prompts, completions):
        text = completion[0]["content"]

        # Count how many times the bad pattern appears
        pattern_count, _ = find_triads(text)

        if pattern_count == 0:
            # reward
            score = VALID_SCORE
        else:
            # fractional penalty with floor
            score = max(
                INVALID_SCORE_FLOOR, VALID_SCORE - (pattern_count * VIOLATION_PENALTY)
            )

        rewards.append(score)

    return rewards


training_args = GRPOConfig(
    learning_rate=5e-6,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    # max_prompt_length=512,
    max_completion_length=2048,
    num_generations=4,  # Compares 4 generations per prompt
    logging_steps=1,  # Live metrics updates every step
    # optim="adamw_8bit",  # VRAM saver for T4 GPU
    output_dir="outputs/grpo",
)

small_train_dataset = training_dataset.select(range(100))

print(json.dumps(training_dataset[0], indent=2))
print(type(training_dataset))
print(type(training_dataset[0]))

trainer = GRPOTrainer(
    model=model,
    tokenizer=tokenizer,
    reward_funcs=[triad_reward_func],
    args=training_args,
    train_dataset=small_train_dataset,
)

trainer.train()
