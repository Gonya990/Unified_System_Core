# Примеры использования Windows ML с ONNX Runtime

Эта папка содержит примеры кода на Python и C# для работы с Windows ML и ONNX Runtime на NVIDIA RTX GPU.

## Python примеры

### 1. `onnx-runtime-basic.py`
Базовый пример использования ONNX Runtime.

**Что демонстрирует:**
- Проверка доступных execution providers
- Создание inference сессии
- Базовые настройки производительности

**Запуск:**
```bash
python onnx-runtime-basic.py
```

### 2. `onnx-runtime-tensorrt.py`
Продвинутый пример с TensorRT оптимизацией.

**Что демонстрирует:**
- Настройка TensorRT провайдера
- FP16 precision
- Кэширование TensorRT движков
- Бенчмарк производительности
- Сравнение разных провайдеров

**Запуск:**
```bash
python onnx-runtime-tensorrt.py
```

### 3. `optimize-model-example.py`
Пример оптимизации модели с Olive Toolkit.

**Что демонстрирует:**
- Квантование моделей
- FP16 конверсия
- Оптимизация для GPU/CPU/NPU
- Сравнение производительности до и после оптимизации

**Запуск:**
```bash
# Базовая оптимизация
python optimize-model-example.py --model your_model.onnx

# С FP16
python optimize-model-example.py --model your_model.onnx --fp16

# С квантованием
python optimize-model-example.py --model your_model.onnx --quantize

# Сравнение моделей
python optimize-model-example.py --model original.onnx --compare optimized.onnx
```

## C# примеры

### `WindowsMLExample`
Полнофункциональный пример на C# для Windows приложений.

**Что демонстрирует:**
- Создание оптимизированной inference сессии
- Работа с TensorRT и CUDA провайдерами
- Бенчмарк производительности
- Best practices для .NET приложений

**Сборка и запуск:**
```powershell
cd examples/csharp
dotnet build
dotnet run
```

**Или используя Visual Studio:**
1. Откройте `WindowsMLExample.csproj` в Visual Studio
2. Нажмите F5 для сборки и запуска

## Требования

### Для Python примеров:
```bash
pip install onnxruntime-gpu
pip install onnx numpy pillow
pip install torch torchvision  # для некоторых примеров
pip install olive-ai  # для оптимизации моделей
```

### Для C# примеров:
- .NET 8.0 SDK или новее
- Visual Studio 2022 (опционально, для удобства разработки)

Зависимости устанавливаются автоматически через NuGet:
- Microsoft.ML.OnnxRuntime
- Microsoft.ML.OnnxRuntime.Gpu
- System.Drawing.Common
- SixLabors.ImageSharp

## Где взять ONNX модели для тестирования

1. **ONNX Model Zoo:**
   - https://github.com/onnx/models
   - Готовые модели для различных задач

2. **Hugging Face:**
   - https://huggingface.co/models?library=onnx
   - Модели с поддержкой ONNX экспорта

3. **Конвертация из PyTorch:**
   ```python
   import torch
   
   model = YourModel()
   dummy_input = torch.randn(1, 3, 224, 224)
   
   torch.onnx.export(
       model,
       dummy_input,
       "model.onnx",
       input_names=['input'],
       output_names=['output'],
       dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}}
   )
   ```

4. **Конвертация из TensorFlow:**
   ```bash
   pip install tf2onnx
   python -m tf2onnx.convert --saved-model tensorflow_model/ --output model.onnx
   ```

## Типичные задачи и примеры

### Классификация изображений

**Python:**
```python
import onnxruntime as ort
import numpy as np
from PIL import Image

# Загрузка модели
session = ort.InferenceSession('resnet50.onnx', 
                               providers=['CUDAExecutionProvider'])

# Загрузка и предобработка изображения
img = Image.open('image.jpg').resize((224, 224))
img_array = np.array(img).transpose(2, 0, 1).astype(np.float32)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Inference
outputs = session.run(None, {'input': img_array})
predictions = outputs[0][0]

# Топ-5 классов
top5_idx = np.argsort(predictions)[-5:][::-1]
```

**C#:**
```csharp
var session = new InferenceSession("resnet50.onnx", sessionOptions);

// Загрузка изображения
var image = Image.Load<Rgb24>("image.jpg");
image.Mutate(x => x.Resize(224, 224));

// Конвертация в тензор
var tensor = ImageToTensor(image);

// Inference
var inputs = new[] { NamedOnnxValue.CreateFromTensor("input", tensor) };
using var results = session.Run(inputs);
```

### Обработка текста (NLP)

**Python:**
```python
from transformers import AutoTokenizer

# Токенизация
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
inputs = tokenizer("Hello, world!", return_tensors="np")

# Inference
session = ort.InferenceSession('bert.onnx', 
                               providers=['CUDAExecutionProvider'])
outputs = session.run(None, {
    'input_ids': inputs['input_ids'],
    'attention_mask': inputs['attention_mask']
})
```

### Генерация (Image-to-Image)

**Python:**
```python
# Для моделей типа Stable Diffusion, Super Resolution и т.д.
session = ort.InferenceSession('model.onnx',
                               providers=['TensorrtExecutionProvider', 
                                        'CUDAExecutionProvider'])

latents = np.random.randn(1, 4, 64, 64).astype(np.float32)
outputs = session.run(None, {'latents': latents})
```

## Оптимизация производительности

### 1. Выбор правильного провайдера

```python
# Приоритет провайдеров для максимальной производительности:
providers = [
    'TensorrtExecutionProvider',  # Лучшее для RTX
    'CUDAExecutionProvider',      # Fallback для GPU
    'CPUExecutionProvider'        # Последний fallback
]

session = ort.InferenceSession(model_path, providers=providers)
```

### 2. Настройка SessionOptions

```python
sess_options = ort.SessionOptions()

# Максимальная оптимизация графа
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

# Многопоточность
sess_options.intra_op_num_threads = 4
sess_options.inter_op_num_threads = 1

# Профилирование (для отладки)
# sess_options.enable_profiling = True
```

### 3. IO Binding (для zero-copy)

```python
io_binding = session.io_binding()

# Привязываем входы и выходы к GPU памяти
io_binding.bind_input(
    name='input',
    device_type='cuda',
    device_id=0,
    element_type=np.float32,
    shape=(1, 3, 224, 224),
    buffer_ptr=input_tensor.data_ptr()
)

io_binding.bind_output('output')

# Запускаем
session.run_with_iobinding(io_binding)
outputs = io_binding.copy_outputs_to_cpu()
```

## Устранение проблем

### Модель не использует GPU

**Проверьте:**
1. Установлен ли onnxruntime-gpu (не onnxruntime)
2. Доступен ли CUDA провайдер:
   ```python
   print(ort.get_available_providers())
   ```
3. Установлены ли драйверы NVIDIA

**Решение:**
```bash
pip uninstall onnxruntime
pip install onnxruntime-gpu
```

### Медленный первый запуск с TensorRT

Это нормально! TensorRT компилирует оптимизированные движки при первом запуске.

**Решение:**
Включите кэширование:
```python
os.environ['ORT_TENSORRT_ENGINE_CACHE_ENABLE'] = '1'
os.environ['ORT_TENSORRT_CACHE_PATH'] = './tensorrt_cache'
```

### Out of Memory ошибки

**Решение:**
1. Уменьшите batch size
2. Используйте FP16 вместо FP32
3. Ограничьте workspace size:
   ```python
   os.environ['ORT_TENSORRT_MAX_WORKSPACE_SIZE'] = '2147483648'  # 2GB
   ```

### Низкая производительность

**Проверьте:**
1. Используете ли правильный провайдер (TensorRT или CUDA, не CPU)
2. Включена ли оптимизация графа
3. Оптимальный ли batch size
4. Не тратится ли время на копирование данных между CPU и GPU

## Дополнительные ресурсы

- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)
- [ONNX Runtime Performance Tuning](https://onnxruntime.ai/docs/performance/)
- [TensorRT Execution Provider](https://onnxruntime.ai/docs/execution-providers/TensorRT-ExecutionProvider.html)
- [Olive Documentation](https://github.com/microsoft/Olive)
- [Windows ML Samples](https://github.com/microsoft/Windows-Machine-Learning)
