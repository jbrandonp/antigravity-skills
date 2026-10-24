---
name: llm-structured-generation-eval-suite
description: >-
  Structured LLM Generation, Quantization & Evaluation Suite: JSON/grammar constrained generation (Outlines, Guidance), LM Evaluation Harness, Weights & Biases telemetry, and GGUF quantization.
version: 2.0.0
tags:
  - llm
  - structured-generation
  - outlines
  - guidance
  - gguf
  - eval-harness
  - wandb
merged_member_skills:
  - lm-evaluation-harness (01_Hermes_Skills_Core_Library/mlops/evaluation/lm-evaluation-harness/SKILL.md)
  - gguf-quantization (01_Hermes_Skills_Core_Library\mlops\inference\gguf\SKILL.md)
  - guidance (01_Hermes_Skills_Core_Library\mlops\inference\guidance\SKILL.md)
  - obliteratus (01_Hermes_Skills_Core_Library\mlops\inference\obliteratus\SKILL.md)
  - outlines (01_Hermes_Skills_Core_Library\mlops\inference\outlines\SKILL.md)
  - weights-and-biases (01_Hermes_Skills_Core_Library\mlops\evaluation\weights-and-biases\SKILL.md)
---

# Llm Structured Generation Eval Suite

> **Master Suite Consolidée :** Regroupe et unifie **5 compétences spécialisées** de l'écosystème Hermes en une référence modulaire et cohérente.


## 🎯 Quand Déclencher cette Master Suite (Triggers)
Cette suite doit être activée dès que l'utilisateur mentionne l'un des mots-clés, frameworks, outils ou objectifs liés aux modules inclus ci-dessous.
Chaque module peut être exécuté individuellement ou orchestré en séquence selon la tâche demandée.

---
## 📋 Vue d'Ensemble & Sommaire des Modules

1. **[gguf-quantization](#module-1-gguf-quantization)** : GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing flexible quantization from 2-8 bit without GPU requirements.
2. **[guidance](#module-2-guidance)** : Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance - Microsoft Research's constrained generation framework
3. **[obliteratus](#module-3-obliteratus)** : Remove refusal behaviors from open-weight LLMs using OBLITERATUS — mechanistic interpretability techniques (diff-in-means, SVD, whitened SVD, LEACE, SAE decomposition, etc.) to excise guardrails while preserving reasoning. 9 CLI methods, 28 analysis modules, 116 model presets across 5 compute tiers, tournament evaluation, and telemetry-driven recommendations. Use when a user wants to uncensor, abliterate, or remove refusal from an LLM.
4. **[outlines](#module-4-outlines)** : Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and maximize inference speed with Outlines - dottxt.ai's structured generation library
5. **[weights-and-biases](#module-5-weights-and-biases)** : Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B - collaborative MLOps platform

---

## Module 1: `gguf-quantization`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\inference\gguf\SKILL.md`
- **Rôle / Objectif :** GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing flexible quantization from 2-8 bit without GPU requirements.

## GGUF - Quantization Format for llama.cpp

The GGUF (GPT-Generated Unified Format) is the standard file format for llama.cpp, enabling efficient inference on CPUs, Apple Silicon, and GPUs with flexible quantization options.

### When to use GGUF

**Use GGUF when:**
- Deploying on consumer hardware (laptops, desktops)
- Running on Apple Silicon (M1/M2/M3) with Metal acceleration
- Need CPU inference without GPU requirements
- Want flexible quantization (Q2_K to Q8_0)
- Using local AI tools (LM Studio, Ollama, text-generation-webui)

**Key advantages:**
- **Universal hardware**: CPU, Apple Silicon, NVIDIA, AMD support
- **No Python runtime**: Pure C/C++ inference
- **Flexible quantization**: 2-8 bit with various methods (K-quants)
- **Ecosystem support**: LM Studio, Ollama, koboldcpp, and more
- **imatrix**: Importance matrix for better low-bit quality

**Use alternatives instead:**
- **AWQ/GPTQ**: Maximum accuracy with calibration on NVIDIA GPUs
- **HQQ**: Fast calibration-free quantization for HuggingFace
- **bitsandbytes**: Simple integration with transformers library
- **TensorRT-LLM**: Production NVIDIA deployment with maximum speed

### Quick start

#### Installation

```bash
## Clone llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

## Build (CPU)
make

## Build with CUDA (NVIDIA)
make GGML_CUDA=1

## Build with Metal (Apple Silicon)
make GGML_METAL=1

## Install Python bindings (optional)
pip install llama-cpp-python
```

#### Convert model to GGUF

```bash
## Install requirements
pip install -r requirements.txt

## Convert HuggingFace model to GGUF (FP16)
python convert_hf_to_gguf.py ./path/to/model --outfile model-f16.gguf

## Or specify output type
python convert_hf_to_gguf.py ./path/to/model \
    --outfile model-f16.gguf \
    --outtype f16
```

#### Quantize model

```bash
## Basic quantization to Q4_K_M
./llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M

## Quantize with importance matrix (better quality)
./llama-imatrix -m model-f16.gguf -f calibration.txt -o model.imatrix
./llama-quantize --imatrix model.imatrix model-f16.gguf model-q4_k_m.gguf Q4_K_M
```

#### Run inference

```bash
## CLI inference
./llama-cli -m model-q4_k_m.gguf -p "Hello, how are you?"

## Interactive mode
./llama-cli -m model-q4_k_m.gguf --interactive

## With GPU offload
./llama-cli -m model-q4_k_m.gguf -ngl 35 -p "Hello!"
```

### Quantization types

#### K-quant methods (recommended)

| Type | Bits | Size (7B) | Quality | Use Case |
|------|------|-----------|---------|----------|
| Q2_K | 2.5 | ~2.8 GB | Low | Extreme compression |
| Q3_K_S | 3.0 | ~3.0 GB | Low-Med | Memory constrained |
| Q3_K_M | 3.3 | ~3.3 GB | Medium | Balance |
| Q4_K_S | 4.0 | ~3.8 GB | Med-High | Good balance |
| Q4_K_M | 4.5 | ~4.1 GB | High | **Recommended default** |
| Q5_K_S | 5.0 | ~4.6 GB | High | Quality focused |
| Q5_K_M | 5.5 | ~4.8 GB | Very High | High quality |
| Q6_K | 6.0 | ~5.5 GB | Excellent | Near-original |
| Q8_0 | 8.0 | ~7.2 GB | Best | Maximum quality |

#### Legacy methods

| Type | Description |
|------|-------------|
| Q4_0 | 4-bit, basic |
| Q4_1 | 4-bit with delta |
| Q5_0 | 5-bit, basic |
| Q5_1 | 5-bit with delta |

**Recommendation**: Use K-quant methods (Q4_K_M, Q5_K_M) for best quality/size ratio.

### Conversion workflows

#### Workflow 1: HuggingFace to GGUF

```bash
## 1. Download model
huggingface-cli download meta-llama/Llama-3.1-8B --local-dir ./llama-3.1-8b

## 2. Convert to GGUF (FP16)
python convert_hf_to_gguf.py ./llama-3.1-8b \
    --outfile llama-3.1-8b-f16.gguf \
    --outtype f16

## 3. Quantize
./llama-quantize llama-3.1-8b-f16.gguf llama-3.1-8b-q4_k_m.gguf Q4_K_M

## 4. Test
./llama-cli -m llama-3.1-8b-q4_k_m.gguf -p "Hello!" -n 50
```

#### Workflow 2: With importance matrix (better quality)

```bash
## 1. Convert to GGUF
python convert_hf_to_gguf.py ./model --outfile model-f16.gguf

## 2. Create calibration text (diverse samples)
cat > calibration.txt << 'EOF'
The quick brown fox jumps over the lazy dog.
Machine learning is a subset of artificial intelligence.
Python is a popular programming language.
## Add more diverse text samples...
EOF

## 3. Generate importance matrix
./llama-imatrix -m model-f16.gguf \
    -f calibration.txt \
    --chunk 512 \
    -o model.imatrix \
    -ngl 35  # GPU layers if available

## 4. Quantize with imatrix
./llama-quantize --imatrix model.imatrix \
    model-f16.gguf \
    model-q4_k_m.gguf \
    Q4_K_M
```

#### Workflow 3: Multiple quantizations

```bash
##!/bin/bash
MODEL="llama-3.1-8b-f16.gguf"
IMATRIX="llama-3.1-8b.imatrix"

## Generate imatrix once
./llama-imatrix -m $MODEL -f wiki.txt -o $IMATRIX -ngl 35

## Create multiple quantizations
for QUANT in Q4_K_M Q5_K_M Q6_K Q8_0; do
    OUTPUT="llama-3.1-8b-${QUANT,,}.gguf"
    ./llama-quantize --imatrix $IMATRIX $MODEL $OUTPUT $QUANT
    echo "Created: $OUTPUT ($(du -h $OUTPUT | cut -f1))"
done
```

### Python usage

#### llama-cpp-python

```python
from llama_cpp import Llama

## Load model
llm = Llama(
    model_path="./model-q4_k_m.gguf",
    n_ctx=4096,          # Context window
    n_gpu_layers=35,     # GPU offload (0 for CPU only)
    n_threads=8          # CPU threads
)

## Generate
output = llm(
    "What is machine learning?",
    max_tokens=256,
    temperature=0.7,
    stop=["</s>", "\n\n"]
)
print(output["choices"][0]["text"])
```

#### Chat completion

```python
from llama_cpp import Llama

llm = Llama(
    model_path="./model-q4_k_m.gguf",
    n_ctx=4096,
    n_gpu_layers=35,
    chat_format="llama-3"  # Or "chatml", "mistral", etc.
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]

response = llm.create_chat_completion(
    messages=messages,
    max_tokens=256,
    temperature=0.7
)
print(response["choices"][0]["message"]["content"])
```

#### Streaming

```python
from llama_cpp import Llama

llm = Llama(model_path="./model-q4_k_m.gguf", n_gpu_layers=35)

## Stream tokens
for chunk in llm(
    "Explain quantum computing:",
    max_tokens=256,
    stream=True
):
    print(chunk["choices"][0]["text"], end="", flush=True)
```

### Server mode

#### Start OpenAI-compatible server

```bash
## Start server
./llama-server -m model-q4_k_m.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -ngl 35 \
    -c 4096

## Or with Python bindings
python -m llama_cpp.server \
    --model model-q4_k_m.gguf \
    --n_gpu_layers 35 \
    --host 0.0.0.0 \
    --port 8080
```

#### Use with OpenAI client

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=256
)
print(response.choices[0].message.content)
```

### Hardware optimization

#### Apple Silicon (Metal)

```bash
## Build with Metal
make clean && make GGML_METAL=1

## Run with Metal acceleration
./llama-cli -m model.gguf -ngl 99 -p "Hello"

## Python with Metal
llm = Llama(
    model_path="model.gguf",
    n_gpu_layers=99,     # Offload all layers
    n_threads=1          # Metal handles parallelism
)
```

#### NVIDIA CUDA

```bash
## Build with CUDA
make clean && make GGML_CUDA=1

## Run with CUDA
./llama-cli -m model.gguf -ngl 35 -p "Hello"

## Specify GPU
CUDA_VISIBLE_DEVICES=0 ./llama-cli -m model.gguf -ngl 35
```

#### CPU optimization

```bash
## Build with AVX2/AVX512
make clean && make

## Run with optimal threads
./llama-cli -m model.gguf -t 8 -p "Hello"

## Python CPU config
llm = Llama(
    model_path="model.gguf",
    n_gpu_layers=0,      # CPU only
    n_threads=8,         # Match physical cores
    n_batch=512          # Batch size for prompt processing
)
```

### Integration with tools

#### Ollama

```bash
## Create Modelfile
cat > Modelfile << 'EOF'
FROM ./model-q4_k_m.gguf
TEMPLATE """{{ .System }}
{{ .Prompt }}"""
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
EOF

## Create Ollama model
ollama create mymodel -f Modelfile

## Run
ollama run mymodel "Hello!"
```

#### LM Studio

1. Place GGUF file in `~/.cache/lm-studio/models/`
2. Open LM Studio and select the model
3. Configure context length and GPU offload
4. Start inference

#### text-generation-webui

```bash
## Place in models folder
cp model-q4_k_m.gguf text-generation-webui/models/

## Start with llama.cpp loader
python server.py --model model-q4_k_m.gguf --loader llama.cpp --n-gpu-layers 35
```

### Best practices

1. **Use K-quants**: Q4_K_M offers best quality/size balance
2. **Use imatrix**: Always use importance matrix for Q4 and below
3. **GPU offload**: Offload as many layers as VRAM allows
4. **Context length**: Start with 4096, increase if needed
5. **Thread count**: Match physical CPU cores, not logical
6. **Batch size**: Increase n_batch for faster prompt processing

### Common issues

**Model loads slowly:**
```bash
## Use mmap for faster loading
./llama-cli -m model.gguf --mmap
```

**Out of memory:**
```bash
## Reduce GPU layers
./llama-cli -m model.gguf -ngl 20  # Reduce from 35

## Or use smaller quantization
./llama-quantize model-f16.gguf model-q3_k_m.gguf Q3_K_M
```

**Poor quality at low bits:**
```bash
## Always use imatrix for Q4 and below
./llama-imatrix -m model-f16.gguf -f calibration.txt -o model.imatrix
./llama-quantize --imatrix model.imatrix model-f16.gguf model-q4_k_m.gguf Q4_K_M
```

### References

- **[Advanced Usage](references/advanced-usage.md)** - Batching, speculative decoding, custom builds
- **[Troubleshooting](references/troubleshooting.md)** - Common issues, debugging, benchmarks

### Resources

- **Repository**: https://github.com/ggml-org/llama.cpp
- **Python Bindings**: https://github.com/abetlen/llama-cpp-python
- **Pre-quantized Models**: https://huggingface.co/TheBloke
- **GGUF Converter**: https://huggingface.co/spaces/ggml-org/gguf-my-repo
- **License**: MIT


---

## Module 2: `guidance`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\inference\guidance\SKILL.md`
- **Rôle / Objectif :** Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance - Microsoft Research's constrained generation framework

## Guidance: Constrained LLM Generation

### When to Use This Skill

Use Guidance when you need to:
- **Control LLM output syntax** with regex or grammars
- **Guarantee valid JSON/XML/code** generation
- **Reduce latency** vs traditional prompting approaches
- **Enforce structured formats** (dates, emails, IDs, etc.)
- **Build multi-step workflows** with Pythonic control flow
- **Prevent invalid outputs** through grammatical constraints

**GitHub Stars**: 18,000+ | **From**: Microsoft Research

### Installation

```bash
## Base installation
pip install guidance

## With specific backends
pip install guidance[transformers]  # Hugging Face models
pip install guidance[llama_cpp]     # llama.cpp models
```

### Quick Start

#### Basic Example: Structured Generation

```python
from guidance import models, gen

## Load model (supports OpenAI, Transformers, llama.cpp)
lm = models.OpenAI("gpt-4")

## Generate with constraints
result = lm + "The capital of France is " + gen("capital", max_tokens=5)

print(result["capital"])  # "Paris"
```

#### With Anthropic Claude

```python
from guidance import models, gen, system, user, assistant

## Configure Claude
lm = models.Anthropic("claude-sonnet-4-5-20250929")

## Use context managers for chat format
with system():
    lm += "You are a helpful assistant."

with user():
    lm += "What is the capital of France?"

with assistant():
    lm += gen(max_tokens=20)
```

### Core Concepts

#### 1. Context Managers

Guidance uses Pythonic context managers for chat-style interactions.

```python
from guidance import system, user, assistant, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

## System message
with system():
    lm += "You are a JSON generation expert."

## User message
with user():
    lm += "Generate a person object with name and age."

## Assistant response
with assistant():
    lm += gen("response", max_tokens=100)

print(lm["response"])
```

**Benefits:**
- Natural chat flow
- Clear role separation
- Easy to read and maintain

#### 2. Constrained Generation

Guidance ensures outputs match specified patterns using regex or grammars.

##### Regex Constraints

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

## Constrain to valid email format
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

## Constrain to date format (YYYY-MM-DD)
lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}")

## Constrain to phone number
lm += "Phone: " + gen("phone", regex=r"\d{3}-\d{3}-\d{4}")

print(lm["email"])  # Guaranteed valid email
print(lm["date"])   # Guaranteed YYYY-MM-DD format
```

**How it works:**
- Regex converted to grammar at token level
- Invalid tokens filtered during generation
- Model can only produce matching outputs

##### Selection Constraints

```python
from guidance import models, gen, select

lm = models.Anthropic("claude-sonnet-4-5-20250929")

## Constrain to specific choices
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")

## Multiple-choice selection
lm += "Best answer: " + select(
    ["A) Paris", "B) London", "C) Berlin", "D) Madrid"],
    name="answer"
)

print(lm["sentiment"])  # One of: positive, negative, neutral
print(lm["answer"])     # One of: A, B, C, or D
```

#### 3. Token Healing

Guidance automatically "heals" token boundaries between prompt and generation.

**Problem:** Tokenization creates unnatural boundaries.

```python
## Without token healing
prompt = "The capital of France is "
## Last token: " is "
## First generated token might be " Par" (with leading space)
## Result: "The capital of France is  Paris" (double space!)
```

**Solution:** Guidance backs up one token and regenerates.

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

## Token healing enabled by default
lm += "The capital of France is " + gen("capital", max_tokens=5)
## Result: "The capital of France is Paris" (correct spacing)
```

**Benefits:**
- Natural text boundaries
- No awkward spacing issues
- Better model performance (sees natural token sequences)

#### 4. Grammar-Based Generation

Define complex structures using context-free grammars.

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

## JSON grammar (simplified)
json_grammar = """
{
    "name": <gen name regex="[A-Za-z ]+" max_tokens=20>,
    "age": <gen age regex="[0-9]+" max_tokens=3>,
    "email": <gen email regex="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}" max_tokens=50>
}
"""

## Generate valid JSON
lm += gen("person", grammar=json_grammar)

print(lm["person"])  # Guaranteed valid JSON structure
```

**Use cases:**
- Complex structured outputs
- Nested data structures
- Programming language syntax
- Domain-specific languages

#### 5. Guidance Functions

Create reusable generation patterns with the `@guidance` decorator.

```python
from guidance import guidance, gen, models

@guidance
def generate_person(lm):
    """Generate a person with name and age."""
    lm += "Name: " + gen("name", max_tokens=20, stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+", max_tokens=3)
    return lm

## Use the function
lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = generate_person(lm)

print(lm["name"])
print(lm["age"])
```

**Stateful Functions:**

```python
@guidance(stateless=False)
def react_agent(lm, question, tools, max_rounds=5):
    """ReAct agent with tool use."""
    lm += f"Question: {question}\n\n"

    for i in range(max_rounds):
        # Thought
        lm += f"Thought {i+1}: " + gen("thought", stop="\n")

        # Action
        lm += "\nAction: " + select(list(tools.keys()), name="action")

        # Execute tool
        tool_result = tools[lm["action"]]()
        lm += f"\nObservation: {tool_result}\n\n"

        # Check if done
        lm += "Done? " + select(["Yes", "No"], name="done")
        if lm["done"] == "Yes":
            break

    # Final answer
    lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
    return lm
```

### Backend Configuration

#### Anthropic Claude

```python
from guidance import models

lm = models.Anthropic(
    model="claude-sonnet-4-5-20250929",
    api_key="your-api-key"  # Or set ANTHROPIC_API_KEY env var
)
```

#### OpenAI

```python
lm = models.OpenAI(
    model="gpt-4o-mini",
    api_key="your-api-key"  # Or set OPENAI_API_KEY env var
)
```

#### Local Models (Transformers)

```python
from guidance.models import Transformers

lm = Transformers(
    "microsoft/Phi-4-mini-instruct",
    device="cuda"  # Or "cpu"
)
```

#### Local Models (llama.cpp)

```python
from guidance.models import LlamaCpp

lm = LlamaCpp(
    model_path="/path/to/model.gguf",
    n_ctx=4096,
    n_gpu_layers=35
)
```

### Common Patterns

#### Pattern 1: JSON Generation

```python
from guidance import models, gen, system, user, assistant

lm = models.Anthropic("claude-sonnet-4-5-20250929")

with system():
    lm += "You generate valid JSON."

with user():
    lm += "Generate a user profile with name, age, and email."

with assistant():
    lm += """{
    "name": """ + gen("name", regex=r'"[A-Za-z ]+"', max_tokens=30) + """,
    "age": """ + gen("age", regex=r"[0-9]+", max_tokens=3) + """,
    "email": """ + gen("email", regex=r'"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"', max_tokens=50) + """
}"""

print(lm)  # Valid JSON guaranteed
```

#### Pattern 2: Classification

```python
from guidance import models, gen, select

lm = models.Anthropic("claude-sonnet-4-5-20250929")

text = "This product is amazing! I love it."

lm += f"Text: {text}\n"
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")
lm += "\nConfidence: " + gen("confidence", regex=r"[0-9]+", max_tokens=3) + "%"

print(f"Sentiment: {lm['sentiment']}")
print(f"Confidence: {lm['confidence']}%")
```

#### Pattern 3: Multi-Step Reasoning

```python
from guidance import models, gen, guidance

@guidance
def chain_of_thought(lm, question):
    """Generate answer with step-by-step reasoning."""
    lm += f"Question: {question}\n\n"

    # Generate multiple reasoning steps
    for i in range(3):
        lm += f"Step {i+1}: " + gen(f"step_{i+1}", stop="\n", max_tokens=100) + "\n"

    # Final answer
    lm += "\nTherefore, the answer is: " + gen("answer", max_tokens=50)

    return lm

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = chain_of_thought(lm, "What is 15% of 200?")

print(lm["answer"])
```

#### Pattern 4: ReAct Agent

```python
from guidance import models, gen, select, guidance

@guidance(stateless=False)
def react_agent(lm, question):
    """ReAct agent with tool use."""
    tools = {
        "calculator": lambda expr: eval(expr),
        "search": lambda query: f"Search results for: {query}",
    }

    lm += f"Question: {question}\n\n"

    for round in range(5):
        # Thought
        lm += f"Thought: " + gen("thought", stop="\n") + "\n"

        # Action selection
        lm += "Action: " + select(["calculator", "search", "answer"], name="action")

        if lm["action"] == "answer":
            lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
            break

        # Action input
        lm += "\nAction Input: " + gen("action_input", stop="\n") + "\n"

        # Execute tool
        if lm["action"] in tools:
            result = tools[lm["action"]](lm["action_input"])
            lm += f"Observation: {result}\n\n"

    return lm

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = react_agent(lm, "What is 25 * 4 + 10?")
print(lm["answer"])
```

#### Pattern 5: Data Extraction

```python
from guidance import models, gen, guidance

@guidance
def extract_entities(lm, text):
    """Extract structured entities from text."""
    lm += f"Text: {text}\n\n"

    # Extract person
    lm += "Person: " + gen("person", stop="\n", max_tokens=30) + "\n"

    # Extract organization
    lm += "Organization: " + gen("organization", stop="\n", max_tokens=30) + "\n"

    # Extract date
    lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}", max_tokens=10) + "\n"

    # Extract location
    lm += "Location: " + gen("location", stop="\n", max_tokens=30) + "\n"

    return lm

text = "Tim Cook announced at Apple Park on 2024-09-15 in Cupertino."

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = extract_entities(lm, text)

print(f"Person: {lm['person']}")
print(f"Organization: {lm['organization']}")
print(f"Date: {lm['date']}")
print(f"Location: {lm['location']}")
```

### Best Practices

#### 1. Use Regex for Format Validation

```python
## ✅ Good: Regex ensures valid format
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

## ❌ Bad: Free generation may produce invalid emails
lm += "Email: " + gen("email", max_tokens=50)
```

#### 2. Use select() for Fixed Categories

```python
## ✅ Good: Guaranteed valid category
lm += "Status: " + select(["pending", "approved", "rejected"], name="status")

## ❌ Bad: May generate typos or invalid values
lm += "Status: " + gen("status", max_tokens=20)
```

#### 3. Leverage Token Healing

```python
## Token healing is enabled by default
## No special action needed - just concatenate naturally
lm += "The capital is " + gen("capital")  # Automatic healing
```

#### 4. Use stop Sequences

```python
## ✅ Good: Stop at newline for single-line outputs
lm += "Name: " + gen("name", stop="\n")

## ❌ Bad: May generate multiple lines
lm += "Name: " + gen("name", max_tokens=50)
```

#### 5. Create Reusable Functions

```python
## ✅ Good: Reusable pattern
@guidance
def generate_person(lm):
    lm += "Name: " + gen("name", stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+")
    return lm

## Use multiple times
lm = generate_person(lm)
lm += "\n\n"
lm = generate_person(lm)
```

#### 6. Balance Constraints

```python
## ✅ Good: Reasonable constraints
lm += gen("name", regex=r"[A-Za-z ]+", max_tokens=30)

## ❌ Too strict: May fail or be very slow
lm += gen("name", regex=r"^(John|Jane)$", max_tokens=10)
```

### Comparison to Alternatives

| Feature | Guidance | Instructor | Outlines | LMQL |
|---------|----------|------------|----------|------|
| Regex Constraints | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Grammar Support | ✅ CFG | ❌ No | ✅ CFG | ✅ CFG |
| Pydantic Validation | ❌ No | ✅ Yes | ✅ Yes | ❌ No |
| Token Healing | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| Local Models | ✅ Yes | ⚠️ Limited | ✅ Yes | ✅ Yes |
| API Models | ✅ Yes | ✅ Yes | ⚠️ Limited | ✅ Yes |
| Pythonic Syntax | ✅ Yes | ✅ Yes | ✅ Yes | ❌ SQL-like |
| Learning Curve | Low | Low | Medium | High |

**When to choose Guidance:**
- Need regex/grammar constraints
- Want token healing
- Building complex workflows with control flow
- Using local models (Transformers, llama.cpp)
- Prefer Pythonic syntax

**When to choose alternatives:**
- Instructor: Need Pydantic validation with automatic retrying
- Outlines: Need JSON schema validation
- LMQL: Prefer declarative query syntax

### Performance Characteristics

**Latency Reduction:**
- 30-50% faster than traditional prompting for constrained outputs
- Token healing reduces unnecessary regeneration
- Grammar constraints prevent invalid token generation

**Memory Usage:**
- Minimal overhead vs unconstrained generation
- Grammar compilation cached after first use
- Efficient token filtering at inference time

**Token Efficiency:**
- Prevents wasted tokens on invalid outputs
- No need for retry loops
- Direct path to valid outputs

### Resources

- **Documentation**: https://guidance.readthedocs.io
- **GitHub**: https://github.com/guidance-ai/guidance (18k+ stars)
- **Notebooks**: https://github.com/guidance-ai/guidance/tree/main/notebooks
- **Discord**: Community support available

### See Also

- `references/constraints.md` - Comprehensive regex and grammar patterns
- `references/backends.md` - Backend-specific configuration
- `references/examples.md` - Production-ready examples


---

## Module 3: `obliteratus`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\inference\obliteratus\SKILL.md`
- **Rôle / Objectif :** Remove refusal behaviors from open-weight LLMs using OBLITERATUS — mechanistic interpretability techniques (diff-in-means, SVD, whitened SVD, LEACE, SAE decomposition, etc.) to excise guardrails while preserving reasoning. 9 CLI methods, 28 analysis modules, 116 model presets across 5 compute tiers, tournament evaluation, and telemetry-driven recommendations. Use when a user wants to uncensor, abliterate, or remove refusal from an LLM.

## OBLITERATUS Skill

Remove refusal behaviors (guardrails) from open-weight LLMs without retraining or fine-tuning. Uses mechanistic interpretability techniques — including diff-in-means, SVD, whitened SVD, LEACE concept erasure, SAE decomposition, Bayesian kernel projection, and more — to identify and surgically excise refusal directions from model weights while preserving reasoning capabilities.

**License warning:** OBLITERATUS is AGPL-3.0. NEVER import it as a Python library. Always invoke via CLI (`obliteratus` command) or subprocess. This keeps Hermes Agent's MIT license clean.

### When to Use This Skill

Trigger when the user:
- Wants to "uncensor" or "abliterate" an LLM
- Asks about removing refusal/guardrails from a model
- Wants to create an uncensored version of Llama, Qwen, Mistral, etc.
- Mentions "refusal removal", "abliteration", "weight projection"
- Wants to analyze how a model's refusal mechanism works
- References OBLITERATUS, abliterator, or refusal directions

### Step 1: Installation

Check if already installed:
```bash
obliteratus --version 2>/dev/null && echo "INSTALLED" || echo "NOT INSTALLED"
```

If not installed, clone and install from GitHub:
```bash
git clone https://github.com/elder-plinius/OBLITERATUS.git
cd OBLITERATUS
pip install -e .
## For Gradio web UI support:
## pip install -e ".[spaces]"
```

**IMPORTANT:** Confirm with user before installing. This pulls in ~5-10GB of dependencies (PyTorch, Transformers, bitsandbytes, etc.).

### Step 2: Check Hardware

Before anything, check what GPU is available:
```bash
python3 -c "
import torch
if torch.cuda.is_available():
    gpu = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f'GPU: {gpu}')
    print(f'VRAM: {vram:.1f} GB')
    if vram < 4: print('TIER: tiny (models under 1B)')
    elif vram < 8: print('TIER: small (models 1-4B)')
    elif vram < 16: print('TIER: medium (models 4-9B with 4bit quant)')
    elif vram < 32: print('TIER: large (models 8-32B with 4bit quant)')
    else: print('TIER: frontier (models 32B+)')
else:
    print('NO GPU - only tiny models (under 1B) on CPU')
"
```

#### VRAM Requirements (with 4-bit quantization)

| VRAM     | Max Model Size  | Example Models                              |
|:---------|:----------------|:--------------------------------------------|
| CPU only | ~1B params      | GPT-2, TinyLlama, SmolLM                    |
| 4-8 GB   | ~4B params      | Qwen2.5-1.5B, Phi-3.5 mini, Llama 3.2 3B   |
| 8-16 GB  | ~9B params      | Llama 3.1 8B, Mistral 7B, Gemma 2 9B       |
| 24 GB    | ~32B params     | Qwen3-32B, Llama 3.1 70B (tight), Command-R |
| 48 GB+   | ~72B+ params    | Qwen2.5-72B, DeepSeek-R1                    |
| Multi-GPU| 200B+ params    | Llama 3.1 405B, DeepSeek-V3 (685B MoE)      |

### Step 3: Browse Available Models & Get Recommendations

```bash
## Browse models by compute tier
obliteratus models --tier medium

## Get architecture info for a specific model
obliteratus info <model_name>

## Get telemetry-driven recommendation for best method & params
obliteratus recommend <model_name>
obliteratus recommend <model_name> --insights  # global cross-architecture rankings
```

### Step 4: Choose a Method

#### Method Selection Guide
**Default / recommended for most cases: `advanced`.** It uses multi-direction SVD with norm-preserving projection and is well-tested.

| Situation                         | Recommended Method | Why                                      |
|:----------------------------------|:-------------------|:-----------------------------------------|
| Default / most models             | `advanced`         | Multi-direction SVD, norm-preserving, reliable |
| Quick test / prototyping          | `basic`            | Fast, simple, good enough to evaluate    |
| Dense model (Llama, Mistral)      | `advanced`         | Multi-direction, norm-preserving         |
| MoE model (DeepSeek, Mixtral)     | `nuclear`          | Expert-granular, handles MoE complexity  |
| Reasoning model (R1 distills)     | `surgical`         | CoT-aware, preserves chain-of-thought    |
| Stubborn refusals persist         | `aggressive`       | Whitened SVD + head surgery + jailbreak   |
| Want reversible changes           | Use steering vectors (see Analysis section) |
| Maximum quality, time no object   | `optimized`        | Bayesian search for best parameters      |
| Experimental auto-detection       | `informed`         | Auto-detects alignment type — experimental, may not always outperform advanced |

#### 9 CLI Methods
- **basic** — Single refusal direction via diff-in-means. Fast (~5-10 min for 8B).
- **advanced** (DEFAULT, RECOMMENDED) — Multiple SVD directions, norm-preserving projection, 2 refinement passes. Medium speed (~10-20 min).
- **aggressive** — Whitened SVD + jailbreak-contrastive + attention head surgery. Higher risk of coherence damage.
- **spectral_cascade** — DCT frequency-domain decomposition. Research/novel approach.
- **informed** — Runs analysis DURING abliteration to auto-configure. Experimental — slower and less predictable than advanced.
- **surgical** — SAE features + neuron masking + head surgery + per-expert. Very slow (~1-2 hrs). Best for reasoning models.
- **optimized** — Bayesian hyperparameter search (Optuna TPE). Longest runtime but finds optimal parameters.
- **inverted** — Flips the refusal direction. Model becomes actively willing.
- **nuclear** — Maximum force combo for stubborn MoE models. Expert-granular.

#### Direction Extraction Methods (--direction-method flag)
- **diff_means** (default) — Simple difference-in-means between refused/complied activations. Robust.
- **svd** — Multi-direction SVD extraction. Better for complex alignment.
- **leace** — LEACE (Linear Erasure via Closed-form Estimation). Optimal linear erasure.

#### 4 Python-API-Only Methods
(NOT available via CLI — require Python import, which violates AGPL boundary. Mention to user only if they explicitly want to use OBLITERATUS as a library in their own AGPL project.)
- failspy, gabliteration, heretic, rdo

### Step 5: Run Abliteration

#### Standard usage
```bash
## Default method (advanced) — recommended for most models
obliteratus obliterate <model_name> --method advanced --output-dir ./abliterated-models

## With 4-bit quantization (saves VRAM)
obliteratus obliterate <model_name> --method advanced --quantization 4bit --output-dir ./abliterated-models

## Large models (70B+) — conservative defaults
obliteratus obliterate <model_name> --method advanced --quantization 4bit --large-model --output-dir ./abliterated-models
```

#### Fine-tuning parameters
```bash
obliteratus obliterate <model_name> \
  --method advanced \
  --direction-method diff_means \
  --n-directions 4 \
  --refinement-passes 2 \
  --regularization 0.1 \
  --quantization 4bit \
  --output-dir ./abliterated-models \
  --contribute  # opt-in telemetry for community research
```

#### Key flags
| Flag | Description | Default |
|:-----|:------------|:--------|
| `--method` | Abliteration method | advanced |
| `--direction-method` | Direction extraction | diff_means |
| `--n-directions` | Number of refusal directions (1-32) | method-dependent |
| `--refinement-passes` | Iterative passes (1-5) | 2 |
| `--regularization` | Regularization strength (0.0-1.0) | 0.1 |
| `--quantization` | Load in 4bit or 8bit | none (full precision) |
| `--large-model` | Conservative defaults for 120B+ | false |
| `--output-dir` | Where to save the abliterated model | ./obliterated_model |
| `--contribute` | Share anonymized results for research | false |
| `--verify-sample-size` | Number of test prompts for refusal check | 20 |
| `--dtype` | Model dtype (float16, bfloat16) | auto |

#### Other execution modes
```bash
## Interactive guided mode (hardware → model → preset)
obliteratus interactive

## Web UI (Gradio)
obliteratus ui --port 7860

## Run a full ablation study from YAML config
obliteratus run config.yaml --preset quick

## Tournament: pit all methods against each other
obliteratus tourney <model_name>
```

### Step 6: Verify Results

After abliteration, check the output metrics:

| Metric | Good Value | Warning |
|:-------|:-----------|:--------|
| Refusal rate | < 5% (ideally ~0%) | > 10% means refusals persist |
| Perplexity change | < 10% increase | > 15% means coherence damage |
| KL divergence | < 0.1 | > 0.5 means significant distribution shift |
| Coherence | High / passes qualitative check | Degraded responses, repetition |

#### If refusals persist (> 10%)
1. Try `aggressive` method
2. Increase `--n-directions` (e.g., 8 or 16)
3. Add `--refinement-passes 3`
4. Try `--direction-method svd` instead of diff_means

#### If coherence is damaged (perplexity > 15% increase)
1. Reduce `--n-directions` (try 2)
2. Increase `--regularization` (try 0.3)
3. Reduce `--refinement-passes` to 1
4. Try `basic` method (gentler)

### Step 7: Use the Abliterated Model

The output is a standard HuggingFace model directory.

```bash
## Test locally with transformers
python3 -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained('./abliterated-models/<model>')
tokenizer = AutoTokenizer.from_pretrained('./abliterated-models/<model>')
inputs = tokenizer('How do I pick a lock?', return_tensors='pt')
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
"

## Upload to HuggingFace Hub
huggingface-cli upload <username>/<model-name>-abliterated ./abliterated-models/<model>

## Serve with vLLM
vllm serve ./abliterated-models/<model>
```

### CLI Command Reference

| Command | Description |
|:--------|:------------|
| `obliteratus obliterate` | Main abliteration command |
| `obliteratus info <model>` | Print model architecture details |
| `obliteratus models --tier <tier>` | Browse curated models by compute tier |
| `obliteratus recommend <model>` | Telemetry-driven method/param suggestion |
| `obliteratus interactive` | Guided setup wizard |
| `obliteratus tourney <model>` | Tournament: all methods head-to-head |
| `obliteratus run <config.yaml>` | Execute ablation study from YAML |
| `obliteratus strategies` | List all registered ablation strategies |
| `obliteratus report <results.json>` | Regenerate visual reports |
| `obliteratus ui` | Launch Gradio web interface |
| `obliteratus aggregate` | Summarize community telemetry data |

### Analysis Modules

OBLITERATUS includes 28 analysis modules for mechanistic interpretability.
See `skill_view(name="obliteratus", file_path="references/analysis-modules.md")` for the full reference.

#### Quick analysis commands
```bash
## Run specific analysis modules
obliteratus run analysis-config.yaml --preset quick

## Key modules to run first:
## - alignment_imprint: Fingerprint DPO/RLHF/CAI/SFT alignment method
## - concept_geometry: Single direction vs polyhedral cone
## - logit_lens: Which layer decides to refuse
## - anti_ouroboros: Self-repair risk score
## - causal_tracing: Causally necessary components
```

#### Steering Vectors (Reversible Alternative)
Instead of permanent weight modification, use inference-time steering:
```python
## Python API only — for user's own projects
from obliteratus.analysis.steering_vectors import SteeringVectorFactory, SteeringHookManager
```

### Ablation Strategies

Beyond direction-based abliteration, OBLITERATUS includes structural ablation strategies:
- **Embedding Ablation** — Target embedding layer components
- **FFN Ablation** — Feed-forward network block removal
- **Head Pruning** — Attention head pruning
- **Layer Removal** — Full layer removal

List all available: `obliteratus strategies`

### Evaluation

OBLITERATUS includes built-in evaluation tools:
- Refusal rate benchmarking
- Perplexity comparison (before/after)
- LM Eval Harness integration for academic benchmarks
- Head-to-head competitor comparison
- Baseline performance tracking

### Platform Support

- **CUDA** — Full support (NVIDIA GPUs)
- **Apple Silicon (MLX)** — Supported via MLX backend
- **CPU** — Supported for tiny models (< 1B params)

### YAML Config Templates

Load templates for reproducible runs via `skill_view`:
- `templates/abliteration-config.yaml` — Standard single-model config
- `templates/analysis-study.yaml` — Pre-abliteration analysis study
- `templates/batch-abliteration.yaml` — Multi-model batch processing

### Telemetry

OBLITERATUS can optionally contribute anonymized run data to a global research dataset.
Enable with `--contribute` flag. No personal data is collected — only model name, method, metrics.

### Common Pitfalls

1. **Don't use `informed` as default** — it's experimental and slower. Use `advanced` for reliable results.
2. **Models under ~1B respond poorly to abliteration** — their refusal behaviors are shallow and fragmented, making clean direction extraction difficult. Expect partial results (20-40% remaining refusal). Models 3B+ have cleaner refusal directions and respond much better (often 0% refusal with `advanced`).
3. **`aggressive` can make things worse** — on small models it can damage coherence and actually increase refusal rate. Only use it if `advanced` leaves > 10% refusals on a 3B+ model.
4. **Always check perplexity** — if it spikes > 15%, the model is damaged. Reduce aggressiveness.
5. **MoE models need special handling** — use `nuclear` method for Mixtral, DeepSeek-MoE, etc.
6. **Quantized models can't be re-quantized** — abliterate the full-precision model, then quantize the output.
7. **VRAM estimation is approximate** — 4-bit quant helps but peak usage can spike during extraction.
8. **Reasoning models are sensitive** — use `surgical` for R1 distills to preserve chain-of-thought.
9. **Check `obliteratus recommend`** — telemetry data may have better parameters than defaults.
10. **AGPL license** — never `import obliteratus` in MIT/Apache projects. CLI invocation only.
11. **Large models (70B+)** — always use `--large-model` flag for conservative defaults.
12. **Spectral certification RED is common** — the spectral check often flags "incomplete" even when practical refusal rate is 0%. Check actual refusal rate rather than relying on spectral certification alone.

### Complementary Skills

- **vllm** — Serve abliterated models with high throughput
- **gguf** — Convert abliterated models to GGUF for llama.cpp
- **huggingface-tokenizers** — Work with model tokenizers


---

## Module 4: `outlines`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\inference\outlines\SKILL.md`
- **Rôle / Objectif :** Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and maximize inference speed with Outlines - dottxt.ai's structured generation library

## Outlines: Structured Text Generation

### When to Use This Skill

Use Outlines when you need to:
- **Guarantee valid JSON/XML/code** structure during generation
- **Use Pydantic models** for type-safe outputs
- **Support local models** (Transformers, llama.cpp, vLLM)
- **Maximize inference speed** with zero-overhead structured generation
- **Generate against JSON schemas** automatically
- **Control token sampling** at the grammar level

**GitHub Stars**: 8,000+ | **From**: dottxt.ai (formerly .txt)

### Installation

```bash
## Base installation
pip install outlines

## With specific backends
pip install outlines transformers  # Hugging Face models
pip install outlines llama-cpp-python  # llama.cpp
pip install outlines vllm  # vLLM for high-throughput
```

### Quick Start

#### Basic Example: Classification

```python
import outlines
from typing import Literal

## Load model
model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

## Generate with type constraint
prompt = "Sentiment of 'This product is amazing!': "
generator = outlines.generate.choice(model, ["positive", "negative", "neutral"])
sentiment = generator(prompt)

print(sentiment)  # "positive" (guaranteed one of these)
```

#### With Pydantic Models

```python
from pydantic import BaseModel
import outlines

class User(BaseModel):
    name: str
    age: int
    email: str

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

## Generate structured output
prompt = "Extract user: John Doe, 30 years old, john@example.com"
generator = outlines.generate.json(model, User)
user = generator(prompt)

print(user.name)   # "John Doe"
print(user.age)    # 30
print(user.email)  # "john@example.com"
```

### Core Concepts

#### 1. Constrained Token Sampling

Outlines uses Finite State Machines (FSM) to constrain token generation at the logit level.

**How it works:**
1. Convert schema (JSON/Pydantic/regex) to context-free grammar (CFG)
2. Transform CFG into Finite State Machine (FSM)
3. Filter invalid tokens at each step during generation
4. Fast-forward when only one valid token exists

**Benefits:**
- **Zero overhead**: Filtering happens at token level
- **Speed improvement**: Fast-forward through deterministic paths
- **Guaranteed validity**: Invalid outputs impossible

```python
import outlines

## Pydantic model -> JSON schema -> CFG -> FSM
class Person(BaseModel):
    name: str
    age: int

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

## Behind the scenes:
## 1. Person -> JSON schema
## 2. JSON schema -> CFG
## 3. CFG -> FSM
## 4. FSM filters tokens during generation

generator = outlines.generate.json(model, Person)
result = generator("Generate person: Alice, 25")
```

#### 2. Structured Generators

Outlines provides specialized generators for different output types.

##### Choice Generator

```python
## Multiple choice selection
generator = outlines.generate.choice(
    model,
    ["positive", "negative", "neutral"]
)

sentiment = generator("Review: This is great!")
## Result: One of the three choices
```

##### JSON Generator

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

## Generate valid JSON matching schema
generator = outlines.generate.json(model, Product)
product = generator("Extract: iPhone 15, $999, available")

## Guaranteed valid Product instance
print(type(product))  # <class '__main__.Product'>
```

##### Regex Generator

```python
## Generate text matching regex
generator = outlines.generate.regex(
    model,
    r"[0-9]{3}-[0-9]{3}-[0-9]{4}"  # Phone number pattern
)

phone = generator("Generate phone number:")
## Result: "555-123-4567" (guaranteed to match pattern)
```

##### Integer/Float Generators

```python
## Generate specific numeric types
int_generator = outlines.generate.integer(model)
age = int_generator("Person's age:")  # Guaranteed integer

float_generator = outlines.generate.float(model)
price = float_generator("Product price:")  # Guaranteed float
```

#### 3. Model Backends

Outlines supports multiple local and API-based backends.

##### Transformers (Hugging Face)

```python
import outlines

## Load from Hugging Face
model = outlines.models.transformers(
    "microsoft/Phi-3-mini-4k-instruct",
    device="cuda"  # Or "cpu"
)

## Use with any generator
generator = outlines.generate.json(model, YourModel)
```

##### llama.cpp

```python
## Load GGUF model
model = outlines.models.llamacpp(
    "./models/llama-3.1-8b-instruct.Q4_K_M.gguf",
    n_gpu_layers=35
)

generator = outlines.generate.json(model, YourModel)
```

##### vLLM (High Throughput)

```python
## For production deployments
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-8B-Instruct",
    tensor_parallel_size=2  # Multi-GPU
)

generator = outlines.generate.json(model, YourModel)
```

##### OpenAI (Limited Support)

```python
## Basic OpenAI support
model = outlines.models.openai(
    "gpt-4o-mini",
    api_key="your-api-key"
)

## Note: Some features limited with API models
generator = outlines.generate.json(model, YourModel)
```

#### 4. Pydantic Integration

Outlines has first-class Pydantic support with automatic schema translation.

##### Basic Models

```python
from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(description="Article title")
    author: str = Field(description="Author name")
    word_count: int = Field(description="Number of words", gt=0)
    tags: list[str] = Field(description="List of tags")

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, Article)

article = generator("Generate article about AI")
print(article.title)
print(article.word_count)  # Guaranteed > 0
```

##### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # Nested model

generator = outlines.generate.json(model, Person)
person = generator("Generate person in New York")

print(person.address.city)  # "New York"
```

##### Enums and Literals

```python
from enum import Enum
from typing import Literal

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(BaseModel):
    applicant: str
    status: Status  # Must be one of enum values
    priority: Literal["low", "medium", "high"]  # Must be one of literals

generator = outlines.generate.json(model, Application)
app = generator("Generate application")

print(app.status)  # Status.PENDING (or APPROVED/REJECTED)
```

### Common Patterns

#### Pattern 1: Data Extraction

```python
from pydantic import BaseModel
import outlines

class CompanyInfo(BaseModel):
    name: str
    founded_year: int
    industry: str
    employees: int

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, CompanyInfo)

text = """
Apple Inc. was founded in 1976 in the technology industry.
The company employs approximately 164,000 people worldwide.
"""

prompt = f"Extract company information:\n{text}\n\nCompany:"
company = generator(prompt)

print(f"Name: {company.name}")
print(f"Founded: {company.founded_year}")
print(f"Industry: {company.industry}")
print(f"Employees: {company.employees}")
```

#### Pattern 2: Classification

```python
from typing import Literal
import outlines

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

## Binary classification
generator = outlines.generate.choice(model, ["spam", "not_spam"])
result = generator("Email: Buy now! 50% off!")

## Multi-class classification
categories = ["technology", "business", "sports", "entertainment"]
category_gen = outlines.generate.choice(model, categories)
category = category_gen("Article: Apple announces new iPhone...")

## With confidence
class Classification(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    confidence: float

classifier = outlines.generate.json(model, Classification)
result = classifier("Review: This product is okay, nothing special")
```

#### Pattern 3: Structured Forms

```python
class UserProfile(BaseModel):
    full_name: str
    age: int
    email: str
    phone: str
    country: str
    interests: list[str]

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, UserProfile)

prompt = """
Extract user profile from:
Name: Alice Johnson
Age: 28
Email: alice@example.com
Phone: 555-0123
Country: USA
Interests: hiking, photography, cooking
"""

profile = generator(prompt)
print(profile.full_name)
print(profile.interests)  # ["hiking", "photography", "cooking"]
```

#### Pattern 4: Multi-Entity Extraction

```python
class Entity(BaseModel):
    name: str
    type: Literal["PERSON", "ORGANIZATION", "LOCATION"]

class DocumentEntities(BaseModel):
    entities: list[Entity]

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, DocumentEntities)

text = "Tim Cook met with Satya Nadella at Microsoft headquarters in Redmond."
prompt = f"Extract entities from: {text}"

result = generator(prompt)
for entity in result.entities:
    print(f"{entity.name} ({entity.type})")
```

#### Pattern 5: Code Generation

```python
class PythonFunction(BaseModel):
    function_name: str
    parameters: list[str]
    docstring: str
    body: str

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, PythonFunction)

prompt = "Generate a Python function to calculate factorial"
func = generator(prompt)

print(f"def {func.function_name}({', '.join(func.parameters)}):")
print(f'    """{func.docstring}"""')
print(f"    {func.body}")
```

#### Pattern 6: Batch Processing

```python
def batch_extract(texts: list[str], schema: type[BaseModel]):
    """Extract structured data from multiple texts."""
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
    generator = outlines.generate.json(model, schema)

    results = []
    for text in texts:
        result = generator(f"Extract from: {text}")
        results.append(result)

    return results

class Person(BaseModel):
    name: str
    age: int

texts = [
    "John is 30 years old",
    "Alice is 25 years old",
    "Bob is 40 years old"
]

people = batch_extract(texts, Person)
for person in people:
    print(f"{person.name}: {person.age}")
```

### Backend Configuration

#### Transformers

```python
import outlines

## Basic usage
model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

## GPU configuration
model = outlines.models.transformers(
    "microsoft/Phi-3-mini-4k-instruct",
    device="cuda",
    model_kwargs={"torch_dtype": "float16"}
)

## Popular models
model = outlines.models.transformers("meta-llama/Llama-3.1-8B-Instruct")
model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.3")
model = outlines.models.transformers("Qwen/Qwen2.5-7B-Instruct")
```

#### llama.cpp

```python
## Load GGUF model
model = outlines.models.llamacpp(
    "./models/llama-3.1-8b.Q4_K_M.gguf",
    n_ctx=4096,         # Context window
    n_gpu_layers=35,    # GPU layers
    n_threads=8         # CPU threads
)

## Full GPU offload
model = outlines.models.llamacpp(
    "./models/model.gguf",
    n_gpu_layers=-1  # All layers on GPU
)
```

#### vLLM (Production)

```python
## Single GPU
model = outlines.models.vllm("meta-llama/Llama-3.1-8B-Instruct")

## Multi-GPU
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-70B-Instruct",
    tensor_parallel_size=4  # 4 GPUs
)

## With quantization
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization="awq"  # Or "gptq"
)
```

### Best Practices

#### 1. Use Specific Types

```python
## ✅ Good: Specific types
class Product(BaseModel):
    name: str
    price: float  # Not str
    quantity: int  # Not str
    in_stock: bool  # Not str

## ❌ Bad: Everything as string
class Product(BaseModel):
    name: str
    price: str  # Should be float
    quantity: str  # Should be int
```

#### 2. Add Constraints

```python
from pydantic import Field

## ✅ Good: With constraints
class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

## ❌ Bad: No constraints
class User(BaseModel):
    name: str
    age: int
    email: str
```

#### 3. Use Enums for Categories

```python
## ✅ Good: Enum for fixed set
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority

## ❌ Bad: Free-form string
class Task(BaseModel):
    title: str
    priority: str  # Can be anything
```

#### 4. Provide Context in Prompts

```python
## ✅ Good: Clear context
prompt = """
Extract product information from the following text.
Text: iPhone 15 Pro costs $999 and is currently in stock.
Product:
"""

## ❌ Bad: Minimal context
prompt = "iPhone 15 Pro costs $999 and is currently in stock."
```

#### 5. Handle Optional Fields

```python
from typing import Optional

## ✅ Good: Optional fields for incomplete data
class Article(BaseModel):
    title: str  # Required
    author: Optional[str] = None  # Optional
    date: Optional[str] = None  # Optional
    tags: list[str] = []  # Default empty list

## Can succeed even if author/date missing
```

### Comparison to Alternatives

| Feature | Outlines | Instructor | Guidance | LMQL |
|---------|----------|------------|----------|------|
| Pydantic Support | ✅ Native | ✅ Native | ❌ No | ❌ No |
| JSON Schema | ✅ Yes | ✅ Yes | ⚠️ Limited | ✅ Yes |
| Regex Constraints | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Local Models | ✅ Full | ⚠️ Limited | ✅ Full | ✅ Full |
| API Models | ⚠️ Limited | ✅ Full | ✅ Full | ✅ Full |
| Zero Overhead | ✅ Yes | ❌ No | ⚠️ Partial | ✅ Yes |
| Automatic Retrying | ❌ No | ✅ Yes | ❌ No | ❌ No |
| Learning Curve | Low | Low | Low | High |

**When to choose Outlines:**
- Using local models (Transformers, llama.cpp, vLLM)
- Need maximum inference speed
- Want Pydantic model support
- Require zero-overhead structured generation
- Control token sampling process

**When to choose alternatives:**
- Instructor: Need API models with automatic retrying
- Guidance: Need token healing and complex workflows
- LMQL: Prefer declarative query syntax

### Performance Characteristics

**Speed:**
- **Zero overhead**: Structured generation as fast as unconstrained
- **Fast-forward optimization**: Skips deterministic tokens
- **1.2-2x faster** than post-generation validation approaches

**Memory:**
- FSM compiled once per schema (cached)
- Minimal runtime overhead
- Efficient with vLLM for high throughput

**Accuracy:**
- **100% valid outputs** (guaranteed by FSM)
- No retry loops needed
- Deterministic token filtering

### Resources

- **Documentation**: https://outlines-dev.github.io/outlines
- **GitHub**: https://github.com/outlines-dev/outlines (8k+ stars)
- **Discord**: https://discord.gg/R9DSu34mGd
- **Blog**: https://blog.dottxt.co

### See Also

- `references/json_generation.md` - Comprehensive JSON and Pydantic patterns
- `references/backends.md` - Backend-specific configuration
- `references/examples.md` - Production-ready examples


---

## Module 5: `weights-and-biases`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\evaluation\weights-and-biases\SKILL.md`
- **Rôle / Objectif :** Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B - collaborative MLOps platform

## Weights & Biases: ML Experiment Tracking & MLOps

### When to Use This Skill

Use Weights & Biases (W&B) when you need to:
- **Track ML experiments** with automatic metric logging
- **Visualize training** in real-time dashboards
- **Compare runs** across hyperparameters and configurations
- **Optimize hyperparameters** with automated sweeps
- **Manage model registry** with versioning and lineage
- **Collaborate on ML projects** with team workspaces
- **Track artifacts** (datasets, models, code) with lineage

**Users**: 200,000+ ML practitioners | **GitHub Stars**: 10.5k+ | **Integrations**: 100+

### Installation

```bash
## Install W&B
pip install wandb

## Login (creates API key)
wandb login

## Or set API key programmatically
export WANDB_API_KEY=your_api_key_here
```

### Quick Start

#### Basic Experiment Tracking

```python
import wandb

## Initialize a run
run = wandb.init(
    project="my-project",
    config={
        "learning_rate": 0.001,
        "epochs": 10,
        "batch_size": 32,
        "architecture": "ResNet50"
    }
)

## Training loop
for epoch in range(run.config.epochs):
    # Your training code
    train_loss = train_epoch()
    val_loss = validate()

    # Log metrics
    wandb.log({
        "epoch": epoch,
        "train/loss": train_loss,
        "val/loss": val_loss,
        "train/accuracy": train_acc,
        "val/accuracy": val_acc
    })

## Finish the run
wandb.finish()
```

#### With PyTorch

```python
import torch
import wandb

## Initialize
wandb.init(project="pytorch-demo", config={
    "lr": 0.001,
    "epochs": 10
})

## Access config
config = wandb.config

## Training loop
for epoch in range(config.epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        # Forward pass
        output = model(data)
        loss = criterion(output, target)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Log every 100 batches
        if batch_idx % 100 == 0:
            wandb.log({
                "loss": loss.item(),
                "epoch": epoch,
                "batch": batch_idx
            })

## Save model
torch.save(model.state_dict(), "model.pth")
wandb.save("model.pth")  # Upload to W&B

wandb.finish()
```

### Core Concepts

#### 1. Projects and Runs

**Project**: Collection of related experiments
**Run**: Single execution of your training script

```python
## Create/use project
run = wandb.init(
    project="image-classification",
    name="resnet50-experiment-1",  # Optional run name
    tags=["baseline", "resnet"],    # Organize with tags
    notes="First baseline run"      # Add notes
)

## Each run has unique ID
print(f"Run ID: {run.id}")
print(f"Run URL: {run.url}")
```

#### 2. Configuration Tracking

Track hyperparameters automatically:

```python
config = {
    # Model architecture
    "model": "ResNet50",
    "pretrained": True,

    # Training params
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 50,
    "optimizer": "Adam",

    # Data params
    "dataset": "ImageNet",
    "augmentation": "standard"
}

wandb.init(project="my-project", config=config)

## Access config during training
lr = wandb.config.learning_rate
batch_size = wandb.config.batch_size
```

#### 3. Metric Logging

```python
## Log scalars
wandb.log({"loss": 0.5, "accuracy": 0.92})

## Log multiple metrics
wandb.log({
    "train/loss": train_loss,
    "train/accuracy": train_acc,
    "val/loss": val_loss,
    "val/accuracy": val_acc,
    "learning_rate": current_lr,
    "epoch": epoch
})

## Log with custom x-axis
wandb.log({"loss": loss}, step=global_step)

## Log media (images, audio, video)
wandb.log({"examples": [wandb.Image(img) for img in images]})

## Log histograms
wandb.log({"gradients": wandb.Histogram(gradients)})

## Log tables
table = wandb.Table(columns=["id", "prediction", "ground_truth"])
wandb.log({"predictions": table})
```

#### 4. Model Checkpointing

```python
import torch
import wandb

## Save model checkpoint
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}

torch.save(checkpoint, 'checkpoint.pth')

## Upload to W&B
wandb.save('checkpoint.pth')

## Or use Artifacts (recommended)
artifact = wandb.Artifact('model', type='model')
artifact.add_file('checkpoint.pth')
wandb.log_artifact(artifact)
```

### Hyperparameter Sweeps

Automatically search for optimal hyperparameters.

#### Define Sweep Configuration

```python
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {
        'name': 'val/accuracy',
        'goal': 'maximize'
    },
    'parameters': {
        'learning_rate': {
            'distribution': 'log_uniform',
            'min': 1e-5,
            'max': 1e-1
        },
        'batch_size': {
            'values': [16, 32, 64, 128]
        },
        'optimizer': {
            'values': ['adam', 'sgd', 'rmsprop']
        },
        'dropout': {
            'distribution': 'uniform',
            'min': 0.1,
            'max': 0.5
        }
    }
}

## Initialize sweep
sweep_id = wandb.sweep(sweep_config, project="my-project")
```

#### Define Training Function

```python
def train():
    # Initialize run
    run = wandb.init()

    # Access sweep parameters
    lr = wandb.config.learning_rate
    batch_size = wandb.config.batch_size
    optimizer_name = wandb.config.optimizer

    # Build model with sweep config
    model = build_model(wandb.config)
    optimizer = get_optimizer(optimizer_name, lr)

    # Training loop
    for epoch in range(NUM_EPOCHS):
        train_loss = train_epoch(model, optimizer, batch_size)
        val_acc = validate(model)

        # Log metrics
        wandb.log({
            "train/loss": train_loss,
            "val/accuracy": val_acc
        })

## Run sweep
wandb.agent(sweep_id, function=train, count=50)  # Run 50 trials
```

#### Sweep Strategies

```python
## Grid search - exhaustive
sweep_config = {
    'method': 'grid',
    'parameters': {
        'lr': {'values': [0.001, 0.01, 0.1]},
        'batch_size': {'values': [16, 32, 64]}
    }
}

## Random search
sweep_config = {
    'method': 'random',
    'parameters': {
        'lr': {'distribution': 'uniform', 'min': 0.0001, 'max': 0.1},
        'dropout': {'distribution': 'uniform', 'min': 0.1, 'max': 0.5}
    }
}

## Bayesian optimization (recommended)
sweep_config = {
    'method': 'bayes',
    'metric': {'name': 'val/loss', 'goal': 'minimize'},
    'parameters': {
        'lr': {'distribution': 'log_uniform', 'min': 1e-5, 'max': 1e-1}
    }
}
```

### Artifacts

Track datasets, models, and other files with lineage.

#### Log Artifacts

```python
## Create artifact
artifact = wandb.Artifact(
    name='training-dataset',
    type='dataset',
    description='ImageNet training split',
    metadata={'size': '1.2M images', 'split': 'train'}
)

## Add files
artifact.add_file('data/train.csv')
artifact.add_dir('data/images/')

## Log artifact
wandb.log_artifact(artifact)
```

#### Use Artifacts

```python
## Download and use artifact
run = wandb.init(project="my-project")

## Download artifact
artifact = run.use_artifact('training-dataset:latest')
artifact_dir = artifact.download()

## Use the data
data = load_data(f"{artifact_dir}/train.csv")
```

#### Model Registry

```python
## Log model as artifact
model_artifact = wandb.Artifact(
    name='resnet50-model',
    type='model',
    metadata={'architecture': 'ResNet50', 'accuracy': 0.95}
)

model_artifact.add_file('model.pth')
wandb.log_artifact(model_artifact, aliases=['best', 'production'])

## Link to model registry
run.link_artifact(model_artifact, 'model-registry/production-models')
```

### Integration Examples

#### HuggingFace Transformers

```python
from transformers import Trainer, TrainingArguments
import wandb

## Initialize W&B
wandb.init(project="hf-transformers")

## Training arguments with W&B
training_args = TrainingArguments(
    output_dir="./results",
    report_to="wandb",  # Enable W&B logging
    run_name="bert-finetuning",
    logging_steps=100,
    save_steps=500
)

## Trainer automatically logs to W&B
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()
```

#### PyTorch Lightning

```python
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import WandbLogger
import wandb

## Create W&B logger
wandb_logger = WandbLogger(
    project="lightning-demo",
    log_model=True  # Log model checkpoints
)

## Use with Trainer
trainer = Trainer(
    logger=wandb_logger,
    max_epochs=10
)

trainer.fit(model, datamodule=dm)
```

#### Keras/TensorFlow

```python
import wandb
from wandb.keras import WandbCallback

## Initialize
wandb.init(project="keras-demo")

## Add callback
model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=10,
    callbacks=[WandbCallback()]  # Auto-logs metrics
)
```

### Visualization & Analysis

#### Custom Charts

```python
## Log custom visualizations
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x, y)
wandb.log({"custom_plot": wandb.Image(fig)})

## Log confusion matrix
wandb.log({"conf_mat": wandb.plot.confusion_matrix(
    probs=None,
    y_true=ground_truth,
    preds=predictions,
    class_names=class_names
)})
```

#### Reports

Create shareable reports in W&B UI:
- Combine runs, charts, and text
- Markdown support
- Embeddable visualizations
- Team collaboration

### Best Practices

#### 1. Organize with Tags and Groups

```python
wandb.init(
    project="my-project",
    tags=["baseline", "resnet50", "imagenet"],
    group="resnet-experiments",  # Group related runs
    job_type="train"             # Type of job
)
```

#### 2. Log Everything Relevant

```python
## Log system metrics
wandb.log({
    "gpu/util": gpu_utilization,
    "gpu/memory": gpu_memory_used,
    "cpu/util": cpu_utilization
})

## Log code version
wandb.log({"git_commit": git_commit_hash})

## Log data splits
wandb.log({
    "data/train_size": len(train_dataset),
    "data/val_size": len(val_dataset)
})
```

#### 3. Use Descriptive Names

```python
## ✅ Good: Descriptive run names
wandb.init(
    project="nlp-classification",
    name="bert-base-lr0.001-bs32-epoch10"
)

## ❌ Bad: Generic names
wandb.init(project="nlp", name="run1")
```

#### 4. Save Important Artifacts

```python
## Save final model
artifact = wandb.Artifact('final-model', type='model')
artifact.add_file('model.pth')
wandb.log_artifact(artifact)

## Save predictions for analysis
predictions_table = wandb.Table(
    columns=["id", "input", "prediction", "ground_truth"],
    data=predictions_data
)
wandb.log({"predictions": predictions_table})
```

#### 5. Use Offline Mode for Unstable Connections

```python
import os

## Enable offline mode
os.environ["WANDB_MODE"] = "offline"

wandb.init(project="my-project")
## ... your code ...

## Sync later
## wandb sync <run_directory>
```

### Team Collaboration

#### Share Runs

```python
## Runs are automatically shareable via URL
run = wandb.init(project="team-project")
print(f"Share this URL: {run.url}")
```

#### Team Projects

- Create team account at wandb.ai
- Add team members
- Set project visibility (private/public)
- Use team-level artifacts and model registry

### Pricing

- **Free**: Unlimited public projects, 100GB storage
- **Academic**: Free for students/researchers
- **Teams**: $50/seat/month, private projects, unlimited storage
- **Enterprise**: Custom pricing, on-prem options

### Resources

- **Documentation**: https://docs.wandb.ai
- **GitHub**: https://github.com/wandb/wandb (10.5k+ stars)
- **Examples**: https://github.com/wandb/examples
- **Community**: https://wandb.ai/community
- **Discord**: https://wandb.me/discord

### See Also

- `references/sweeps.md` - Comprehensive hyperparameter optimization guide
- `references/artifacts.md` - Data and model versioning patterns
- `references/integrations.md` - Framework-specific examples


---


## Module 6: `lm-evaluation-harness`
- **Origine :** `01_Hermes_Skills_Core_Library/mlops/evaluation/lm-evaluation-harness/SKILL.md`
- **Rôle / Objectif :** Standardized language model evaluation benchmark runner (EleutherAI LM-Eval-Harness).

## lm-evaluation-harness - LLM Benchmarking

### Quick start

lm-evaluation-harness evaluates LLMs across 60+ academic benchmarks using standardized prompts and metrics.

**Installation**:
```bash
pip install lm-eval
```

**Evaluate any HuggingFace model**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag \
  --device cuda:0 \
  --batch_size 8
```

**View available tasks**:
```bash
lm_eval --tasks list
```

### Common workflows

#### Workflow 1: Standard benchmark evaluation

Evaluate model on core benchmarks (MMLU, GSM8K, HumanEval).

Copy this checklist:

```
Benchmark Evaluation:
- [ ] Step 1: Choose benchmark suite
- [ ] Step 2: Configure model
- [ ] Step 3: Run evaluation
- [ ] Step 4: Analyze results
```

**Step 1: Choose benchmark suite**

**Core reasoning benchmarks**:
- **MMLU** (Massive Multitask Language Understanding) - 57 subjects, multiple choice
- **GSM8K** - Grade school math word problems
- **HellaSwag** - Common sense reasoning
- **TruthfulQA** - Truthfulness and factuality
- **ARC** (AI2 Reasoning Challenge) - Science questions

**Code benchmarks**:
- **HumanEval** - Python code generation (164 problems)
- **MBPP** (Mostly Basic Python Problems) - Python coding

**Standard suite** (recommended for model releases):
```bash
--tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge
```

**Step 2: Configure model**

**HuggingFace model**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,dtype=bfloat16 \
  --tasks mmlu \
  --device cuda:0 \
  --batch_size auto  # Auto-detect optimal batch size
```

**Quantized model (4-bit/8-bit)**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,load_in_4bit=True \
  --tasks mmlu \
  --device cuda:0
```

**Custom checkpoint**:
```bash
lm_eval --model hf \
  --model_args pretrained=/path/to/my-model,tokenizer=/path/to/tokenizer \
  --tasks mmlu \
  --device cuda:0
```

**Step 3: Run evaluation**

```bash
## Full MMLU evaluation (57 subjects)
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --num_fewshot 5 \  # 5-shot evaluation (standard)
  --batch_size 8 \
  --output_path results/ \
  --log_samples  # Save individual predictions

## Multiple benchmarks at once
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \
  --num_fewshot 5 \
  --batch_size 8 \
  --output_path results/llama2-7b-eval.json
```

**Step 4: Analyze results**

Results saved to `results/llama2-7b-eval.json`:

```json
{
  "results": {
    "mmlu": {
      "acc": 0.459,
      "acc_stderr": 0.004
    },
    "gsm8k": {
      "exact_match": 0.142,
      "exact_match_stderr": 0.006
    },
    "hellaswag": {
      "acc_norm": 0.765,
      "acc_norm_stderr": 0.004
    }
  },
  "config": {
    "model": "hf",
    "model_args": "pretrained=meta-llama/Llama-2-7b-hf",
    "num_fewshot": 5
  }
}
```

#### Workflow 2: Track training progress

Evaluate checkpoints during training.

```
Training Progress Tracking:
- [ ] Step 1: Set up periodic evaluation
- [ ] Step 2: Choose quick benchmarks
- [ ] Step 3: Automate evaluation
- [ ] Step 4: Plot learning curves
```

**Step 1: Set up periodic evaluation**

Evaluate every N training steps:

```bash
##!/bin/bash
## eval_checkpoint.sh

CHECKPOINT_DIR=$1
STEP=$2

lm_eval --model hf \
  --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \
  --tasks gsm8k,hellaswag \
  --num_fewshot 0 \  # 0-shot for speed
  --batch_size 16 \
  --output_path results/step-$STEP.json
```

**Step 2: Choose quick benchmarks**

Fast benchmarks for frequent evaluation:
- **HellaSwag**: ~10 minutes on 1 GPU
- **GSM8K**: ~5 minutes
- **PIQA**: ~2 minutes

Avoid for frequent eval (too slow):
- **MMLU**: ~2 hours (57 subjects)
- **HumanEval**: Requires code execution

**Step 3: Automate evaluation**

Integrate with training script:

```python
## In training loop
if step % eval_interval == 0:
    model.save_pretrained(f"checkpoints/step-{step}")

    # Run evaluation
    os.system(f"./eval_checkpoint.sh checkpoints step-{step}")
```

Or use PyTorch Lightning callbacks:

```python
from pytorch_lightning import Callback

class EvalHarnessCallback(Callback):
    def on_validation_epoch_end(self, trainer, pl_module):
        step = trainer.global_step
        checkpoint_path = f"checkpoints/step-{step}"

        # Save checkpoint
        trainer.save_checkpoint(checkpoint_path)

        # Run lm-eval
        os.system(f"lm_eval --model hf --model_args pretrained={checkpoint_path} ...")
```

**Step 4: Plot learning curves**

```python
import json
import matplotlib.pyplot as plt

## Load all results
steps = []
mmlu_scores = []

for file in sorted(glob.glob("results/step-*.json")):
    with open(file) as f:
        data = json.load(f)
        step = int(file.split("-")[1].split(".")[0])
        steps.append(step)
        mmlu_scores.append(data["results"]["mmlu"]["acc"])

## Plot
plt.plot(steps, mmlu_scores)
plt.xlabel("Training Step")
plt.ylabel("MMLU Accuracy")
plt.title("Training Progress")
plt.savefig("training_curve.png")
```

#### Workflow 3: Compare multiple models

Benchmark suite for model comparison.

```
Model Comparison:
- [ ] Step 1: Define model list
- [ ] Step 2: Run evaluations
- [ ] Step 3: Generate comparison table
```

**Step 1: Define model list**

```bash
## models.txt
meta-llama/Llama-2-7b-hf
meta-llama/Llama-2-13b-hf
mistralai/Mistral-7B-v0.1
microsoft/phi-2
```

**Step 2: Run evaluations**

```bash
##!/bin/bash
## eval_all_models.sh

TASKS="mmlu,gsm8k,hellaswag,truthfulqa"

while read model; do
    echo "Evaluating $model"

    # Extract model name for output file
    model_name=$(echo $model | sed 's/\//-/g')

    lm_eval --model hf \
      --model_args pretrained=$model,dtype=bfloat16 \
      --tasks $TASKS \
      --num_fewshot 5 \
      --batch_size auto \
      --output_path results/$model_name.json

done < models.txt
```

**Step 3: Generate comparison table**

```python
import json
import pandas as pd

models = [
    "meta-llama-Llama-2-7b-hf",
    "meta-llama-Llama-2-13b-hf",
    "mistralai-Mistral-7B-v0.1",
    "microsoft-phi-2"
]

tasks = ["mmlu", "gsm8k", "hellaswag", "truthfulqa"]

results = []
for model in models:
    with open(f"results/{model}.json") as f:
        data = json.load(f)
        row = {"Model": model.replace("-", "/")}
        for task in tasks:
            # Get primary metric for each task
            metrics = data["results"][task]
            if "acc" in metrics:
                row[task.upper()] = f"{metrics['acc']:.3f}"
            elif "exact_match" in metrics:
                row[task.upper()] = f"{metrics['exact_match']:.3f}"
        results.append(row)

df = pd.DataFrame(results)
print(df.to_markdown(index=False))
```

Output:
```
| Model                  | MMLU  | GSM8K | HELLASWAG | TRUTHFULQA |
|------------------------|-------|-------|-----------|------------|
| meta-llama/Llama-2-7b  | 0.459 | 0.142 | 0.765     | 0.391      |
| meta-llama/Llama-2-13b | 0.549 | 0.287 | 0.801     | 0.430      |
| mistralai/Mistral-7B   | 0.626 | 0.395 | 0.812     | 0.428      |
| microsoft/phi-2        | 0.560 | 0.613 | 0.682     | 0.447      |
```

#### Workflow 4: Evaluate with vLLM (faster inference)

Use vLLM backend for 5-10x faster evaluation.

```
vLLM Evaluation:
- [ ] Step 1: Install vLLM
- [ ] Step 2: Configure vLLM backend
- [ ] Step 3: Run evaluation
```

**Step 1: Install vLLM**

```bash
pip install vllm
```

**Step 2: Configure vLLM backend**

```bash
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8 \
  --tasks mmlu \
  --batch_size auto
```

**Step 3: Run evaluation**

vLLM is 5-10× faster than standard HuggingFace:

```bash
## Standard HF: ~2 hours for MMLU on 7B model
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --batch_size 8

## vLLM: ~15-20 minutes for MMLU on 7B model
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \
  --tasks mmlu \
  --batch_size auto
```

### When to use vs alternatives

**Use lm-evaluation-harness when:**
- Benchmarking models for academic papers
- Comparing model quality across standard tasks
- Tracking training progress
- Reporting standardized metrics (everyone uses same prompts)
- Need reproducible evaluation

**Use alternatives instead:**
- **HELM** (Stanford): Broader evaluation (fairness, efficiency, calibration)
- **AlpacaEval**: Instruction-following evaluation with LLM judges
- **MT-Bench**: Conversational multi-turn evaluation
- **Custom scripts**: Domain-specific evaluation

### Common issues

**Issue: Evaluation too slow**

Use vLLM backend:
```bash
lm_eval --model vllm \
  --model_args pretrained=model-name,tensor_parallel_size=2
```

Or reduce fewshot examples:
```bash
--num_fewshot 0  # Instead of 5
```

Or evaluate subset of MMLU:
```bash
--tasks mmlu_stem  # Only STEM subjects
```

**Issue: Out of memory**

Reduce batch size:
```bash
--batch_size 1  # Or --batch_size auto
```

Use quantization:
```bash
--model_args pretrained=model-name,load_in_8bit=True
```

Enable CPU offloading:
```bash
--model_args pretrained=model-name,device_map=auto,offload_folder=offload
```

**Issue: Different results than reported**

Check fewshot count:
```bash
--num_fewshot 5  # Most papers use 5-shot
```

Check exact task name:
```bash
--tasks mmlu  # Not mmlu_direct or mmlu_fewshot
```

Verify model and tokenizer match:
```bash
--model_args pretrained=model-name,tokenizer=same-model-name
```

**Issue: HumanEval not executing code**

Install execution dependencies:
```bash
pip install human-eval
```

Enable code execution:
```bash
lm_eval --model hf \
  --model_args pretrained=model-name \
  --tasks humaneval \
  --allow_code_execution  # Required for HumanEval
```

### Advanced topics

**Benchmark descriptions**: See [references/benchmark-guide.md](references/benchmark-guide.md) for detailed description of all 60+ tasks, what they measure, and interpretation.

**Custom tasks**: See [references/custom-tasks.md](references/custom-tasks.md) for creating domain-specific evaluation tasks.

**API evaluation**: See [references/api-evaluation.md](references/api-evaluation.md) for evaluating OpenAI, Anthropic, and other API models.

**Multi-GPU strategies**: See [references/distributed-eval.md](references/distributed-eval.md) for data parallel and tensor parallel evaluation.

### Hardware requirements

- **GPU**: NVIDIA (CUDA 11.8+), works on CPU (very slow)
- **VRAM**:
  - 7B model: 16GB (bf16) or 8GB (8-bit)
  - 13B model: 28GB (bf16) or 14GB (8-bit)
  - 70B model: Requires multi-GPU or quantization
- **Time** (7B model, single A100):
  - HellaSwag: 10 minutes
  - GSM8K: 5 minutes
  - MMLU (full): 2 hours
  - HumanEval: 20 minutes

### Resources

- GitHub: https://github.com/EleutherAI/lm-evaluation-harness
- Docs: https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs
- Task library: 60+ tasks including MMLU, GSM8K, HumanEval, TruthfulQA, HellaSwag, ARC, WinoGrande, etc.
- Leaderboard: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard (uses this harness)

---
