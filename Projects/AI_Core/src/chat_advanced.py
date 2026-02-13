"""
Professional LLM Chat with instruction-following model
Uses Mistral-7B or similar model optimized for following instructions
"""

import sys
import traceback

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    import transformers as _transformers

    TF_VER = _transformers.__version__
except Exception:
    TF_VER = "(transformers not available)"
try:
    import accelerate as _accelerate

    ACC_VER = _accelerate.__version__
except Exception:
    ACC_VER = "(accelerate not available)"


def main():
    print("=" * 70)
    print("🤖 LOADING ADVANCED INSTRUCTION-FOLLOWING MODEL...")
    print("=" * 70)

    # Use a better model for Russian and instructions
    # Options (uncomment one):

    # Option 1: Mistral 7B Instruct (best quality, needs 14GB VRAM)
    # model_name = "mistralai/Mistral-7B-Instruct-v0.2"

    # Option 2: Phi-3 Mini (good balance, 3.8B params, ~8GB VRAM)
    model_name = "microsoft/Phi-3-mini-4k-instruct"

    # Option 3: Gemma 2B (smaller, 4GB VRAM)
    # model_name = "google/gemma-2b-it"

    print(f"\nModel: {model_name}")
    print("Loading tokenizer...")
    print(f"transformers version: {TF_VER}; accelerate version: {ACC_VER}")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading model on GPU...")
    print("This may take 1-2 minutes for first download...")

    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.float16, device_map="cuda", trust_remote_code=True
    )

    model.eval()

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_allocated = torch.cuda.memory_allocated(0) / 1024**3
        print(f"\n✅ GPU: {gpu_name}")
        print(f"✅ VRAM used: {vram_allocated:.1f} GB")

    print("\n" + "=" * 70)
    print("✅ MODEL READY FOR INSTRUCTIONS!")
    print("=" * 70)
    print("\n📝 HOW TO USE:")
    print("   Ask questions or give tasks in Russian or English")
    print("   Examples:")
    print("   - Explain what is machine learning")
    print("   - Write Python code to sort a list")
    print("   - Summarize this text: [your text]")
    print("   - Calculate 15 * 23 + 47")
    print("\nCommands: /exit (quit), /clear (clear history), /help")
    print("=" * 70)

    # Instruction / system prompt: задаёт поведение ассистента
    instruction_prefix = (
        "You are a helpful, precise and instruction-following assistant. "
        "Answer in the same language as the user. If asked to perform actions, provide step-by-step instructions and any code examples. "
        "Be concise but complete. If the request is ambiguous, ask a clarifying question."
    )

    conversation_history = []

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["/exit", "/quit"]:
                print("\n👋 Goodbye!")
                break

            if user_input.lower() == "/clear":
                conversation_history = []
                print("🗑️  History cleared")
                continue

            if user_input.lower() == "/help":
                print("\n📖 HELP:")
                print("  This model follows instructions and answers questions")
                print("  You can ask it to:")
                print("  - Explain concepts")
                print("  - Write code")
                print("  - Solve problems")
                print("  - Analyze text")
                print("  - Do calculations")
                continue

            # Build conversation with proper instruction format
            # Префикс-инструкция идёт всегда впереди — задаёт роль ассистента
            if conversation_history:
                # Include last 3 exchanges for context
                context = "\n".join(conversation_history[-6:])
                full_prompt = f"{instruction_prefix}\n\n{context}\n\nUser: {user_input}\nAssistant:"
            else:
                full_prompt = f"{instruction_prefix}\n\nUser: {user_input}\nAssistant:"

            # Tokenize
            inputs = tokenizer(full_prompt, return_tensors="pt", max_length=1024, truncation=True).to("cuda")

            print("\n🤖 Assistant: ", end="", flush=True)

            # Generate response with robust error handling for provider/library issues
            try:
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=300,
                        min_new_tokens=20,
                        temperature=0.8,
                        top_p=0.95,
                        do_sample=True,
                        pad_token_id=tokenizer.pad_token_id,
                        repetition_penalty=1.15,
                        no_repeat_ngram_size=3,
                        use_cache=False,  # avoid provider DynamicCache issues
                    )
            except Exception as e:
                # Log full traceback for diagnostics
                tb = traceback.format_exc()
                print(
                    f"\n❌ Generation failed: {e}\nTraceback:\n{tb}\nAttempting safe fallback generation...", flush=True
                )
                # If it's a known DynamicCache/seen_tokens issue or any other, retry with safe params
                try:
                    with torch.no_grad():
                        outputs = model.generate(
                            **inputs,
                            max_new_tokens=200,
                            temperature=0.0,
                            do_sample=False,
                            pad_token_id=tokenizer.pad_token_id,
                            repetition_penalty=1.0,
                            use_cache=False,
                        )
                    print("\n✅ Fallback generation succeeded.", flush=True)
                except Exception as e2:
                    tb2 = traceback.format_exc()
                    print(f"\n❌ Fallback generation failed: {e2}\nTraceback:\n{tb2}")
                    # Give user hint and continue loop
                    print(
                        "Попробуйте перезапустить скрипт или использовать более простую модель (меньше параметров).\n"
                    )
                    continue

            # Decode response
            full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract only the new answer
            if "Assistant:" in full_response:
                response = full_response.split("Assistant:")[-1].strip()
            else:
                response = full_response[len(full_prompt) :].strip()

            # Clean up response - take first complete sentence/paragraph
            if "\n\n" in response:
                response = response.split("\n\n")[0]
            elif "\nUser:" in response:
                response = response.split("\nUser:")[0]

            response = response.strip()

            if response:
                print(response)

                # Save to history
                conversation_history.append(f"User: {user_input}")
                conversation_history.append(f"Assistant: {response}")
            else:
                print("I apologize, I couldn't generate a proper response. Please try rephrasing.")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except torch.cuda.OutOfMemoryError:
            print("\n❌ GPU out of memory! Try:")
            print("   - Restart the script")
            print("   - Use a smaller model")
            print("   - Close other GPU applications")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Try again or type /help")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        sys.exit(1)
