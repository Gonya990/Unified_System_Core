"""
Пример использования ONNX Runtime с TensorRT
Демонстрирует оптимизацию производительности на NVIDIA RTX GPU
"""

import os
import time

import numpy as np
import onnxruntime as ort


def print_section(title):
    """Красивый вывод секций"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def setup_tensorrt_options():
    """Настройка опций для TensorRT"""

    # Переменные окружения для TensorRT
    tensorrt_env = {
        "ORT_TENSORRT_FP16_ENABLE": "1",  # Включить FP16 для ускорения
        "ORT_TENSORRT_ENGINE_CACHE_ENABLE": "1",  # Кэширование движков
        "ORT_TENSORRT_CACHE_PATH": "./tensorrt_cache",  # Путь к кэшу
        "ORT_TENSORRT_MAX_WORKSPACE_SIZE": "4294967296",  # 4GB workspace
    }

    for key, value in tensorrt_env.items():
        os.environ[key] = value

    return tensorrt_env


def create_inference_session(model_path, use_tensorrt=True):
    """
    Создание оптимизированной inference сессии

    Args:
        model_path: путь к ONNX модели
        use_tensorrt: использовать TensorRT провайдер
    """

    # Настройки сессии
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    # Включаем профилирование (опционально, для анализа производительности)
    # sess_options.enable_profiling = True

    # Выбор провайдеров
    providers = []
    provider_options = []

    if use_tensorrt and "TensorrtExecutionProvider" in ort.get_available_providers():
        # TensorRT провайдер с настройками
        providers.append("TensorrtExecutionProvider")
        provider_options.append(
            {
                "trt_fp16_enable": True,  # FP16 precision
                "trt_engine_cache_enable": True,  # Кэширование движков
                "trt_engine_cache_path": "./tensorrt_cache",
                "trt_max_workspace_size": 4 * 1024 * 1024 * 1024,  # 4GB
                "trt_max_partition_iterations": 1000,
            }
        )
        print("  ✓ Используется TensorRT провайдер")

    if "CUDAExecutionProvider" in ort.get_available_providers():
        # CUDA провайдер (fallback если TensorRT не подходит)
        providers.append("CUDAExecutionProvider")
        provider_options.append(
            {
                "device_id": 0,  # GPU ID
                "arena_extend_strategy": "kNextPowerOfTwo",  # Стратегия расширения памяти
                "gpu_mem_limit": 4 * 1024 * 1024 * 1024,  # 4GB лимит
                "cudnn_conv_algo_search": "EXHAUSTIVE",  # Поиск оптимального алгоритма
                "do_copy_in_default_stream": True,
            }
        )
        print("  ✓ Добавлен CUDA провайдер (fallback)")

    # CPU провайдер (последний fallback)
    providers.append("CPUExecutionProvider")
    provider_options.append({})
    print("  ✓ Добавлен CPU провайдер (fallback)")

    # Создание сессии
    try:
        session = ort.InferenceSession(
            model_path, sess_options=sess_options, providers=providers, provider_options=provider_options
        )

        print(f"\n  Активный провайдер: {session.get_providers()[0]}")
        return session

    except Exception as e:
        print(f"  ✗ Ошибка создания сессии: {e}")
        return None


def benchmark_model(session, input_data, num_runs=100, warmup_runs=10):
    """
    Бенчмарк производительности модели

    Args:
        session: ONNX Runtime сессия
        input_data: входные данные
        num_runs: количество запусков для измерения
        warmup_runs: количество прогревочных запусков
    """

    input_name = session.get_inputs()[0].name

    print(f"\n  Прогрев ({warmup_runs} запусков)...")
    for _ in range(warmup_runs):
        session.run(None, {input_name: input_data})

    print(f"  Измерение производительности ({num_runs} запусков)...")

    latencies = []
    for _ in range(num_runs):
        start = time.perf_counter()
        session.run(None, {input_name: input_data})
        end = time.perf_counter()
        latencies.append((end - start) * 1000)  # в миллисекундах

    # Статистика
    latencies = np.array(latencies)

    print("\n  Результаты:")
    print(f"    Среднее время: {np.mean(latencies):.2f} ms")
    print(f"    Медиана: {np.median(latencies):.2f} ms")
    print(f"    Мин: {np.min(latencies):.2f} ms")
    print(f"    Макс: {np.max(latencies):.2f} ms")
    print(f"    Std Dev: {np.std(latencies):.2f} ms")
    print(f"    Throughput: {1000 / np.mean(latencies):.2f} inferences/sec")

    return latencies


def compare_providers(model_path, input_shape):
    """
    Сравнение производительности разных провайдеров
    """

    print_section("Сравнение производительности провайдеров")

    # Создаём тестовые данные
    input_data = np.random.randn(*input_shape).astype(np.float32)

    results = {}

    # Тест TensorRT
    if "TensorrtExecutionProvider" in ort.get_available_providers():
        print("\n[1] TensorRT провайдер:")
        session = create_inference_session(model_path, use_tensorrt=True)
        if session:
            latencies = benchmark_model(session, input_data)
            results["TensorRT"] = np.mean(latencies)

    # Тест CUDA
    if "CUDAExecutionProvider" in ort.get_available_providers():
        print("\n[2] CUDA провайдер:")
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        session = ort.InferenceSession(model_path, providers=["CUDAExecutionProvider"], sess_options=sess_options)
        latencies = benchmark_model(session, input_data)
        results["CUDA"] = np.mean(latencies)

    # Тест CPU
    print("\n[3] CPU провайдер (baseline):")
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"], sess_options=sess_options)
    latencies = benchmark_model(session, input_data)
    results["CPU"] = np.mean(latencies)

    # Итоговое сравнение
    print_section("Итоговое сравнение")

    baseline = results.get("CPU", 0)
    for provider, latency in sorted(results.items(), key=lambda x: x[1]):
        speedup = baseline / latency if latency > 0 else 0
        print(f"  {provider:15s}: {latency:7.2f} ms (ускорение {speedup:.2f}x)")


def main():
    print_section("ONNX Runtime с TensorRT оптимизацией")

    # Проверка доступных провайдеров
    print("\nДоступные провайдеры:")
    providers = ort.get_available_providers()
    for provider in providers:
        print(f"  • {provider}")

    # Настройка TensorRT
    if "TensorrtExecutionProvider" in providers:
        print_section("Настройка TensorRT")
        tensorrt_env = setup_tensorrt_options()
        for key, value in tensorrt_env.items():
            print(f"  {key}={value}")

    # Пример использования с моделью
    print_section("Пример использования")

    print("""
  Шаги для использования с вашей моделью:

  1. Поместите вашу ONNX модель в текущую папку

  2. Загрузите модель:
     model_path = 'your_model.onnx'
     session = create_inference_session(model_path, use_tensorrt=True)

  3. Подготовьте входные данные:
     # Пример для модели классификации изображений
     input_shape = (1, 3, 224, 224)  # (batch, channels, height, width)
     input_data = np.random.randn(*input_shape).astype(np.float32)

  4. Запустите inference:
     input_name = session.get_inputs()[0].name
     outputs = session.run(None, {input_name: input_data})

  5. Получите результаты:
     predictions = outputs[0]

  6. Сравните производительность:
     compare_providers(model_path, input_shape)
    """)

    # Советы по оптимизации
    print_section("Советы по оптимизации для TensorRT")
    print("""
  1. FP16 Precision:
     - Включайте FP16 для ускорения на RTX GPU
     - Может привести к небольшой потере точности
     - Обычно приемлемо для большинства задач

  2. Кэширование TensorRT движков:
     - Первый запуск медленный (компиляция)
     - Последующие запуски быстрые (используют кэш)
     - Кэш сохраняется в tensorrt_cache/

  3. Workspace Size:
     - Больше памяти = больше оптимизаций
     - По умолчанию 4GB обычно достаточно
     - Увеличьте если есть больше VRAM

  4. Batch Size:
     - Больший batch = лучшая утилизация GPU
     - Но требует больше памяти
     - Найдите оптимальный для вашей модели

  5. Динамические размеры:
     - TensorRT лучше работает с фиксированными размерами
     - Избегайте динамических размеров если возможно

  6. Профилирование:
     - Используйте sess_options.enable_profiling = True
     - Анализируйте узкие места
     - Оптимизируйте критичные операции
    """)

    print_section("Готово!")


if __name__ == "__main__":
    main()
