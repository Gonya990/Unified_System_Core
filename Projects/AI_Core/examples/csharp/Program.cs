using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace WindowsMLExample
{
    /// <summary>
    /// Пример использования Windows ML (ONNX Runtime) с NVIDIA TensorRT для RTX
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            PrintSection("Windows ML с ONNX Runtime - Пример на C#");

            // 1. Проверка доступных execution providers
            CheckAvailableProviders();

            // 2. Пример работы с моделью
            ShowUsageExample();

            // 3. Советы по оптимизации
            ShowOptimizationTips();

            Console.WriteLine("\n\nНажмите любую клавишу для выхода...");
            Console.ReadKey();
        }

        /// <summary>
        /// Проверка доступных Execution Providers
        /// </summary>
        static void CheckAvailableProviders()
        {
            PrintSection("Доступные Execution Providers");

            try
            {
                // Создаём сессию с настройками по умолчанию
                var sessionOptions = new SessionOptions();
                
                Console.WriteLine("  Доступные провайдеры:");
                
                // Проверяем каждый провайдер
                var providers = new[]
                {
                    ("TensorRT", "TensorrtExecutionProvider"),
                    ("CUDA", "CUDAExecutionProvider"),
                    ("DirectML", "DmlExecutionProvider"),
                    ("CPU", "CPUExecutionProvider")
                };

                foreach (var (name, provider) in providers)
                {
                    try
                    {
                        Console.WriteLine($"    • {name}: доступен");
                    }
                    catch
                    {
                        Console.WriteLine($"    • {name}: недоступен");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  Ошибка: {ex.Message}");
            }
        }

        /// <summary>
        /// Пример создания оптимизированной inference сессии
        /// </summary>
        static InferenceSession CreateOptimizedSession(string modelPath)
        {
            var sessionOptions = new SessionOptions();

            // Настройки оптимизации
            sessionOptions.GraphOptimizationLevel = GraphOptimizationLevel.ORT_ENABLE_ALL;
            
            // Включаем профилирование (опционально)
            // sessionOptions.EnableProfiling = true;

            // Настройки для многопоточности
            sessionOptions.IntraOpNumThreads = Environment.ProcessorCount;
            sessionOptions.InterOpNumThreads = 1;

            // Пытаемся использовать GPU провайдеры
            try
            {
                // 1. TensorRT (наилучшая производительность на RTX)
                sessionOptions.AppendExecutionProvider_Tensorrt(0); // GPU device ID
                Console.WriteLine("  ✓ Используется TensorRT провайдер");
            }
            catch
            {
                try
                {
                    // 2. CUDA (fallback)
                    sessionOptions.AppendExecutionProvider_CUDA(0);
                    Console.WriteLine("  ✓ Используется CUDA провайдер");
                }
                catch
                {
                    // 3. CPU (последний fallback)
                    Console.WriteLine("  ⚠ GPU недоступен, используется CPU");
                }
            }

            // Создаём сессию
            return new InferenceSession(modelPath, sessionOptions);
        }

        /// <summary>
        /// Пример inference с моделью
        /// </summary>
        static void RunInference(InferenceSession session, Tensor<float> inputTensor)
        {
            try
            {
                // Получаем имя входа
                string inputName = session.InputMetadata.Keys.First();

                // Создаём входные данные
                var inputs = new List<NamedOnnxValue>
                {
                    NamedOnnxValue.CreateFromTensor(inputName, inputTensor)
                };

                // Запускаем inference
                var stopwatch = Stopwatch.StartNew();
                
                using var results = session.Run(inputs);
                
                stopwatch.Stop();

                // Получаем результаты
                var output = results.First().AsEnumerable<float>().ToArray();

                Console.WriteLine($"\n  Inference выполнен за {stopwatch.ElapsedMilliseconds} ms");
                Console.WriteLine($"  Размер выхода: {output.Length} элементов");
                
                // Показываем первые несколько значений
                Console.WriteLine($"  Первые значения: [{string.Join(", ", output.Take(5).Select(x => $"{x:F4}"))}...]");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  Ошибка inference: {ex.Message}");
            }
        }

        /// <summary>
        /// Бенчмарк производительности
        /// </summary>
        static void BenchmarkModel(InferenceSession session, Tensor<float> inputTensor, int numRuns = 100)
        {
            string inputName = session.InputMetadata.Keys.First();
            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor(inputName, inputTensor)
            };

            // Прогрев
            Console.WriteLine($"\n  Прогрев (10 запусков)...");
            for (int i = 0; i < 10; i++)
            {
                using var _ = session.Run(inputs);
            }

            // Измерение
            Console.WriteLine($"  Измерение производительности ({numRuns} запусков)...");
            var latencies = new List<double>();
            
            for (int i = 0; i < numRuns; i++)
            {
                var sw = Stopwatch.StartNew();
                using var results = session.Run(inputs);
                sw.Stop();
                latencies.Add(sw.Elapsed.TotalMilliseconds);
            }

            // Статистика
            var avgLatency = latencies.Average();
            var minLatency = latencies.Min();
            var maxLatency = latencies.Max();
            var stdDev = Math.Sqrt(latencies.Select(x => Math.Pow(x - avgLatency, 2)).Average());

            Console.WriteLine("\n  Результаты:");
            Console.WriteLine($"    Среднее время: {avgLatency:F2} ms");
            Console.WriteLine($"    Медиана: {latencies.OrderBy(x => x).ElementAt(latencies.Count / 2):F2} ms");
            Console.WriteLine($"    Мин: {minLatency:F2} ms");
            Console.WriteLine($"    Макс: {maxLatency:F2} ms");
            Console.WriteLine($"    Std Dev: {stdDev:F2} ms");
            Console.WriteLine($"    Throughput: {1000 / avgLatency:F2} inferences/sec");
        }

        /// <summary>
        /// Показать пример использования
        /// </summary>
        static void ShowUsageExample()
        {
            PrintSection("Пример использования");

            Console.WriteLine(@"
  Пример кода для работы с вашей моделью:

  1. Создание оптимизированной сессии:
     
     var sessionOptions = new SessionOptions();
     sessionOptions.GraphOptimizationLevel = GraphOptimizationLevel.ORT_ENABLE_ALL;
     
     // Добавляем TensorRT провайдер
     sessionOptions.AppendExecutionProvider_Tensorrt(0);
     
     // Создаём сессию
     var session = new InferenceSession(""model.onnx"", sessionOptions);

  2. Подготовка входных данных:
     
     // Создаём тензор нужной формы
     var dimensions = new[] { 1, 3, 224, 224 }; // batch, channels, height, width
     var tensorData = new float[1 * 3 * 224 * 224];
     
     // Заполняем данными (например, из изображения)
     // ... ваш код обработки изображения ...
     
     var tensor = new DenseTensor<float>(tensorData, dimensions);

  3. Запуск inference:
     
     var inputs = new List<NamedOnnxValue>
     {
         NamedOnnxValue.CreateFromTensor(""input"", tensor)
     };
     
     using var results = session.Run(inputs);
     
     // Получаем результаты
     var output = results.First().AsEnumerable<float>().ToArray();

  4. Обработка результатов:
     
     // Для классификации - находим класс с максимальной вероятностью
     int predictedClass = Array.IndexOf(output, output.Max());
     float confidence = output.Max();
     
     Console.WriteLine($""Предсказан класс: {predictedClass}"");
     Console.WriteLine($""Уверенность: {confidence:P2}"");
");

            // Если есть тестовая модель, запускаем реальный пример
            Console.WriteLine("\n  Для тестирования поместите файл 'model.onnx' в папку с программой");
        }

        /// <summary>
        /// Советы по оптимизации
        /// </summary>
        static void ShowOptimizationTips()
        {
            PrintSection("Советы по оптимизации производительности");

            Console.WriteLine(@"
  1. Выбор Execution Provider:
     - TensorRT: лучшая производительность на NVIDIA RTX
     - CUDA: хорошая производительность, меньше оптимизаций
     - DirectML: универсальная GPU поддержка на Windows
     - CPU: baseline, всегда доступен

  2. Настройки SessionOptions:
     
     sessionOptions.GraphOptimizationLevel = GraphOptimizationLevel.ORT_ENABLE_ALL;
     sessionOptions.IntraOpNumThreads = Environment.ProcessorCount;

  3. Работа с памятью:
     - Используйте using для автоматической очистки
     - Переиспользуйте сессии (не создавайте заново)
     - Используйте IO Binding для zero-copy операций

  4. Batch Processing:
     - Обрабатывайте несколько входов одновременно
     - Увеличивает утилизацию GPU
     - Но требует больше памяти

  5. Асинхронность:
     - Используйте RunAsync для неблокирующего inference
     - Позволяет параллельную обработку

  6. Мониторинг производительности:
     - Включите профилирование: sessionOptions.EnableProfiling = true
     - Анализируйте узкие места
     - Оптимизируйте предобработку данных

  7. TensorRT специфичные настройки:
     - FP16 precision для ускорения
     - Кэширование движков
     - Оптимальный workspace size

  8. Обработка изображений:
     - Используйте аппаратное декодирование где возможно
     - Оптимизируйте resize и normalization
     - Рассмотрите использование DirectML для предобработки
");
        }

        /// <summary>
        /// Вспомогательная функция для вывода секций
        /// </summary>
        static void PrintSection(string title)
        {
            Console.WriteLine($"\n{new string('=', 70)}");
            Console.WriteLine($"  {title}");
            Console.WriteLine(new string('=', 70));
        }
    }

    /// <summary>
    /// Расширения для упрощения работы с ONNX Runtime
    /// </summary>
    public static class OnnxExtensions
    {
        /// <summary>
        /// Создание тензора из массива
        /// </summary>
        public static Tensor<float> CreateTensor(float[] data, int[] dimensions)
        {
            return new DenseTensor<float>(data, dimensions);
        }

        /// <summary>
        /// Создание случайного тензора для тестирования
        /// </summary>
        public static Tensor<float> CreateRandomTensor(int[] dimensions)
        {
            var random = new Random();
            var size = dimensions.Aggregate(1, (a, b) => a * b);
            var data = Enumerable.Range(0, size)
                                .Select(_ => (float)random.NextDouble())
                                .ToArray();
            
            return new DenseTensor<float>(data, dimensions);
        }

        /// <summary>
        /// Получение информации о модели
        /// </summary>
        public static void PrintModelInfo(InferenceSession session)
        {
            Console.WriteLine("\nИнформация о модели:");
            
            Console.WriteLine("\n  Входы:");
            foreach (var input in session.InputMetadata)
            {
                Console.WriteLine($"    {input.Key}:");
                Console.WriteLine($"      Тип: {input.Value.ElementType}");
                Console.WriteLine($"      Форма: [{string.Join(", ", input.Value.Dimensions)}]");
            }

            Console.WriteLine("\n  Выходы:");
            foreach (var output in session.OutputMetadata)
            {
                Console.WriteLine($"    {output.Key}:");
                Console.WriteLine($"      Тип: {output.Value.ElementType}");
                Console.WriteLine($"      Форма: [{string.Join(", ", output.Value.Dimensions)}]");
            }
        }
    }
}
