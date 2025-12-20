"""
Пример оптимизации модели с помощью Olive Toolkit
Демонстрирует квантование и оптимизацию для NVIDIA RTX GPU
"""

import os
import json
import argparse
from pathlib import Path


def print_section(title):
    """Красивый вывод секций"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def create_optimization_config(
    model_path,
    output_dir="optimized_model",
    target_device="gpu",
    enable_fp16=True,
    enable_quantization=False
):
    """
    Создание конфигурации оптимизации для Olive
    
    Args:
        model_path: путь к исходной ONNX модели
        output_dir: папка для сохранения результатов
        target_device: целевое устройство (gpu/cpu/npu)
        enable_fp16: использовать FP16 precision
        enable_quantization: использовать квантование
    """
    
    config = {
        "input_model": {
            "type": "OnnxModel",
            "model_path": str(model_path)
        },
        "systems": {
            "local_system": {
                "type": "LocalSystem",
                "accelerators": []
            }
        },
        "evaluators": {
            "common_evaluator": {
                "metrics": [
                    {
                        "name": "latency",
                        "type": "latency",
                        "sub_types": [
                            {"name": "avg", "priority": 1},
                            {"name": "max", "priority": 2},
                            {"name": "min", "priority": 3}
                        ],
                        "user_config": {
                            "io_bind": True
                        }
                    }
                ]
            }
        },
        "passes": {},
        "engine": {
            "search_strategy": {
                "execution_order": "joint",
                "search_algorithm": "exhaustive"
            },
            "evaluator": "common_evaluator",
            "target": "local_system",
            "cache_dir": "cache",
            "output_dir": output_dir
        }
    }
    
    # Настройка для GPU
    if target_device == "gpu":
        config["systems"]["local_system"]["accelerators"].append({
            "device": "gpu",
            "execution_providers": [
                "TensorrtExecutionProvider",
                "CUDAExecutionProvider"
            ]
        })
        
        # Оптимизация графа для GPU
        config["passes"]["optimize"] = {
            "type": "OrtTransformersOptimization",
            "disable_search": True
        }
        
        # FP16 конверсия
        if enable_fp16:
            config["passes"]["convert_to_fp16"] = {
                "type": "OnnxFloatToFloat16"
            }
        
        # Квантование (опционально)
        if enable_quantization:
            config["passes"]["quantization"] = {
                "type": "OnnxDynamicQuantization",
                "weight_type": "QUInt8"
            }
    
    # Настройка для CPU
    elif target_device == "cpu":
        config["systems"]["local_system"]["accelerators"].append({
            "device": "cpu",
            "execution_providers": ["CPUExecutionProvider"]
        })
        
        config["passes"]["optimize"] = {
            "type": "OrtTransformersOptimization"
        }
        
        # Динамическое квантование для CPU
        config["passes"]["quantization"] = {
            "type": "OnnxDynamicQuantization",
            "weight_type": "QInt8"
        }
    
    return config


def optimize_model(model_path, config_path=None, output_dir="optimized_model"):
    """
    Запуск оптимизации модели через Olive
    
    Args:
        model_path: путь к ONNX модели
        config_path: путь к конфигурации (опционально)
        output_dir: папка для результатов
    """
    
    print_section(f"Оптимизация модели: {model_path}")
    
    # Проверка существования модели
    if not Path(model_path).exists():
        print(f"  ✗ Модель не найдена: {model_path}")
        return False
    
    # Если конфигурация не указана, создаём автоматически
    if config_path is None:
        print("  Создание конфигурации автоматически...")
        config = create_optimization_config(
            model_path=model_path,
            output_dir=output_dir,
            target_device="gpu",
            enable_fp16=True,
            enable_quantization=False
        )
        
        config_path = "temp_olive_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"  ✓ Конфигурация сохранена: {config_path}")
    
    # Запуск Olive
    print("\n  Запуск Olive оптимизации...")
    print("  (это может занять несколько минут...)\n")
    
    try:
        from olive.workflows import run as olive_run
        
        # Загружаем конфигурацию
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Запускаем оптимизацию
        olive_run(config)
        
        print_section("Оптимизация завершена!")
        print(f"  ✓ Результаты сохранены в: {output_dir}")
        
        # Показываем результаты
        output_path = Path(output_dir)
        if output_path.exists():
            print("\n  Оптимизированные модели:")
            for model_file in output_path.rglob("*.onnx"):
                size_mb = model_file.stat().st_size / (1024 * 1024)
                print(f"    • {model_file.name} ({size_mb:.2f} MB)")
        
        return True
    
    except ImportError:
        print("  ✗ Olive не установлен!")
        print("  Установите: pip install olive-ai")
        return False
    
    except Exception as e:
        print(f"  ✗ Ошибка оптимизации: {e}")
        return False


def compare_models(original_path, optimized_path):
    """
    Сравнение производительности оригинальной и оптимизированной модели
    """
    
    print_section("Сравнение производительности")
    
    try:
        import numpy as np
        import onnxruntime as ort
        import time
        
        # Загружаем обе модели
        print("  Загрузка моделей...")
        original_session = ort.InferenceSession(
            original_path,
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        )
        
        optimized_session = ort.InferenceSession(
            optimized_path,
            providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
        )
        
        # Получаем информацию о входе
        input_name = original_session.get_inputs()[0].name
        input_shape = original_session.get_inputs()[0].shape
        
        # Заменяем динамические размеры на фиксированные
        input_shape = [1 if isinstance(dim, str) else dim for dim in input_shape]
        
        print(f"  Входная форма: {input_shape}")
        
        # Создаём тестовые данные
        input_data = np.random.randn(*input_shape).astype(np.float32)
        
        # Бенчмарк оригинальной модели
        print("\n  Тестирование оригинальной модели...")
        warmup = 10
        runs = 100
        
        for _ in range(warmup):
            original_session.run(None, {input_name: input_data})
        
        original_times = []
        for _ in range(runs):
            start = time.perf_counter()
            original_session.run(None, {input_name: input_data})
            end = time.perf_counter()
            original_times.append((end - start) * 1000)
        
        # Бенчмарк оптимизированной модели
        print("  Тестирование оптимизированной модели...")
        
        for _ in range(warmup):
            optimized_session.run(None, {input_name: input_data})
        
        optimized_times = []
        for _ in range(runs):
            start = time.perf_counter()
            optimized_session.run(None, {input_name: input_data})
            end = time.perf_counter()
            optimized_times.append((end - start) * 1000)
        
        # Результаты
        original_avg = np.mean(original_times)
        optimized_avg = np.mean(optimized_times)
        speedup = original_avg / optimized_avg
        
        print_section("Результаты сравнения")
        print(f"  Оригинальная модель:")
        print(f"    Среднее время: {original_avg:.2f} ms")
        print(f"    Throughput: {1000/original_avg:.2f} inferences/sec")
        
        print(f"\n  Оптимизированная модель:")
        print(f"    Среднее время: {optimized_avg:.2f} ms")
        print(f"    Throughput: {1000/optimized_avg:.2f} inferences/sec")
        
        print(f"\n  Ускорение: {speedup:.2f}x")
        
        # Размеры файлов
        original_size = Path(original_path).stat().st_size / (1024 * 1024)
        optimized_size = Path(optimized_path).stat().st_size / (1024 * 1024)
        compression = original_size / optimized_size
        
        print(f"\n  Размер файлов:")
        print(f"    Оригинал: {original_size:.2f} MB")
        print(f"    Оптимизирован: {optimized_size:.2f} MB")
        print(f"    Сжатие: {compression:.2f}x")
        
    except Exception as e:
        print(f"  ✗ Ошибка сравнения: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Оптимизация ONNX модели с помощью Olive"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Путь к ONNX модели для оптимизации"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Путь к конфигурации Olive (опционально)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="optimized_model",
        help="Папка для сохранения результатов"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="gpu",
        choices=["gpu", "cpu", "npu"],
        help="Целевое устройство"
    )
    parser.add_argument(
        "--fp16",
        action="store_true",
        help="Использовать FP16 precision"
    )
    parser.add_argument(
        "--quantize",
        action="store_true",
        help="Применить квантование"
    )
    parser.add_argument(
        "--compare",
        type=str,
        default=None,
        help="Путь к оптимизированной модели для сравнения"
    )
    
    args = parser.parse_args()
    
    print_section("Olive Model Optimization Tool")
    
    # Если модель не указана, показываем инструкции
    if not args.model:
        print("""
  Использование:
  
  1. Базовая оптимизация:
     python optimize-model-example.py --model your_model.onnx
  
  2. С FP16 precision:
     python optimize-model-example.py --model your_model.onnx --fp16
  
  3. С квантованием:
     python optimize-model-example.py --model your_model.onnx --quantize
  
  4. С пользовательской конфигурацией:
     python optimize-model-example.py --model your_model.onnx --config config.json
  
  5. Сравнение моделей:
     python optimize-model-example.py --model original.onnx --compare optimized.onnx
        """)
        
        print_section("Примеры конфигураций")
        print("  Готовые примеры находятся в папке configs/")
        return
    
    # Оптимизация модели
    if args.compare is None:
        success = optimize_model(
            model_path=args.model,
            config_path=args.config,
            output_dir=args.output
        )
        
        if success:
            print("\n  Следующие шаги:")
            print("  1. Проверьте оптимизированные модели в папке output")
            print("  2. Сравните производительность:")
            print(f"     python optimize-model-example.py --model {args.model} --compare {args.output}/model.onnx")
    
    # Сравнение моделей
    else:
        compare_models(args.model, args.compare)


if __name__ == "__main__":
    main()
