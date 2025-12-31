"""
Интерактивный чат с LLM моделью на RTX GPU
Используйте этот скрипт для общения с моделью в консоли
"""

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch
import sys

def main():
    print("=" * 60)
    print("🤖 ЗАГРУЗКА МОДЕЛИ...")
    print("=" * 60)
    
    # Выбор модели (можно легко заменить на другую)
    model_name = "microsoft/phi-2"
    # Альтернативы для русского языка:
    # model_name = "facebook/opt-1.3b"
    # model_name = "bigscience/bloomz-560m"
    
    print(f"\nМодель: {model_name}")
    print("Загрузка токенизатора...")
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, 
        trust_remote_code=True
    )
    
    # Устанавливаем pad_token если его нет
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print("Загрузка модели на GPU...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,  # FP16 для экономии памяти
        device_map="cuda",           # Автоматически на GPU
        trust_remote_code=True
    )
    
    model.eval()  # Режим inference
    
    # Информация о GPU
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"\n✅ GPU: {gpu_name}")
        print(f"✅ Память GPU: {gpu_memory:.1f} GB")
    
    print("\n" + "=" * 60)
    print("✅ МОДЕЛЬ ГОТОВА К РАБОТЕ!")
    print("=" * 60)
    print("\nКоманды:")
    print("  - Просто пишите текст для общения")
    print("  - /exit или /quit - выход")
    print("  - /clear - очистить историю")
    print("  - /help - справка")
    print("=" * 60)
    
    # История диалога (опционально)
    conversation_history = []
    
    while True:
        try:
            # Получаем ввод пользователя
            user_input = input("\n👤 Вы: ").strip()
            
            if not user_input:
                continue
            
            # Обработка команд
            if user_input.lower() in ['/exit', '/quit', '/выход']:
                print("\n👋 До свидания!")
                break
            
            if user_input.lower() in ['/clear', '/очистить']:
                conversation_history = []
                print("🗑️  История очищена")
                continue
            
            if user_input.lower() in ['/help', '/помощь']:
                print("\n📖 СПРАВКА:")
                print("  - Пишите вопросы на русском или английском")
                print("  - Модель генерирует ответы используя RTX 3080")
                print("  - /exit - выход из программы")
                print("  - /clear - очистить историю диалога")
                continue
            
            # Формируем промпт с учетом истории
            if conversation_history:
                # Берем последние 3 обмена для контекста
                recent_history = conversation_history[-6:]
                context = "\n".join(recent_history)
                prompt = f"{context}\nВопрос: {user_input}\nОтвет:"
            else:
                prompt = f"Вопрос: {user_input}\nОтвет:"
            
            # Токенизация
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to("cuda")
            
            print("\n🤖 Модель: ", end="", flush=True)
            
            # Генерация ответа
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=150,          # Максимум новых токенов
                    temperature=0.7,              # Креативность (0.1-1.0)
                    top_p=0.9,                    # Nucleus sampling
                    top_k=50,                     # Top-K sampling
                    do_sample=True,               # Включить sampling
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.2        # Штраф за повторы
                )
            
            # Декодируем ответ
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Извлекаем только новый ответ (убираем промпт)
            if "Ответ:" in generated_text:
                response = generated_text.split("Ответ:")[-1].strip()
            else:
                response = generated_text[len(prompt):].strip()
            
            # Очистка ответа от лишних символов
            response = response.split("\n")[0] if "\n" in response else response
            response = response.strip()
            
            print(response)
            
            # Сохраняем в историю
            conversation_history.append(f"Вопрос: {user_input}")
            conversation_history.append(f"Ответ: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Прервано пользователем. До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            print("Попробуйте еще раз или введите /help для справки")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
