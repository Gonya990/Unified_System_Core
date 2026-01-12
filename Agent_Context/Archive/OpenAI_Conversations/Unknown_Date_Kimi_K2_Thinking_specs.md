# Kimi K2 Thinking specs

**Date | Дата:** Unknown_Date 00:00:00

**ID:** 6931857b-8014-832d-94cd-1fa75eff3c62

---

**👤 User | Пользователь:**

kimi k2 thinking specs


**🤖 Assistant | Ассистент:**

Here are the main specs for Kimi K2 Thinking — the “Thinking” variant of the Kimi-K2 family from Moonshot AI.  Kimi K2
+2
Hugging Face
+2

✅ Key Technical Specs

Architecture: Mixture-of-Experts (MoE) — sparse model. 
Hugging Face
+2
Kimi K2
+2

Total parameters: ~ 1 trillion (1T) 
ApX Machine Learning
+2
Rival
+2

Active parameters at inference: ~ 32 billion (32B) 
Hugging Face
+1

Number of experts: ~ 384 experts; for each token the model selects ~ 8 experts. 
Hugging Face
+1

Model depth / layers: 61 layers total. 
ApX Machine Learning
+1

Attention mechanism: Multi-head attention / MLA (depending on config) with 64 attention heads. 
Hugging Face
+1

Activation function: SwiGLU. 
Hugging Face
+1

Vocabulary size: ~ 160,000 tokens. 
Hugging Face
+1

Context window (maximum input length): up to ~ 256,000 tokens (some sources report ~262.1K tokens). 
Кими K2
+2
Galaxy.ai Blog
+2

Output token limit: some builds limit outputs to ~16,384 tokens. 
Simtheory
+1

🧠 Capabilities & Design Purpose

The “Thinking” variant is explicitly optimized for deep, multi-step reasoning (long chains of thought), tool orchestration, and agentic workflows — e.g. code execution, web search, multi-step tasks, planning. 
Kimi K2
+2
Google Cloud Documentation
+2

It is designed to support 200–300 sequential tool invocations while maintaining coherence. 
Кими K2
+2
Rival
+2

It aims for “thinking while acting”: combining reasoning and function/tool calls in an interleaved way, rather than simple one-shot completion. 
Kimi K2
+2
Google Cloud Documentation
+2

Supports open-weight release under a modified MIT license, enabling self-hosting or deployment in custom infrastructures. 
Hugging Face
+2
Kimi K2
+2

📈 Performance & Benchmarks (as reported)

According to the initial reports by Moonshot AI and associated independent analysis: 
Aize
+3
Digital Applied
+3
Kimi K2
+3

On the benchmark Humanity's Last Exam (HLE) with tools — ~ 44.9% (base config) — and in “heavy mode” reportedly up to ~ 51%. 
Kimi K2
+2
Digital Applied
+2

On BrowseComp (agentic web-browsing + reasoning benchmark) — ~ 60.2%. 
Kimi K2
+2
Digital Applied
+2

On coding / programming + reasoning benchmarks (e.g. SWE-Bench Verified) — reportedly ~ 71.3%. 
Digital Applied
+1

🧰 Deployment & Inference Requirements

The weights are publicly available (open source), enabling self-hosting or local deployment. 
Hugging Face
+2
Kimi K2
+2

Out-of-the-box, the model uses native INT4 quantization (Quantization-Aware Training) — which helps reduce VRAM and memory consumption while improving speed. 
platform.moonshot.ai
+2
Kimi K2
+2

For “full precision” or high throughput, resource requirements are substantial — e.g. large RAM/VRAM or offloading strategies (depending on quantization settings) needed for best performance. 
docs.unsloth.ai
+2
Kimi K2
+2

If you like — I can also pull up typical GPU & RAM requirements to run Kimi K2 Thinking (for Quantized, Lite-deployment, and Full-performance variants), which helps evaluate feasibility for self-hosting. Do you want me to compile those for you now?

