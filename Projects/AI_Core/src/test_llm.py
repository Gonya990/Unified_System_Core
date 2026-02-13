"""
Test LLM inference on RTX 3080
Simple example using Hugging Face Transformers
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print("=" * 70)
print("  LLM Inference Test on RTX 3080")
print("=" * 70)

# Check GPU
if torch.cuda.is_available():
    print(f"\nGPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("\nWARNING: GPU not available, using CPU")

# Small model that fits in 10GB VRAM
model_name = "microsoft/phi-2"  # 2.7B parameters
print(f"\nLoading model: {model_name}")
print("(This may take a few minutes on first run...)")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # FP16 for memory efficiency
    device_map="cuda",  # Use GPU
    trust_remote_code=True,
)

print("Model loaded successfully!")

# Test prompts
prompts = [
    "What is artificial intelligence?",
    "Explain machine learning in simple terms:",
    "Write a Python function to calculate fibonacci:",
]

print("\n" + "=" * 70)
print("  Running inference...")
print("=" * 70)

for i, prompt in enumerate(prompts, 1):
    print(f"\n[{i}] Prompt: {prompt}")
    print("-" * 70)

    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    # Generate
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=150, temperature=0.7, do_sample=True, top_p=0.9)

    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Response:\n{response}")

print("\n" + "=" * 70)
print("  Test completed successfully!")
print("=" * 70)
print("\nYour RTX 3080 is ready for LLM inference!")
