---
name: mlops-llm-infrastructure-suite
description: >-
  High-Throughput LLM & MLOps Infrastructure Suite: Low-latency inference with vLLM, serverless GPU scaling with Modal, HuggingFace Hub artifact governance, and quantized Llama.cpp deployment.
version: 2.0.0
tags:
  - mlops
  - vllm
  - modal
  - gpu
  - huggingface
  - llama-cpp
  - inference
merged_member_skills:
  - huggingface-hub (01_Hermes_Skills_Core_Library\mlops\huggingface-hub\SKILL.md)
  - llama-cpp (01_Hermes_Skills_Core_Library\mlops\inference\llama-cpp\SKILL.md)
  - modal-serverless-gpu (01_Hermes_Skills_Core_Library\mlops\cloud\modal\SKILL.md)
  - serving-llms-vllm (01_Hermes_Skills_Core_Library\mlops\inference\vllm\SKILL.md)
---

# Mlops Llm Infrastructure Suite

> **Master Suite Consolidée :** Regroupe et unifie **4 compétences spécialisées** de l'écosystème Hermes en une référence modulaire et cohérente.


## 🎯 Quand Déclencher cette Master Suite (Triggers)
Cette suite doit être activée dès que l'utilisateur mentionne l'un des mots-clés, frameworks, outils ou objectifs liés aux modules inclus ci-dessous.
Chaque module peut être exécuté individuellement ou orchestré en séquence selon la tâche demandée.

---
## 📋 Vue d'Ensemble & Sommaire des Modules

1. **[huggingface-hub](#module-1-huggingface-hub)** : Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, deploy inference endpoints, manage Spaces and buckets.
2. **[llama-cpp](#module-2-llama-cpp)** : Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware. Use for edge deployment, M1/M2/M3 Macs, AMD/Intel GPUs, or when CUDA is unavailable. Supports GGUF quantization (1.5-8 bit) for reduced memory and 4-10× speedup vs PyTorch on CPU.
3. **[modal-serverless-gpu](#module-3-modal-serverless-gpu)** : Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models as APIs, or running batch jobs with automatic scaling.
4. **[serving-llms-vllm](#module-4-serving-llms-vllm)** : Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory. Supports OpenAI-compatible endpoints, quantization (GPTQ/AWQ/FP8), and tensor parallelism.

---

## Module 1: `huggingface-hub`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\huggingface-hub\SKILL.md`
- **Rôle / Objectif :** Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, deploy inference endpoints, manage Spaces and buckets.

## Hugging Face CLI (`hf`) Reference Guide

The `hf` command is the modern command-line interface for interacting with the Hugging Face Hub, providing tools to manage repositories, models, datasets, and Spaces.

> **IMPORTANT:** The `hf` command replaces the now deprecated `huggingface-cli` command.

### Quick Start
*   **Installation:** `curl -LsSf https://hf.co/cli/install.sh | bash -s`
*   **Help:** Use `hf --help` to view all available functions and real-world examples.
*   **Authentication:** Recommended via `HF_TOKEN` environment variable or the `--token` flag.

---

### Core Commands

#### General Operations
*   `hf download REPO_ID`: Download files from the Hub.
*   `hf upload REPO_ID`: Upload files/folders (recommended for single-commit).
*   `hf upload-large-folder REPO_ID LOCAL_PATH`: Recommended for resumable uploads of large directories.
*   `hf sync`: Sync files between a local directory and a bucket.
*   `hf env` / `hf version`: View environment and version details.

#### Authentication (`hf auth`)
*   `login` / `logout`: Manage sessions using tokens from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
*   `list` / `switch`: Manage and toggle between multiple stored access tokens.
*   `whoami`: Identify the currently logged-in account.

#### Repository Management (`hf repos`)
*   `create` / `delete`: Create or permanently remove repositories.
*   `duplicate`: Clone a model, dataset, or Space to a new ID.
*   `move`: Transfer a repository between namespaces.
*   `branch` / `tag`: Manage Git-like references.
*   `delete-files`: Remove specific files using patterns.

---

### Specialized Hub Interactions

#### Datasets & Models
*   **Datasets:** `hf datasets list`, `info`, and `parquet` (list parquet URLs).
*   **SQL Queries:** `hf datasets sql SQL` — Execute raw SQL via DuckDB against dataset parquet URLs.
*   **Models:** `hf models list` and `info`.
*   **Papers:** `hf papers list` — View daily papers.

#### Discussions & Pull Requests (`hf discussions`)
*   Manage the lifecycle of Hub contributions: `list`, `create`, `info`, `comment`, `close`, `reopen`, and `rename`.
*   `diff`: View changes in a PR.
*   `merge`: Finalize pull requests.

#### Infrastructure & Compute
*   **Endpoints:** Deploy and manage Inference Endpoints (`deploy`, `pause`, `resume`, `scale-to-zero`, `catalog`).
*   **Jobs:** Run compute tasks on HF infrastructure. Includes `hf jobs uv` for running Python scripts with inline dependencies and `stats` for resource monitoring.
*   **Spaces:** Manage interactive apps. Includes `dev-mode` and `hot-reload` for Python files without full restarts.

#### Storage & Automation
*   **Buckets:** Full S3-like bucket management (`create`, `cp`, `mv`, `rm`, `sync`).
*   **Cache:** Manage local storage with `list`, `prune` (remove detached revisions), and `verify` (checksum checks).
*   **Webhooks:** Automate workflows by managing Hub webhooks (`create`, `watch`, `enable`/`disable`).
*   **Collections:** Organize Hub items into collections (`add-item`, `update`, `list`).

---

### Advanced Usage & Tips

#### Global Flags
*   `--format json`: Produces machine-readable output for automation.
*   `-q` / `--quiet`: Limits output to IDs only.

#### Extensions & Skills
*   **Extensions:** Extend CLI functionality via GitHub repositories using `hf extensions install REPO_ID`.
*   **Skills:** Manage AI assistant skills with `hf skills add`.


---

## Module 2: `llama-cpp`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\inference\llama-cpp\SKILL.md`
- **Rôle / Objectif :** Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware. Use for edge deployment, M1/M2/M3 Macs, AMD/Intel GPUs, or when CUDA is unavailable. Supports GGUF quantization (1.5-8 bit) for reduced memory and 4-10× speedup vs PyTorch on CPU.

## llama.cpp

Pure C/C++ LLM inference with minimal dependencies, optimized for CPUs and non-NVIDIA hardware.

### When to use llama.cpp

**Use llama.cpp when:**
- Running on CPU-only machines
- Deploying on Apple Silicon (M1/M2/M3/M4)
- Using AMD or Intel GPUs (no CUDA)
- Edge deployment (Raspberry Pi, embedded systems)
- Need simple deployment without Docker/Python

**Use TensorRT-LLM instead when:**
- Have NVIDIA GPUs (A100/H100)
- Need maximum throughput (100K+ tok/s)
- Running in datacenter with CUDA

**Use vLLM instead when:**
- Have NVIDIA GPUs
- Need Python-first API
- Want PagedAttention

### Quick start

#### Installation

```bash
## macOS/Linux
brew install llama.cpp

## Or build from source
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

## With Metal (Apple Silicon)
make LLAMA_METAL=1

## With CUDA (NVIDIA)
make LLAMA_CUDA=1

## With ROCm (AMD)
make LLAMA_HIP=1
```

#### Download model

```bash
## Download from HuggingFace (GGUF format)
huggingface-cli download \
    TheBloke/Llama-2-7B-Chat-GGUF \
    llama-2-7b-chat.Q4_K_M.gguf \
    --local-dir models/

## Or convert from HuggingFace
python convert_hf_to_gguf.py models/llama-2-7b-chat/
```

#### Run inference

```bash
## Simple chat
./llama-cli \
    -m models/llama-2-7b-chat.Q4_K_M.gguf \
    -p "Explain quantum computing" \
    -n 256  # Max tokens

## Interactive chat
./llama-cli \
    -m models/llama-2-7b-chat.Q4_K_M.gguf \
    --interactive
```

#### Server mode

```bash
## Start OpenAI-compatible server
./llama-server \
    -m models/llama-2-7b-chat.Q4_K_M.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -ngl 32  # Offload 32 layers to GPU

## Client request
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-2-7b-chat",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

### Quantization formats

#### GGUF format overview

| Format | Bits | Size (7B) | Speed | Quality | Use Case |
|--------|------|-----------|-------|---------|----------|
| **Q4_K_M** | 4.5 | 4.1 GB | Fast | Good | **Recommended default** |
| Q4_K_S | 4.3 | 3.9 GB | Faster | Lower | Speed critical |
| Q5_K_M | 5.5 | 4.8 GB | Medium | Better | Quality critical |
| Q6_K | 6.5 | 5.5 GB | Slower | Best | Maximum quality |
| Q8_0 | 8.0 | 7.0 GB | Slow | Excellent | Minimal degradation |
| Q2_K | 2.5 | 2.7 GB | Fastest | Poor | Testing only |

#### Choosing quantization

```bash
## General use (balanced)
Q4_K_M  # 4-bit, medium quality

## Maximum speed (more degradation)
Q2_K or Q3_K_M

## Maximum quality (slower)
Q6_K or Q8_0

## Very large models (70B, 405B)
Q3_K_M or Q4_K_S  # Lower bits to fit in memory
```

### Hardware acceleration

#### Apple Silicon (Metal)

```bash
## Build with Metal
make LLAMA_METAL=1

## Run with GPU acceleration (automatic)
./llama-cli -m model.gguf -ngl 999  # Offload all layers

## Performance: M3 Max 40-60 tokens/sec (Llama 2-7B Q4_K_M)
```

#### NVIDIA GPUs (CUDA)

```bash
## Build with CUDA
make LLAMA_CUDA=1

## Offload layers to GPU
./llama-cli -m model.gguf -ngl 35  # Offload 35/40 layers

## Hybrid CPU+GPU for large models
./llama-cli -m llama-70b.Q4_K_M.gguf -ngl 20  # GPU: 20 layers, CPU: rest
```

#### AMD GPUs (ROCm)

```bash
## Build with ROCm
make LLAMA_HIP=1

## Run with AMD GPU
./llama-cli -m model.gguf -ngl 999
```

### Common patterns

#### Batch processing

```bash
## Process multiple prompts from file
cat prompts.txt | ./llama-cli \
    -m model.gguf \
    --batch-size 512 \
    -n 100
```

#### Constrained generation

```bash
## JSON output with grammar
./llama-cli \
    -m model.gguf \
    -p "Generate a person: " \
    --grammar-file grammars/json.gbnf

## Outputs valid JSON only
```

#### Context size

```bash
## Increase context (default 512)
./llama-cli \
    -m model.gguf \
    -c 4096  # 4K context window

## Very long context (if model supports)
./llama-cli -m model.gguf -c 32768  # 32K context
```

### Performance benchmarks

#### CPU performance (Llama 2-7B Q4_K_M)

| CPU | Threads | Speed | Cost |
|-----|---------|-------|------|
| Apple M3 Max | 16 | 50 tok/s | $0 (local) |
| AMD Ryzen 9 7950X | 32 | 35 tok/s | $0.50/hour |
| Intel i9-13900K | 32 | 30 tok/s | $0.40/hour |
| AWS c7i.16xlarge | 64 | 40 tok/s | $2.88/hour |

#### GPU acceleration (Llama 2-7B Q4_K_M)

| GPU | Speed | vs CPU | Cost |
|-----|-------|--------|------|
| NVIDIA RTX 4090 | 120 tok/s | 3-4× | $0 (local) |
| NVIDIA A10 | 80 tok/s | 2-3× | $1.00/hour |
| AMD MI250 | 70 tok/s | 2× | $2.00/hour |
| Apple M3 Max (Metal) | 50 tok/s | ~Same | $0 (local) |

### Supported models

**LLaMA family**:
- Llama 2 (7B, 13B, 70B)
- Llama 3 (8B, 70B, 405B)
- Code Llama

**Mistral family**:
- Mistral 7B
- Mixtral 8x7B, 8x22B

**Other**:
- Falcon, BLOOM, GPT-J
- Phi-3, Gemma, Qwen
- LLaVA (vision), Whisper (audio)

**Find models**: https://huggingface.co/models?library=gguf

### References

- **[Quantization Guide](references/llama-cpp_quantization.md)** - GGUF formats, conversion, quality comparison
- **[Server Deployment](references/llama-cpp_server.md)** - API endpoints, Docker, monitoring
- **[Optimization](references/llama-cpp_optimization.md)** - Performance tuning, hybrid CPU+GPU

### Resources

- **GitHub**: https://github.com/ggerganov/llama.cpp
- **Models**: https://huggingface.co/models?library=gguf
- **Discord**: https://discord.gg/llama-cpp


---

## Module 3: `modal-serverless-gpu`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\cloud\modal\SKILL.md`
- **Rôle / Objectif :** Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models as APIs, or running batch jobs with automatic scaling.

## Modal Serverless GPU

Comprehensive guide to running ML workloads on Modal's serverless GPU cloud platform.

### When to use Modal

**Use Modal when:**
- Running GPU-intensive ML workloads without managing infrastructure
- Deploying ML models as auto-scaling APIs
- Running batch processing jobs (training, inference, data processing)
- Need pay-per-second GPU pricing without idle costs
- Prototyping ML applications quickly
- Running scheduled jobs (cron-like workloads)

**Key features:**
- **Serverless GPUs**: T4, L4, A10G, L40S, A100, H100, H200, B200 on-demand
- **Python-native**: Define infrastructure in Python code, no YAML
- **Auto-scaling**: Scale to zero, scale to 100+ GPUs instantly
- **Sub-second cold starts**: Rust-based infrastructure for fast container launches
- **Container caching**: Image layers cached for rapid iteration
- **Web endpoints**: Deploy functions as REST APIs with zero-downtime updates

**Use alternatives instead:**
- **RunPod**: For longer-running pods with persistent state
- **Lambda Labs**: For reserved GPU instances
- **SkyPilot**: For multi-cloud orchestration and cost optimization
- **Kubernetes**: For complex multi-service architectures

### Quick start

#### Installation

```bash
pip install modal
modal setup  # Opens browser for authentication
```

#### Hello World with GPU

```python
import modal

app = modal.App("hello-gpu")

@app.function(gpu="T4")
def gpu_info():
    import subprocess
    return subprocess.run(["nvidia-smi"], capture_output=True, text=True).stdout

@app.local_entrypoint()
def main():
    print(gpu_info.remote())
```

Run: `modal run hello_gpu.py`

#### Basic inference endpoint

```python
import modal

app = modal.App("text-generation")
image = modal.Image.debian_slim().pip_install("transformers", "torch", "accelerate")

@app.cls(gpu="A10G", image=image)
class TextGenerator:
    @modal.enter()
    def load_model(self):
        from transformers import pipeline
        self.pipe = pipeline("text-generation", model="gpt2", device=0)

    @modal.method()
    def generate(self, prompt: str) -> str:
        return self.pipe(prompt, max_length=100)[0]["generated_text"]

@app.local_entrypoint()
def main():
    print(TextGenerator().generate.remote("Hello, world"))
```

### Core concepts

#### Key components

| Component | Purpose |
|-----------|---------|
| `App` | Container for functions and resources |
| `Function` | Serverless function with compute specs |
| `Cls` | Class-based functions with lifecycle hooks |
| `Image` | Container image definition |
| `Volume` | Persistent storage for models/data |
| `Secret` | Secure credential storage |

#### Execution modes

| Command | Description |
|---------|-------------|
| `modal run script.py` | Execute and exit |
| `modal serve script.py` | Development with live reload |
| `modal deploy script.py` | Persistent cloud deployment |

### GPU configuration

#### Available GPUs

| GPU | VRAM | Best For |
|-----|------|----------|
| `T4` | 16GB | Budget inference, small models |
| `L4` | 24GB | Inference, Ada Lovelace arch |
| `A10G` | 24GB | Training/inference, 3.3x faster than T4 |
| `L40S` | 48GB | Recommended for inference (best cost/perf) |
| `A100-40GB` | 40GB | Large model training |
| `A100-80GB` | 80GB | Very large models |
| `H100` | 80GB | Fastest, FP8 + Transformer Engine |
| `H200` | 141GB | Auto-upgrade from H100, 4.8TB/s bandwidth |
| `B200` | Latest | Blackwell architecture |

#### GPU specification patterns

```python
## Single GPU
@app.function(gpu="A100")

## Specific memory variant
@app.function(gpu="A100-80GB")

## Multiple GPUs (up to 8)
@app.function(gpu="H100:4")

## GPU with fallbacks
@app.function(gpu=["H100", "A100", "L40S"])

## Any available GPU
@app.function(gpu="any")
```

### Container images

```python
## Basic image with pip
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "torch==2.1.0", "transformers==4.36.0", "accelerate"
)

## From CUDA base
image = modal.Image.from_registry(
    "nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04",
    add_python="3.11"
).pip_install("torch", "transformers")

## With system packages
image = modal.Image.debian_slim().apt_install("git", "ffmpeg").pip_install("whisper")
```

### Persistent storage

```python
volume = modal.Volume.from_name("model-cache", create_if_missing=True)

@app.function(gpu="A10G", volumes={"/models": volume})
def load_model():
    import os
    model_path = "/models/llama-7b"
    if not os.path.exists(model_path):
        model = download_model()
        model.save_pretrained(model_path)
        volume.commit()  # Persist changes
    return load_from_path(model_path)
```

### Web endpoints

#### FastAPI endpoint decorator

```python
@app.function()
@modal.fastapi_endpoint(method="POST")
def predict(text: str) -> dict:
    return {"result": model.predict(text)}
```

#### Full ASGI app

```python
from fastapi import FastAPI
web_app = FastAPI()

@web_app.post("/predict")
async def predict(text: str):
    return {"result": await model.predict.remote.aio(text)}

@app.function()
@modal.asgi_app()
def fastapi_app():
    return web_app
```

#### Web endpoint types

| Decorator | Use Case |
|-----------|----------|
| `@modal.fastapi_endpoint()` | Simple function → API |
| `@modal.asgi_app()` | Full FastAPI/Starlette apps |
| `@modal.wsgi_app()` | Django/Flask apps |
| `@modal.web_server(port)` | Arbitrary HTTP servers |

### Dynamic batching

```python
@app.function()
@modal.batched(max_batch_size=32, wait_ms=100)
async def batch_predict(inputs: list[str]) -> list[dict]:
    # Inputs automatically batched
    return model.batch_predict(inputs)
```

### Secrets management

```bash
## Create secret
modal secret create huggingface HF_TOKEN=hf_xxx
```

```python
@app.function(secrets=[modal.Secret.from_name("huggingface")])
def download_model():
    import os
    token = os.environ["HF_TOKEN"]
```

### Scheduling

```python
@app.function(schedule=modal.Cron("0 0 * * *"))  # Daily midnight
def daily_job():
    pass

@app.function(schedule=modal.Period(hours=1))
def hourly_job():
    pass
```

### Performance optimization

#### Cold start mitigation

```python
@app.function(
    container_idle_timeout=300,  # Keep warm 5 min
    allow_concurrent_inputs=10,  # Handle concurrent requests
)
def inference():
    pass
```

#### Model loading best practices

```python
@app.cls(gpu="A100")
class Model:
    @modal.enter()  # Run once at container start
    def load(self):
        self.model = load_model()  # Load during warm-up

    @modal.method()
    def predict(self, x):
        return self.model(x)
```

### Parallel processing

```python
@app.function()
def process_item(item):
    return expensive_computation(item)

@app.function()
def run_parallel():
    items = list(range(1000))
    # Fan out to parallel containers
    results = list(process_item.map(items))
    return results
```

### Common configuration

```python
@app.function(
    gpu="A100",
    memory=32768,              # 32GB RAM
    cpu=4,                     # 4 CPU cores
    timeout=3600,              # 1 hour max
    container_idle_timeout=120,# Keep warm 2 min
    retries=3,                 # Retry on failure
    concurrency_limit=10,      # Max concurrent containers
)
def my_function():
    pass
```

### Debugging

```python
## Test locally
if __name__ == "__main__":
    result = my_function.local()

## View logs
## modal app logs my-app
```

### Common issues

| Issue | Solution |
|-------|----------|
| Cold start latency | Increase `container_idle_timeout`, use `@modal.enter()` |
| GPU OOM | Use larger GPU (`A100-80GB`), enable gradient checkpointing |
| Image build fails | Pin dependency versions, check CUDA compatibility |
| Timeout errors | Increase `timeout`, add checkpointing |

### References

- **[Advanced Usage](references/modal-serverless-gpu_advanced-usage.md)** - Multi-GPU, distributed training, cost optimization
- **[Troubleshooting](references/modal-serverless-gpu_troubleshooting.md)** - Common issues and solutions

### Resources

- **Documentation**: https://modal.com/docs
- **Examples**: https://github.com/modal-labs/modal-examples
- **Pricing**: https://modal.com/pricing
- **Discord**: https://discord.gg/modal


---

## Module 4: `serving-llms-vllm`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\inference\vllm\SKILL.md`
- **Rôle / Objectif :** Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory. Supports OpenAI-compatible endpoints, quantization (GPTQ/AWQ/FP8), and tensor parallelism.

## vLLM - High-Performance LLM Serving

### Quick start

vLLM achieves 24x higher throughput than standard transformers through PagedAttention (block-based KV cache) and continuous batching (mixing prefill/decode requests).

**Installation**:
```bash
pip install vllm
```

**Basic offline inference**:
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct")
sampling = SamplingParams(temperature=0.7, max_tokens=256)

outputs = llm.generate(["Explain quantum computing"], sampling)
print(outputs[0].outputs[0].text)
```

**OpenAI-compatible server**:
```bash
vllm serve meta-llama/Llama-3-8B-Instruct

## Query with OpenAI SDK
python -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8000/v1', api_key='EMPTY')
print(client.chat.completions.create(
    model='meta-llama/Llama-3-8B-Instruct',
    messages=[{'role': 'user', 'content': 'Hello!'}]
).choices[0].message.content)
"
```

### Common workflows

#### Workflow 1: Production API deployment

Copy this checklist and track progress:

```
Deployment Progress:
- [ ] Step 1: Configure server settings
- [ ] Step 2: Test with limited traffic
- [ ] Step 3: Enable monitoring
- [ ] Step 4: Deploy to production
- [ ] Step 5: Verify performance metrics
```

**Step 1: Configure server settings**

Choose configuration based on your model size:

```bash
## For 7B-13B models on single GPU
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192 \
  --port 8000

## For 30B-70B models with tensor parallelism
vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9 \
  --quantization awq \
  --port 8000

## For production with caching and metrics
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching \
  --enable-metrics \
  --metrics-port 9090 \
  --port 8000 \
  --host 0.0.0.0
```

**Step 2: Test with limited traffic**

Run load test before production:

```bash
## Install load testing tool
pip install locust

## Create test_load.py with sample requests
## Run: locust -f test_load.py --host http://localhost:8000
```

Verify TTFT (time to first token) < 500ms and throughput > 100 req/sec.

**Step 3: Enable monitoring**

vLLM exposes Prometheus metrics on port 9090:

```bash
curl http://localhost:9090/metrics | grep vllm
```

Key metrics to monitor:
- `vllm:time_to_first_token_seconds` - Latency
- `vllm:num_requests_running` - Active requests
- `vllm:gpu_cache_usage_perc` - KV cache utilization

**Step 4: Deploy to production**

Use Docker for consistent deployment:

```bash
## Run vLLM in Docker
docker run --gpus all -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching
```

**Step 5: Verify performance metrics**

Check that deployment meets targets:
- TTFT < 500ms (for short prompts)
- Throughput > target req/sec
- GPU utilization > 80%
- No OOM errors in logs

#### Workflow 2: Offline batch inference

For processing large datasets without server overhead.

Copy this checklist:

```
Batch Processing:
- [ ] Step 1: Prepare input data
- [ ] Step 2: Configure LLM engine
- [ ] Step 3: Run batch inference
- [ ] Step 4: Process results
```

**Step 1: Prepare input data**

```python
## Load prompts from file
prompts = []
with open("prompts.txt") as f:
    prompts = [line.strip() for line in f]

print(f"Loaded {len(prompts)} prompts")
```

**Step 2: Configure LLM engine**

```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Llama-3-8B-Instruct",
    tensor_parallel_size=2,  # Use 2 GPUs
    gpu_memory_utilization=0.9,
    max_model_len=4096
)

sampling = SamplingParams(
    temperature=0.7,
    top_p=0.95,
    max_tokens=512,
    stop=["</s>", "\n\n"]
)
```

**Step 3: Run batch inference**

vLLM automatically batches requests for efficiency:

```python
## Process all prompts in one call
outputs = llm.generate(prompts, sampling)

## vLLM handles batching internally
## No need to manually chunk prompts
```

**Step 4: Process results**

```python
## Extract generated text
results = []
for output in outputs:
    prompt = output.prompt
    generated = output.outputs[0].text
    results.append({
        "prompt": prompt,
        "generated": generated,
        "tokens": len(output.outputs[0].token_ids)
    })

## Save to file
import json
with open("results.jsonl", "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")

print(f"Processed {len(results)} prompts")
```

#### Workflow 3: Quantized model serving

Fit large models in limited GPU memory.

```
Quantization Setup:
- [ ] Step 1: Choose quantization method
- [ ] Step 2: Find or create quantized model
- [ ] Step 3: Launch with quantization flag
- [ ] Step 4: Verify accuracy
```

**Step 1: Choose quantization method**

- **AWQ**: Best for 70B models, minimal accuracy loss
- **GPTQ**: Wide model support, good compression
- **FP8**: Fastest on H100 GPUs

**Step 2: Find or create quantized model**

Use pre-quantized models from HuggingFace:

```bash
## Search for AWQ models
## Example: TheBloke/Llama-2-70B-AWQ
```

**Step 3: Launch with quantization flag**

```bash
## Using pre-quantized model
vllm serve TheBloke/Llama-2-70B-AWQ \
  --quantization awq \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.95

## Results: 70B model in ~40GB VRAM
```

**Step 4: Verify accuracy**

Test outputs match expected quality:

```python
## Compare quantized vs non-quantized responses
## Verify task-specific performance unchanged
```

### When to use vs alternatives

**Use vLLM when:**
- Deploying production LLM APIs (100+ req/sec)
- Serving OpenAI-compatible endpoints
- Limited GPU memory but need large models
- Multi-user applications (chatbots, assistants)
- Need low latency with high throughput

**Use alternatives instead:**
- **llama.cpp**: CPU/edge inference, single-user
- **HuggingFace transformers**: Research, prototyping, one-off generation
- **TensorRT-LLM**: NVIDIA-only, need absolute maximum performance
- **Text-Generation-Inference**: Already in HuggingFace ecosystem

### Common issues

**Issue: Out of memory during model loading**

Reduce memory usage:
```bash
vllm serve MODEL \
  --gpu-memory-utilization 0.7 \
  --max-model-len 4096
```

Or use quantization:
```bash
vllm serve MODEL --quantization awq
```

**Issue: Slow first token (TTFT > 1 second)**

Enable prefix caching for repeated prompts:
```bash
vllm serve MODEL --enable-prefix-caching
```

For long prompts, enable chunked prefill:
```bash
vllm serve MODEL --enable-chunked-prefill
```

**Issue: Model not found error**

Use `--trust-remote-code` for custom models:
```bash
vllm serve MODEL --trust-remote-code
```

**Issue: Low throughput (<50 req/sec)**

Increase concurrent sequences:
```bash
vllm serve MODEL --max-num-seqs 512
```

Check GPU utilization with `nvidia-smi` - should be >80%.

**Issue: Inference slower than expected**

Verify tensor parallelism uses power of 2 GPUs:
```bash
vllm serve MODEL --tensor-parallel-size 4  # Not 3
```

Enable speculative decoding for faster generation:
```bash
vllm serve MODEL --speculative-model DRAFT_MODEL
```

### Advanced topics

**Server deployment patterns**: See [references/serving-llms-vllm_server-deployment.md](references/serving-llms-vllm_server-deployment.md) for Docker, Kubernetes, and load balancing configurations.

**Performance optimization**: See [references/llama-cpp_optimization.md](references/llama-cpp_optimization.md) for PagedAttention tuning, continuous batching details, and benchmark results.

**Quantization guide**: See [references/llama-cpp_quantization.md](references/llama-cpp_quantization.md) for AWQ/GPTQ/FP8 setup, model preparation, and accuracy comparisons.

**Troubleshooting**: See [references/modal-serverless-gpu_troubleshooting.md](references/modal-serverless-gpu_troubleshooting.md) for detailed error messages, debugging steps, and performance diagnostics.

### Hardware requirements

- **Small models (7B-13B)**: 1x A10 (24GB) or A100 (40GB)
- **Medium models (30B-40B)**: 2x A100 (40GB) with tensor parallelism
- **Large models (70B+)**: 4x A100 (40GB) or 2x A100 (80GB), use AWQ/GPTQ

Supported platforms: NVIDIA (primary), AMD ROCm, Intel GPUs, TPUs

### Resources

- Official docs: https://docs.vllm.ai
- GitHub: https://github.com/vllm-project/vllm
- Paper: "Efficient Memory Management for Large Language Model Serving with PagedAttention" (SOSP 2023)
- Community: https://discuss.vllm.ai


---
