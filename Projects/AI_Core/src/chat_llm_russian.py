"""
Интерактивный чат с мультиязычной LLM моделью на RTX GPU
Поддержка русского языка через BLOOMZ
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import sys

def main():
    print("=" * 60)
    print("🤖 ЗАГРУЗКА МОДЕЛИ С ПОДДЕРЖКОЙ РУССКОГО...")
    print("=" * 60)
    
    # Используем BLOOMZ - хорошая поддержка русского языка
    model_name = "bigscience/bloomz-560m"
    
    print(f"\nМодель: {model_name}")
    print("Эта модель специально обучена на русском языке!")
    print("\nЗагрузка токенизатора...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    print("Загрузка модели на GPU...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="cuda"
    )
    
    model.eval()
    
    # Информация о GPU
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"\n✅ GPU: {gpu_name}")
    
    print("\n" + "=" * 60)
    print("✅ МОДЕЛЬ ГОТОВА!")
    print("=" * 60)
    print("\n💡 СОВЕТ: Задавайте конкретные вопросы.")
    print("   Примеры:")
    print("   - Что такое Python?")
    print("   - Объясни что такое GPU")
    print("   - Расскажи про искусственный интеллект")
    print("\nКоманды: /exit (выход), /clear (очистить)")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n👤 Вы: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/exit', '/quit', '/выход']:
                print("\n👋 До свидания!")
                break
            
            if user_input.lower() in ['/clear', '/очистить']:
                print("🗑️  История очищена")
                continue
            
            # Простой промпт для лучших ответов
            prompt = f"{user_input}\n\nОтвет:"
            
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                max_length=256,
                truncation=True
            ).to("cuda")
            
            print("\n🤖 Модель: ", end="", flush=True)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=100,
                    temperature=0.8,
                    top_p=0.95,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.3
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Убираем промпт из ответа
            if "Ответ:" in response:
                answer = response.split("Ответ:")[-1].strip()
            else:
                answer = response[len(prompt):].strip()
            
            # Берем первое предложение для краткости
            if ". " in answer:
                answer = answer.split(". ")[0] + "."
            
            print(answer if answer else "Извините, не могу ответить на этот вопрос.")
            
        except KeyboardInterrupt:
            print("\n\n👋 Выход...")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
