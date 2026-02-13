"""
Базовый пример использования ONNX Runtime
Демонстрирует загрузку и выполнение ONNX модели
"""

import onnxruntime as ort


def print_section(title):
    """Красивый вывод секций"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main():
    print_section("ONNX Runtime - Базовый пример")

    # 1. Проверка доступных провайдеров
    print_section("Доступные Execution Providers")
    providers = ort.get_available_providers()
    for i, provider in enumerate(providers, 1):
        print(f"  {i}. {provider}")

    # 2. Информация о версии
    print(f"\nONNX Runtime версия: {ort.__version__}")

    # 3. Проверка устройств
    print_section("Информация об устройствах")

    if "CUDAExecutionProvider" in providers:
        print("  ✓ CUDA доступна (NVIDIA GPU)")
        print("  Рекомендуется для максимальной производительности")
    else:
        print("  ⚠ CUDA не доступна, будет использован CPU")

    if "TensorrtExecutionProvider" in providers:
        print("  ✓ TensorRT доступен (оптимизация для RTX)")
        print("  Максимальная производительность на NVIDIA RTX GPU")

    if "DmlExecutionProvider" in providers:
        print("  ✓ DirectML доступен (универсальная GPU поддержка)")

    # 4. Создание простой тестовой модели
    print_section("Создание тестовой ONNX модели")

    # Для примера создадим простую модель вручную
    # В реальности вы будете загружать существующую модель
    print("  Создаём простую модель для демонстрации...")

    # Настройки сессии
    print_section("Настройка Inference Session")

    # Выбираем провайдера по приоритету
    if "CUDAExecutionProvider" in providers:
        print("  Используем: CUDA (GPU) с fallback на CPU")
    else:
        print("  Используем: CPU")

    # Настройки сессии для оптимизации
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    sess_options.intra_op_num_threads = 4

    print("  Настройки:")
    print(f"    - Оптимизация графа: {sess_options.graph_optimization_level}")
    print(f"    - Потоков: {sess_options.intra_op_num_threads}")

    # 5. Пример работы с реальной моделью
    print_section("Пример использования модели")
    print("""
  Для работы с вашей моделью:

  1. Загрузите ONNX модель:
     session = ort.InferenceSession('model.onnx',
                                     providers=selected_providers,
                                     sess_options=sess_options)

  2. Подготовьте входные данные:
     input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)

  3. Запустите inference:
     outputs = session.run(None, {'input': input_data})

  4. Получите результаты:
     predictions = outputs[0]
    """)

    # 6. Советы по производительности
    print_section("Советы по оптимизации производительности")
    print("""
  1. Используйте правильный Execution Provider:
     - CUDAExecutionProvider для NVIDIA GPU
     - TensorrtExecutionProvider для максимальной производительности на RTX
     - DmlExecutionProvider для универсальной GPU поддержки

  2. Включите оптимизацию графа:
     sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

  3. Настройте количество потоков:
     sess_options.intra_op_num_threads = число_ядер_CPU

  4. Используйте правильный тип данных:
     - float32 для общего использования
     - float16 для ускорения на RTX GPU

  5. Батчинг:
     - Обрабатывайте несколько входов одновременно
     - Увеличивает утилизацию GPU

  6. Кэширование TensorRT:
     - Установите ORT_TENSORRT_ENGINE_CACHE_ENABLE=1
     - Ускоряет последующие запуски
    """)

    print_section("Готово!")
    print("  Для работы с вашей моделью:")
    print("  1. Поместите ONNX модель в текущую папку")
    print("  2. Измените путь к модели в коде")
    print("  3. Запустите скрипт")


if __name__ == "__main__":
    main()
