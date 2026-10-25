---
name: mlops-llm-fine-tuning-training-suite
description: >-
  State-of-the-Art LLM Fine-Tuning & Training Suite: Axolotl, Unsloth 5x faster training, PEFT (LoRA/QLoRA), GRPO reinforcement learning from human/rule feedback, TRL, PyTorch FSDP multi-GPU, and DSPy declarative prompt optimization.
version: 2.0.0
tags:
  - mlops
  - fine-tuning
  - axolotl
  - unsloth
  - peft
  - lora
  - grpo
  - fsdp
  - dspy
  - trl
merged_member_skills:
  - axolotl (01_Hermes_Skills_Core_Library\mlops\training\axolotl\SKILL.md)
  - dspy (01_Hermes_Skills_Core_Library\mlops\research\dspy\SKILL.md)
  - fine-tuning-with-trl (01_Hermes_Skills_Core_Library\mlops\training\trl-fine-tuning\SKILL.md)
  - grpo-rl-training (01_Hermes_Skills_Core_Library\mlops\training\grpo-rl-training\SKILL.md)
  - peft-fine-tuning (01_Hermes_Skills_Core_Library\mlops\training\peft\SKILL.md)
  - pytorch-fsdp (01_Hermes_Skills_Core_Library\mlops\training\pytorch-fsdp\SKILL.md)
  - unsloth (01_Hermes_Skills_Core_Library\mlops\training\unsloth\SKILL.md)
---

# Mlops Llm Fine Tuning Training Suite

> **Master Suite Consolidée :** Regroupe et unifie **7 compétences spécialisées** de l'écosystème Hermes en une référence modulaire et cohérente.


## 🎯 Quand Déclencher cette Master Suite (Triggers)
Cette suite doit être activée dès que l'utilisateur mentionne l'un des mots-clés, frameworks, outils ou objectifs liés aux modules inclus ci-dessous.
Chaque module peut être exécuté individuellement ou orchestré en séquence selon la tâche demandée.

---
## 📋 Vue d'Ensemble & Sommaire des Modules

1. **[axolotl](#module-1-axolotl)** : Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support
2. **[dspy](#module-2-dspy)** : Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's framework for systematic LM programming
3. **[fine-tuning-with-trl](#module-3-fine-tuning-with-trl)** : Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and reward model training. Use when need RLHF, align model with preferences, or train from human feedback. Works with HuggingFace Transformers.
4. **[grpo-rl-training](#module-4-grpo-rl-training)** : Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training
5. **[peft-fine-tuning](#module-5-peft-fine-tuning)** : Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter serving. HuggingFace's official library integrated with transformers ecosystem.
6. **[pytorch-fsdp](#module-6-pytorch-fsdp)** : Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP - parameter sharding, mixed precision, CPU offloading, FSDP2
7. **[unsloth](#module-7-unsloth)** : Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization

---

## Module 1: `axolotl`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\training\axolotl\SKILL.md`
- **Rôle / Objectif :** Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support

## Axolotl Skill

Comprehensive assistance with axolotl development, generated from official documentation.

### When to Use This Skill

This skill should be triggered when:
- Working with axolotl
- Asking about axolotl features or APIs
- Implementing axolotl solutions
- Debugging axolotl code
- Learning axolotl best practices

### Quick Reference

#### Common Patterns

**Pattern 1:** To validate that acceptable data transfer speeds exist for your training job, running NCCL Tests can help pinpoint bottlenecks, for example:

```
./build/all_reduce_perf -b 8 -e 128M -f 2 -g 3
```

**Pattern 2:** Configure your model to use FSDP in the Axolotl yaml. For example:

```
fsdp_version: 2
fsdp_config:
  offload_params: true
  state_dict_type: FULL_STATE_DICT
  auto_wrap_policy: TRANSFORMER_BASED_WRAP
  transformer_layer_cls_to_wrap: LlamaDecoderLayer
  reshard_after_forward: true
```

**Pattern 3:** The context_parallel_size should be a divisor of the total number of GPUs. For example:

```
context_parallel_size
```

**Pattern 4:** For example: - With 8 GPUs and no sequence parallelism: 8 different batches processed per step - With 8 GPUs and context_parallel_size=4: Only 2 different batches processed per step (each split across 4 GPUs) - If your per-GPU micro_batch_size is 2, the global batch size decreases from 16 to 4

```
context_parallel_size=4
```

**Pattern 5:** Setting save_compressed: true in your configuration enables saving models in a compressed format, which: - Reduces disk space usage by approximately 40% - Maintains compatibility with vLLM for accelerated inference - Maintains compatibility with llmcompressor for further optimization (example: quantization)

```
save_compressed: true
```

**Pattern 6:** Note It is not necessary to place your integration in the integrations folder. It can be in any location, so long as it’s installed in a package in your python env. See this repo for an example: https://github.com/axolotl-ai-cloud/diff-transformer

```
integrations
```

**Pattern 7:** Handle both single-example and batched data. - single example: sample[‘input_ids’] is a list[int] - batched data: sample[‘input_ids’] is a list[list[int]]

```
utils.trainer.drop_long_seq(sample, sequence_len=2048, min_sequence_len=2)
```

#### Example Code Patterns

**Example 1** (python):
```python
cli.cloud.modal_.ModalCloud(config, app=None)
```

**Example 2** (python):
```python
cli.cloud.modal_.run_cmd(cmd, run_folder, volumes=None)
```

**Example 3** (python):
```python
core.trainers.base.AxolotlTrainer(
    *_args,
    bench_data_collator=None,
    eval_data_collator=None,
    dataset_tags=None,
    **kwargs,
)
```

**Example 4** (python):
```python
core.trainers.base.AxolotlTrainer.log(logs, start_time=None)
```

**Example 5** (python):
```python
prompt_strategies.input_output.RawInputOutputPrompter()
```

### Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **dataset-formats.md** - Dataset-Formats documentation
- **other.md** - Other documentation

Use `view` to read specific reference files when detailed information is needed.

### Working with This Skill

#### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

#### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

#### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

### Resources

#### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

#### scripts/
Add helper scripts here for common automation tasks.

#### assets/
Add templates, boilerplate, or example projects here.

### Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

### Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information


---

## Module 2: `dspy`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\research\dspy\SKILL.md`
- **Rôle / Objectif :** Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's framework for systematic LM programming

## DSPy: Declarative Language Model Programming

### When to Use This Skill

Use DSPy when you need to:
- **Build complex AI systems** with multiple components and workflows
- **Program LMs declaratively** instead of manual prompt engineering
- **Optimize prompts automatically** using data-driven methods
- **Create modular AI pipelines** that are maintainable and portable
- **Improve model outputs systematically** with optimizers
- **Build RAG systems, agents, or classifiers** with better reliability

**GitHub Stars**: 22,000+ | **Created By**: Stanford NLP

### Installation

```bash
## Stable release
pip install dspy

## Latest development version
pip install git+https://github.com/stanfordnlp/dspy.git

## With specific LM providers
pip install dspy[openai]        # OpenAI
pip install dspy[anthropic]     # Anthropic Claude
pip install dspy[all]           # All providers
```

### Quick Start

#### Basic Example: Question Answering

```python
import dspy

## Configure your language model
lm = dspy.Claude(model="claude-sonnet-4-5-20250929")
dspy.settings.configure(lm=lm)

## Define a signature (input → output)
class QA(dspy.Signature):
    """Answer questions with short factual answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

## Create a module
qa = dspy.Predict(QA)

## Use it
response = qa(question="What is the capital of France?")
print(response.answer)  # "Paris"
```

#### Chain of Thought Reasoning

```python
import dspy

lm = dspy.Claude(model="claude-sonnet-4-5-20250929")
dspy.settings.configure(lm=lm)

## Use ChainOfThought for better reasoning
class MathProblem(dspy.Signature):
    """Solve math word problems."""
    problem = dspy.InputField()
    answer = dspy.OutputField(desc="numerical answer")

## ChainOfThought generates reasoning steps automatically
cot = dspy.ChainOfThought(MathProblem)

response = cot(problem="If John has 5 apples and gives 2 to Mary, how many does he have?")
print(response.rationale)  # Shows reasoning steps
print(response.answer)     # "3"
```

### Core Concepts

#### 1. Signatures

Signatures define the structure of your AI task (inputs → outputs):

```python
## Inline signature (simple)
qa = dspy.Predict("question -> answer")

## Class signature (detailed)
class Summarize(dspy.Signature):
    """Summarize text into key points."""
    text = dspy.InputField()
    summary = dspy.OutputField(desc="bullet points, 3-5 items")

summarizer = dspy.ChainOfThought(Summarize)
```

**When to use each:**
- **Inline**: Quick prototyping, simple tasks
- **Class**: Complex tasks, type hints, better documentation

#### 2. Modules

Modules are reusable components that transform inputs to outputs:

##### dspy.Predict
Basic prediction module:

```python
predictor = dspy.Predict("context, question -> answer")
result = predictor(context="Paris is the capital of France",
                   question="What is the capital?")
```

##### dspy.ChainOfThought
Generates reasoning steps before answering:

```python
cot = dspy.ChainOfThought("question -> answer")
result = cot(question="Why is the sky blue?")
print(result.rationale)  # Reasoning steps
print(result.answer)     # Final answer
```

##### dspy.ReAct
Agent-like reasoning with tools:

```python
from dspy.predict import ReAct

class SearchQA(dspy.Signature):
    """Answer questions using search."""
    question = dspy.InputField()
    answer = dspy.OutputField()

def search_tool(query: str) -> str:
    """Search Wikipedia."""
    # Your search implementation
    return results

react = ReAct(SearchQA, tools=[search_tool])
result = react(question="When was Python created?")
```

##### dspy.ProgramOfThought
Generates and executes code for reasoning:

```python
pot = dspy.ProgramOfThought("question -> answer")
result = pot(question="What is 15% of 240?")
## Generates: answer = 240 * 0.15
```

#### 3. Optimizers

Optimizers improve your modules automatically using training data:

##### BootstrapFewShot
Learns from examples:

```python
from dspy.teleprompt import BootstrapFewShot

## Training data
trainset = [
    dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),
    dspy.Example(question="What is 3+5?", answer="8").with_inputs("question"),
]

## Define metric
def validate_answer(example, pred, trace=None):
    return example.answer == pred.answer

## Optimize
optimizer = BootstrapFewShot(metric=validate_answer, max_bootstrapped_demos=3)
optimized_qa = optimizer.compile(qa, trainset=trainset)

## Now optimized_qa performs better!
```

##### MIPRO (Most Important Prompt Optimization)
Iteratively improves prompts:

```python
from dspy.teleprompt import MIPRO

optimizer = MIPRO(
    metric=validate_answer,
    num_candidates=10,
    init_temperature=1.0
)

optimized_cot = optimizer.compile(
    cot,
    trainset=trainset,
    num_trials=100
)
```

##### BootstrapFinetune
Creates datasets for model fine-tuning:

```python
from dspy.teleprompt import BootstrapFinetune

optimizer = BootstrapFinetune(metric=validate_answer)
optimized_module = optimizer.compile(qa, trainset=trainset)

## Exports training data for fine-tuning
```

#### 4. Building Complex Systems

##### Multi-Stage Pipeline

```python
import dspy

class MultiHopQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=3)
        self.generate_query = dspy.ChainOfThought("question -> search_query")
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Stage 1: Generate search query
        search_query = self.generate_query(question=question).search_query

        # Stage 2: Retrieve context
        passages = self.retrieve(search_query).passages
        context = "\n".join(passages)

        # Stage 3: Generate answer
        answer = self.generate_answer(context=context, question=question).answer
        return dspy.Prediction(answer=answer, context=context)

## Use the pipeline
qa_system = MultiHopQA()
result = qa_system(question="Who wrote the book that inspired the movie Blade Runner?")
```

##### RAG System with Optimization

```python
import dspy
from dspy.retrieve.chromadb_rm import ChromadbRM

## Configure retriever
retriever = ChromadbRM(
    collection_name="documents",
    persist_directory="./chroma_db"
)

class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

## Create and optimize
rag = RAG()

## Optimize with training data
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(metric=validate_answer)
optimized_rag = optimizer.compile(rag, trainset=trainset)
```

### LM Provider Configuration

#### Anthropic Claude

```python
import dspy

lm = dspy.Claude(
    model="claude-sonnet-4-5-20250929",
    api_key="your-api-key",  # Or set ANTHROPIC_API_KEY env var
    max_tokens=1000,
    temperature=0.7
)
dspy.settings.configure(lm=lm)
```

#### OpenAI

```python
lm = dspy.OpenAI(
    model="gpt-4",
    api_key="your-api-key",
    max_tokens=1000
)
dspy.settings.configure(lm=lm)
```

#### Local Models (Ollama)

```python
lm = dspy.OllamaLocal(
    model="llama3.1",
    base_url="http://localhost:11434"
)
dspy.settings.configure(lm=lm)
```

#### Multiple Models

```python
## Different models for different tasks
cheap_lm = dspy.OpenAI(model="gpt-3.5-turbo")
strong_lm = dspy.Claude(model="claude-sonnet-4-5-20250929")

## Use cheap model for retrieval, strong model for reasoning
with dspy.settings.context(lm=cheap_lm):
    context = retriever(question)

with dspy.settings.context(lm=strong_lm):
    answer = generator(context=context, question=question)
```

### Common Patterns

#### Pattern 1: Structured Output

```python
from pydantic import BaseModel, Field

class PersonInfo(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")
    occupation: str = Field(description="Current job")

class ExtractPerson(dspy.Signature):
    """Extract person information from text."""
    text = dspy.InputField()
    person: PersonInfo = dspy.OutputField()

extractor = dspy.TypedPredictor(ExtractPerson)
result = extractor(text="John Doe is a 35-year-old software engineer.")
print(result.person.name)  # "John Doe"
print(result.person.age)   # 35
```

#### Pattern 2: Assertion-Driven Optimization

```python
import dspy
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

class MathQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.solve = dspy.ChainOfThought("problem -> solution: float")

    def forward(self, problem):
        solution = self.solve(problem=problem).solution

        # Assert solution is numeric
        dspy.Assert(
            isinstance(float(solution), float),
            "Solution must be a number",
            backtrack=backtrack_handler
        )

        return dspy.Prediction(solution=solution)
```

#### Pattern 3: Self-Consistency

```python
import dspy
from collections import Counter

class ConsistentQA(dspy.Module):
    def __init__(self, num_samples=5):
        super().__init__()
        self.qa = dspy.ChainOfThought("question -> answer")
        self.num_samples = num_samples

    def forward(self, question):
        # Generate multiple answers
        answers = []
        for _ in range(self.num_samples):
            result = self.qa(question=question)
            answers.append(result.answer)

        # Return most common answer
        most_common = Counter(answers).most_common(1)[0][0]
        return dspy.Prediction(answer=most_common)
```

#### Pattern 4: Retrieval with Reranking

```python
class RerankedRAG(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=10)
        self.rerank = dspy.Predict("question, passage -> relevance_score: float")
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Retrieve candidates
        passages = self.retrieve(question).passages

        # Rerank passages
        scored = []
        for passage in passages:
            score = float(self.rerank(question=question, passage=passage).relevance_score)
            scored.append((score, passage))

        # Take top 3
        top_passages = [p for _, p in sorted(scored, reverse=True)[:3]]
        context = "\n\n".join(top_passages)

        # Generate answer
        return self.answer(context=context, question=question)
```

### Evaluation and Metrics

#### Custom Metrics

```python
def exact_match(example, pred, trace=None):
    """Exact match metric."""
    return example.answer.lower() == pred.answer.lower()

def f1_score(example, pred, trace=None):
    """F1 score for text overlap."""
    pred_tokens = set(pred.answer.lower().split())
    gold_tokens = set(example.answer.lower().split())

    if not pred_tokens:
        return 0.0

    precision = len(pred_tokens & gold_tokens) / len(pred_tokens)
    recall = len(pred_tokens & gold_tokens) / len(gold_tokens)

    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)
```

#### Evaluation

```python
from dspy.evaluate import Evaluate

## Create evaluator
evaluator = Evaluate(
    devset=testset,
    metric=exact_match,
    num_threads=4,
    display_progress=True
)

## Evaluate model
score = evaluator(qa_system)
print(f"Accuracy: {score}")

## Compare optimized vs unoptimized
score_before = evaluator(qa)
score_after = evaluator(optimized_qa)
print(f"Improvement: {score_after - score_before:.2%}")
```

### Best Practices

#### 1. Start Simple, Iterate

```python
## Start with Predict
qa = dspy.Predict("question -> answer")

## Add reasoning if needed
qa = dspy.ChainOfThought("question -> answer")

## Add optimization when you have data
optimized_qa = optimizer.compile(qa, trainset=data)
```

#### 2. Use Descriptive Signatures

```python
## ❌ Bad: Vague
class Task(dspy.Signature):
    input = dspy.InputField()
    output = dspy.OutputField()

## ✅ Good: Descriptive
class SummarizeArticle(dspy.Signature):
    """Summarize news articles into 3-5 key points."""
    article = dspy.InputField(desc="full article text")
    summary = dspy.OutputField(desc="bullet points, 3-5 items")
```

#### 3. Optimize with Representative Data

```python
## Create diverse training examples
trainset = [
    dspy.Example(question="factual", answer="...).with_inputs("question"),
    dspy.Example(question="reasoning", answer="...").with_inputs("question"),
    dspy.Example(question="calculation", answer="...").with_inputs("question"),
]

## Use validation set for metric
def metric(example, pred, trace=None):
    return example.answer in pred.answer
```

#### 4. Save and Load Optimized Models

```python
## Save
optimized_qa.save("models/qa_v1.json")

## Load
loaded_qa = dspy.ChainOfThought("question -> answer")
loaded_qa.load("models/qa_v1.json")
```

#### 5. Monitor and Debug

```python
## Enable tracing
dspy.settings.configure(lm=lm, trace=[])

## Run prediction
result = qa(question="...")

## Inspect trace
for call in dspy.settings.trace:
    print(f"Prompt: {call['prompt']}")
    print(f"Response: {call['response']}")
```

### Comparison to Other Approaches

| Feature | Manual Prompting | LangChain | DSPy |
|---------|-----------------|-----------|------|
| Prompt Engineering | Manual | Manual | Automatic |
| Optimization | Trial & error | None | Data-driven |
| Modularity | Low | Medium | High |
| Type Safety | No | Limited | Yes (Signatures) |
| Portability | Low | Medium | High |
| Learning Curve | Low | Medium | Medium-High |

**When to choose DSPy:**
- You have training data or can generate it
- You need systematic prompt improvement
- You're building complex multi-stage systems
- You want to optimize across different LMs

**When to choose alternatives:**
- Quick prototypes (manual prompting)
- Simple chains with existing tools (LangChain)
- Custom optimization logic needed

### Resources

- **Documentation**: https://dspy.ai
- **GitHub**: https://github.com/stanfordnlp/dspy (22k+ stars)
- **Discord**: https://discord.gg/XCGy2WDCQB
- **Twitter**: @DSPyOSS
- **Paper**: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"

### See Also

- `references/dspy_modules.md` - Detailed module guide (Predict, ChainOfThought, ReAct, ProgramOfThought)
- `references/dspy_optimizers.md` - Optimization algorithms (BootstrapFewShot, MIPRO, BootstrapFinetune)
- `references/dspy_examples.md` - Real-world examples (RAG, agents, classifiers)


---

## Module 3: `fine-tuning-with-trl`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\training\trl-fine-tuning\SKILL.md`
- **Rôle / Objectif :** Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and reward model training. Use when need RLHF, align model with preferences, or train from human feedback. Works with HuggingFace Transformers.

## TRL - Transformer Reinforcement Learning

### Quick start

TRL provides post-training methods for aligning language models with human preferences.

**Installation**:
```bash
pip install trl transformers datasets peft accelerate
```

**Supervised Fine-Tuning** (instruction tuning):
```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,  # Prompt-completion pairs
)
trainer.train()
```

**DPO** (align with preferences):
```python
from trl import DPOTrainer, DPOConfig

config = DPOConfig(output_dir="model-dpo", beta=0.1)
trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=preference_dataset,  # chosen/rejected pairs
    processing_class=tokenizer
)
trainer.train()
```

### Common workflows

#### Workflow 1: Full RLHF pipeline (SFT → Reward Model → PPO)

Complete pipeline from base model to human-aligned model.

Copy this checklist:

```
RLHF Training:
- [ ] Step 1: Supervised fine-tuning (SFT)
- [ ] Step 2: Train reward model
- [ ] Step 3: PPO reinforcement learning
- [ ] Step 4: Evaluate aligned model
```

**Step 1: Supervised fine-tuning**

Train base model on instruction-following data:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

## Load model
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")

## Load instruction dataset
dataset = load_dataset("trl-lib/Capybara", split="train")

## Configure training
training_args = SFTConfig(
    output_dir="Qwen2.5-0.5B-SFT",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=2e-5,
    logging_steps=10,
    save_strategy="epoch"
)

## Train
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)
trainer.train()
trainer.save_model()
```

**Step 2: Train reward model**

Train model to predict human preferences:

```python
from transformers import AutoModelForSequenceClassification
from trl import RewardTrainer, RewardConfig

## Load SFT model as base
model = AutoModelForSequenceClassification.from_pretrained(
    "Qwen2.5-0.5B-SFT",
    num_labels=1  # Single reward score
)
tokenizer = AutoTokenizer.from_pretrained("Qwen2.5-0.5B-SFT")

## Load preference data (chosen/rejected pairs)
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")

## Configure training
training_args = RewardConfig(
    output_dir="Qwen2.5-0.5B-Reward",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    learning_rate=1e-5
)

## Train reward model
trainer = RewardTrainer(
    model=model,
    args=training_args,
    processing_class=tokenizer,
    train_dataset=dataset
)
trainer.train()
trainer.save_model()
```

**Step 3: PPO reinforcement learning**

Optimize policy using reward model:

```bash
python -m trl.scripts.ppo \
    --model_name_or_path Qwen2.5-0.5B-SFT \
    --reward_model_path Qwen2.5-0.5B-Reward \
    --dataset_name trl-internal-testing/descriptiveness-sentiment-trl-style \
    --output_dir Qwen2.5-0.5B-PPO \
    --learning_rate 3e-6 \
    --per_device_train_batch_size 64 \
    --total_episodes 10000
```

**Step 4: Evaluate**

```python
from transformers import pipeline

## Load aligned model
generator = pipeline("text-generation", model="Qwen2.5-0.5B-PPO")

## Test
prompt = "Explain quantum computing to a 10-year-old"
output = generator(prompt, max_length=200)[0]["generated_text"]
print(output)
```

#### Workflow 2: Simple preference alignment with DPO

Align model with preferences without reward model.

Copy this checklist:

```
DPO Training:
- [ ] Step 1: Prepare preference dataset
- [ ] Step 2: Configure DPO
- [ ] Step 3: Train with DPOTrainer
- [ ] Step 4: Evaluate alignment
```

**Step 1: Prepare preference dataset**

Dataset format:
```json
{
  "prompt": "What is the capital of France?",
  "chosen": "The capital of France is Paris.",
  "rejected": "I don't know."
}
```

Load dataset:
```python
from datasets import load_dataset

dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
## Or load your own
## dataset = load_dataset("json", data_files="preferences.json")
```

**Step 2: Configure DPO**

```python
from trl import DPOConfig

config = DPOConfig(
    output_dir="Qwen2.5-0.5B-DPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=5e-7,
    beta=0.1,  # KL penalty strength
    max_prompt_length=512,
    max_length=1024,
    logging_steps=10
)
```

**Step 3: Train with DPOTrainer**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    processing_class=tokenizer
)

trainer.train()
trainer.save_model()
```

**CLI alternative**:
```bash
trl dpo \
    --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
    --dataset_name argilla/Capybara-Preferences \
    --output_dir Qwen2.5-0.5B-DPO \
    --per_device_train_batch_size 4 \
    --learning_rate 5e-7 \
    --beta 0.1
```

#### Workflow 3: Memory-efficient online RL with GRPO

Train with reinforcement learning using minimal memory.

Copy this checklist:

```
GRPO Training:
- [ ] Step 1: Define reward function
- [ ] Step 2: Configure GRPO
- [ ] Step 3: Train with GRPOTrainer
```

**Step 1: Define reward function**

```python
def reward_function(completions, **kwargs):
    """
    Compute rewards for completions.

    Args:
        completions: List of generated texts

    Returns:
        List of reward scores (floats)
    """
    rewards = []
    for completion in completions:
        # Example: reward based on length and unique words
        score = len(completion.split())  # Favor longer responses
        score += len(set(completion.lower().split()))  # Reward unique words
        rewards.append(score)
    return rewards
```

Or use a reward model:
```python
from transformers import pipeline

reward_model = pipeline("text-classification", model="reward-model-path")

def reward_from_model(completions, prompts, **kwargs):
    # Combine prompt + completion
    full_texts = [p + c for p, c in zip(prompts, completions)]
    # Get reward scores
    results = reward_model(full_texts)
    return [r["score"] for r in results]
```

**Step 2: Configure GRPO**

```python
from trl import GRPOConfig

config = GRPOConfig(
    output_dir="Qwen2-GRPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=1e-5,
    num_generations=4,  # Generate 4 completions per prompt
    max_new_tokens=128
)
```

**Step 3: Train with GRPOTrainer**

```python
from datasets import load_dataset
from trl import GRPOTrainer

## Load prompt-only dataset
dataset = load_dataset("trl-lib/tldr", split="train")

trainer = GRPOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=reward_function,  # Your reward function
    args=config,
    train_dataset=dataset
)

trainer.train()
```

**CLI**:
```bash
trl grpo \
    --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
    --dataset_name trl-lib/tldr \
    --output_dir Qwen2-GRPO \
    --num_generations 4
```

### When to use vs alternatives

**Use TRL when:**
- Need to align model with human preferences
- Have preference data (chosen/rejected pairs)
- Want to use reinforcement learning (PPO, GRPO)
- Need reward model training
- Doing RLHF (full pipeline)

**Method selection**:
- **SFT**: Have prompt-completion pairs, want basic instruction following
- **DPO**: Have preferences, want simple alignment (no reward model needed)
- **PPO**: Have reward model, need maximum control over RL
- **GRPO**: Memory-constrained, want online RL
- **Reward Model**: Building RLHF pipeline, need to score generations

**Use alternatives instead:**
- **HuggingFace Trainer**: Basic fine-tuning without RL
- **Axolotl**: YAML-based training configuration
- **LitGPT**: Educational, minimal fine-tuning
- **Unsloth**: Fast LoRA training

### Common issues

**Issue: OOM during DPO training**

Reduce batch size and sequence length:
```python
config = DPOConfig(
    per_device_train_batch_size=1,  # Reduce from 4
    max_length=512,  # Reduce from 1024
    gradient_accumulation_steps=8  # Maintain effective batch
)
```

Or use gradient checkpointing:
```python
model.gradient_checkpointing_enable()
```

**Issue: Poor alignment quality**

Tune beta parameter:
```python
## Higher beta = more conservative (stays closer to reference)
config = DPOConfig(beta=0.5)  # Default 0.1

## Lower beta = more aggressive alignment
config = DPOConfig(beta=0.01)
```

**Issue: Reward model not learning**

Check loss type and learning rate:
```python
config = RewardConfig(
    learning_rate=1e-5,  # Try different LR
    num_train_epochs=3  # Train longer
)
```

Ensure preference dataset has clear winners:
```python
## Verify dataset
print(dataset[0])
## Should have clear chosen > rejected
```

**Issue: PPO training unstable**

Adjust KL coefficient:
```python
config = PPOConfig(
    kl_coef=0.1,  # Increase from 0.05
    cliprange=0.1  # Reduce from 0.2
)
```

### Advanced topics

**SFT training guide**: See [references/fine-tuning-with-trl_sft-training.md](references/fine-tuning-with-trl_sft-training.md) for dataset formats, chat templates, packing strategies, and multi-GPU training.

**DPO variants**: See [references/fine-tuning-with-trl_dpo-variants.md](references/fine-tuning-with-trl_dpo-variants.md) for IPO, cDPO, RPO, and other DPO loss functions with recommended hyperparameters.

**Reward modeling**: See [references/fine-tuning-with-trl_reward-modeling.md](references/fine-tuning-with-trl_reward-modeling.md) for outcome vs process rewards, Bradley-Terry loss, and reward model evaluation.

**Online RL methods**: See [references/fine-tuning-with-trl_online-rl.md](references/fine-tuning-with-trl_online-rl.md) for PPO, GRPO, RLOO, and OnlineDPO with detailed configurations.

### Hardware requirements

- **GPU**: NVIDIA (CUDA required)
- **VRAM**: Depends on model and method
  - SFT 7B: 16GB (with LoRA)
  - DPO 7B: 24GB (stores reference model)
  - PPO 7B: 40GB (policy + reward model)
  - GRPO 7B: 24GB (more memory efficient)
- **Multi-GPU**: Supported via `accelerate`
- **Mixed precision**: BF16 recommended (A100/H100)

**Memory optimization**:
- Use LoRA/QLoRA for all methods
- Enable gradient checkpointing
- Use smaller batch sizes with gradient accumulation

### Resources

- Docs: https://huggingface.co/docs/trl/
- GitHub: https://github.com/huggingface/trl
- Papers:
  - "Training language models to follow instructions with human feedback" (InstructGPT, 2022)
  - "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" (DPO, 2023)
  - "Group Relative Policy Optimization" (GRPO, 2024)
- Examples: https://github.com/huggingface/trl/tree/main/examples/scripts


---

## Module 4: `grpo-rl-training`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\training\grpo-rl-training\SKILL.md`
- **Rôle / Objectif :** Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training

## GRPO/RL Training with TRL

Expert-level guidance for implementing Group Relative Policy Optimization (GRPO) using the Transformer Reinforcement Learning (TRL) library. This skill provides battle-tested patterns, critical insights, and production-ready workflows for fine-tuning language models with custom reward functions.

### When to Use This Skill

Use GRPO training when you need to:
- **Enforce specific output formats** (e.g., XML tags, JSON, structured reasoning)
- **Teach verifiable tasks** with objective correctness metrics (math, coding, fact-checking)
- **Improve reasoning capabilities** by rewarding chain-of-thought patterns
- **Align models to domain-specific behaviors** without labeled preference data
- **Optimize for multiple objectives** simultaneously (format + correctness + style)

**Do NOT use GRPO for:**
- Simple supervised fine-tuning tasks (use SFT instead)
- Tasks without clear reward signals
- When you already have high-quality preference pairs (use DPO/PPO instead)

---

### Core Concepts

#### 1. GRPO Algorithm Fundamentals

**Key Mechanism:**
- Generates **multiple completions** for each prompt (group size: 4-16)
- Compares completions within each group using reward functions
- Updates policy to favor higher-rewarded responses relative to the group

**Critical Difference from PPO:**
- No separate reward model needed
- More sample-efficient (learns from within-group comparisons)
- Simpler to implement and debug

**Mathematical Intuition:**
```
For each prompt p:
  1. Generate N completions: {c₁, c₂, ..., cₙ}
  2. Compute rewards: {r₁, r₂, ..., rₙ}
  3. Learn to increase probability of high-reward completions
     relative to low-reward ones in the same group
```

#### 2. Reward Function Design Philosophy

**Golden Rules:**
1. **Compose multiple reward functions** - Each handles one aspect (format, correctness, style)
2. **Scale rewards appropriately** - Higher weight = stronger signal
3. **Use incremental rewards** - Partial credit for partial compliance
4. **Test rewards independently** - Debug each reward function in isolation

**Reward Function Types:**

| Type | Use Case | Example Weight |
|------|----------|----------------|
| **Correctness** | Verifiable tasks (math, code) | 2.0 (highest) |
| **Format** | Strict structure enforcement | 0.5-1.0 |
| **Length** | Encourage verbosity/conciseness | 0.1-0.5 |
| **Style** | Penalize unwanted patterns | -0.5 to 0.5 |

---

### Implementation Workflow

#### Step 1: Dataset Preparation

**Critical Requirements:**
- Prompts in chat format (list of dicts with 'role' and 'content')
- Include system prompts to set expectations
- For verifiable tasks, include ground truth answers as additional columns

**Example Structure:**
```python
from datasets import load_dataset, Dataset

SYSTEM_PROMPT = """
Respond in the following format:
<reasoning>
[Your step-by-step thinking]
</reasoning>
<answer>
[Final answer]
</answer>
"""

def prepare_dataset(raw_data):
    """
    Transform raw data into GRPO-compatible format.

    Returns: Dataset with columns:
    - 'prompt': List[Dict] with role/content (system + user messages)
    - 'answer': str (ground truth, optional but recommended)
    """
    return raw_data.map(lambda x: {
        'prompt': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': x['question']}
        ],
        'answer': extract_answer(x['raw_answer'])
    })
```

**Pro Tips:**
- Use one-shot or few-shot examples in system prompt for complex formats
- Keep prompts concise (max_prompt_length: 256-512 tokens)
- Validate data quality before training (garbage in = garbage out)

#### Step 2: Reward Function Implementation

**Template Structure:**
```python
def reward_function_name(
    prompts,        # List[List[Dict]]: Original prompts
    completions,    # List[List[Dict]]: Model generations
    answer=None,    # Optional: Ground truth from dataset
    **kwargs        # Additional dataset columns
) -> list[float]:
    """
    Evaluate completions and return rewards.

    Returns: List of floats (one per completion)
    """
    # Extract completion text
    responses = [comp[0]['content'] for comp in completions]

    # Compute rewards
    rewards = []
    for response in responses:
        score = compute_score(response)
        rewards.append(score)

    return rewards
```

**Example 1: Correctness Reward (Math/Coding)**
```python
def correctness_reward(prompts, completions, answer, **kwargs):
    """Reward correct answers with high score."""
    responses = [comp[0]['content'] for comp in completions]
    extracted = [extract_final_answer(r) for r in responses]
    return [2.0 if ans == gt else 0.0
            for ans, gt in zip(extracted, answer)]
```

**Example 2: Format Reward (Structured Output)**
```python
import re

def format_reward(completions, **kwargs):
    """Reward XML-like structured format."""
    pattern = r'<reasoning>.*?</reasoning>\s*<answer>.*?</answer>'
    responses = [comp[0]['content'] for comp in completions]
    return [1.0 if re.search(pattern, r, re.DOTALL) else 0.0
            for r in responses]
```

**Example 3: Incremental Format Reward (Partial Credit)**
```python
def incremental_format_reward(completions, **kwargs):
    """Award partial credit for format compliance."""
    responses = [comp[0]['content'] for comp in completions]
    rewards = []

    for r in responses:
        score = 0.0
        if '<reasoning>' in r:
            score += 0.25
        if '</reasoning>' in r:
            score += 0.25
        if '<answer>' in r:
            score += 0.25
        if '</answer>' in r:
            score += 0.25
        # Penalize extra text after closing tag
        if r.count('</answer>') == 1:
            extra_text = r.split('</answer>')[-1].strip()
            score -= len(extra_text) * 0.001
        rewards.append(score)

    return rewards
```

**Critical Insight:**
Combine 3-5 reward functions for robust training. Order matters less than diversity of signals.

#### Step 3: Training Configuration

**Memory-Optimized Config (Small GPU)**
```python
from trl import GRPOConfig

training_args = GRPOConfig(
    output_dir="outputs/grpo-model",

    # Learning rate
    learning_rate=5e-6,          # Lower = more stable
    adam_beta1=0.9,
    adam_beta2=0.99,
    weight_decay=0.1,
    warmup_ratio=0.1,
    lr_scheduler_type='cosine',

    # Batch settings
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,  # Effective batch = 4

    # GRPO-specific
    num_generations=8,            # Group size: 8-16 recommended
    max_prompt_length=256,
    max_completion_length=512,

    # Training duration
    num_train_epochs=1,
    max_steps=None,               # Or set fixed steps (e.g., 500)

    # Optimization
    bf16=True,                    # Faster on A100/H100
    optim="adamw_8bit",          # Memory-efficient optimizer
    max_grad_norm=0.1,

    # Logging
    logging_steps=1,
    save_steps=100,
    report_to="wandb",            # Or "none" for no logging
)
```

**High-Performance Config (Large GPU)**
```python
training_args = GRPOConfig(
    output_dir="outputs/grpo-model",
    learning_rate=1e-5,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    num_generations=16,           # Larger groups = better signal
    max_prompt_length=512,
    max_completion_length=1024,
    num_train_epochs=1,
    bf16=True,
    use_vllm=True,                # Fast generation with vLLM
    logging_steps=10,
)
```

**Critical Hyperparameters:**

| Parameter | Impact | Tuning Advice |
|-----------|--------|---------------|
| `num_generations` | Group size for comparison | Start with 8, increase to 16 if GPU allows |
| `learning_rate` | Convergence speed/stability | 5e-6 (safe), 1e-5 (faster, riskier) |
| `max_completion_length` | Output verbosity | Match your task (512 for reasoning, 256 for short answers) |
| `gradient_accumulation_steps` | Effective batch size | Increase if GPU memory limited |

#### Step 4: Model Setup and Training

**Standard Setup (Transformers)**
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig
from trl import GRPOTrainer

## Load model
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # 2-3x faster
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

## Optional: LoRA for parameter-efficient training
peft_config = LoraConfig(
    r=16,                         # Rank (higher = more capacity)
    lora_alpha=32,               # Scaling factor (typically 2*r)
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    task_type="CAUSAL_LM",
    lora_dropout=0.05,
)

## Initialize trainer
trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    reward_funcs=[
        incremental_format_reward,
        format_reward,
        correctness_reward,
    ],
    args=training_args,
    train_dataset=dataset,
    peft_config=peft_config,      # Remove for full fine-tuning
)

## Train
trainer.train()

## Save
trainer.save_model("final_model")
```

**Unsloth Setup (2-3x Faster)**
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="google/gemma-3-1b-it",
    max_seq_length=1024,
    load_in_4bit=True,
    fast_inference=True,
    max_lora_rank=32,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=32,
    use_gradient_checkpointing="unsloth",
)

## Rest is identical to standard setup
trainer = GRPOTrainer(model=model, ...)
trainer.train()
```

---

### Critical Training Insights

#### 1. Loss Behavior (EXPECTED PATTERN)
- **Loss starts near 0 and INCREASES during training**
- This is CORRECT - loss measures KL divergence from initial policy
- Model is learning (diverging from original behavior to optimize rewards)
- Monitor reward metrics instead of loss for progress

#### 2. Reward Tracking
Key metrics to watch:
- `reward`: Average across all completions
- `reward_std`: Diversity within groups (should remain > 0)
- `kl`: KL divergence from reference (should grow moderately)

**Healthy Training Pattern:**
```
Step   Reward    Reward_Std   KL
100    0.5       0.3          0.02
200    0.8       0.25         0.05
300    1.2       0.2          0.08  ← Good progression
400    1.5       0.15         0.12
```

**Warning Signs:**
- Reward std → 0 (model collapsing to single response)
- KL exploding (> 0.5) (diverging too much, reduce LR)
- Reward stuck (reward functions too harsh or model capacity issue)

#### 3. Common Pitfalls and Solutions

| Problem | Symptom | Solution |
|---------|---------|----------|
| **Mode collapse** | All completions identical | Increase `num_generations`, add diversity penalty |
| **No learning** | Flat rewards | Check reward function logic, increase LR |
| **OOM errors** | GPU memory exceeded | Reduce `num_generations`, enable gradient checkpointing |
| **Slow training** | < 1 it/s | Enable `use_vllm=True`, use Unsloth, reduce seq length |
| **Format ignored** | Model doesn't follow structure | Increase format reward weight, add incremental rewards |

---

### Advanced Patterns

#### 1. Multi-Stage Training
For complex tasks, train in stages:

```python
## Stage 1: Format compliance (epochs=1)
trainer_stage1 = GRPOTrainer(
    model=model,
    reward_funcs=[incremental_format_reward, format_reward],
    ...
)
trainer_stage1.train()

## Stage 2: Correctness (epochs=1)
trainer_stage2 = GRPOTrainer(
    model=model,
    reward_funcs=[format_reward, correctness_reward],
    ...
)
trainer_stage2.train()
```

#### 2. Adaptive Reward Scaling
```python
class AdaptiveReward:
    def __init__(self, base_reward_func, initial_weight=1.0):
        self.func = base_reward_func
        self.weight = initial_weight

    def __call__(self, *args, **kwargs):
        rewards = self.func(*args, **kwargs)
        return [r * self.weight for r in rewards]

    def adjust_weight(self, success_rate):
        """Increase weight if model struggling, decrease if succeeding."""
        if success_rate < 0.3:
            self.weight *= 1.2
        elif success_rate > 0.8:
            self.weight *= 0.9
```

#### 3. Custom Dataset Integration
```python
def load_custom_knowledge_base(csv_path):
    """Example: School communication platform docs."""
    import pandas as pd
    df = pd.read_csv(csv_path)

    dataset = Dataset.from_pandas(df).map(lambda x: {
        'prompt': [
            {'role': 'system', 'content': CUSTOM_SYSTEM_PROMPT},
            {'role': 'user', 'content': x['question']}
        ],
        'answer': x['expert_answer']
    })
    return dataset
```

---

### Deployment and Inference

#### Save and Merge LoRA
```python
## Merge LoRA adapters into base model
if hasattr(trainer.model, 'merge_and_unload'):
    merged_model = trainer.model.merge_and_unload()
    merged_model.save_pretrained("production_model")
    tokenizer.save_pretrained("production_model")
```

#### Inference Example
```python
from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="production_model",
    tokenizer=tokenizer
)

result = generator(
    [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': "What is 15 + 27?"}
    ],
    max_new_tokens=256,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
)
print(result[0]['generated_text'])
```

---

### Best Practices Checklist

**Before Training:**
- [ ] Validate dataset format (prompts as List[Dict])
- [ ] Test reward functions on sample data
- [ ] Calculate expected max_prompt_length from data
- [ ] Choose appropriate num_generations based on GPU memory
- [ ] Set up logging (wandb recommended)

**During Training:**
- [ ] Monitor reward progression (should increase)
- [ ] Check reward_std (should stay > 0.1)
- [ ] Watch for OOM errors (reduce batch size if needed)
- [ ] Sample generations every 50-100 steps
- [ ] Validate format compliance on holdout set

**After Training:**
- [ ] Merge LoRA weights if using PEFT
- [ ] Test on diverse prompts
- [ ] Compare to baseline model
- [ ] Document reward weights and hyperparameters
- [ ] Save reproducibility config

---

### Troubleshooting Guide

#### Debugging Workflow
1. **Isolate reward functions** - Test each independently
2. **Check data distribution** - Ensure diversity in prompts
3. **Reduce complexity** - Start with single reward, add gradually
4. **Monitor generations** - Print samples every N steps
5. **Validate extraction logic** - Ensure answer parsing works

#### Quick Fixes
```python
## Debug reward function
def debug_reward(completions, **kwargs):
    responses = [comp[0]['content'] for comp in completions]
    for i, r in enumerate(responses[:2]):  # Print first 2
        print(f"Response {i}: {r[:200]}...")
    return [1.0] * len(responses)  # Dummy rewards

## Test without training
trainer = GRPOTrainer(..., reward_funcs=[debug_reward])
trainer.generate_completions(dataset[:1])  # Generate without updating
```

---

### References and Resources

**Official Documentation:**
- TRL GRPO Trainer: https://huggingface.co/docs/trl/grpo_trainer
- DeepSeek R1 Paper: https://arxiv.org/abs/2501.12948
- Unsloth Docs: https://docs.unsloth.ai/

**Example Repositories:**
- Open R1 Implementation: https://github.com/huggingface/open-r1
- TRL Examples: https://github.com/huggingface/trl/tree/main/examples

**Recommended Reading:**
- Progressive Disclosure Pattern for agent instructions
- Reward shaping in RL (Ng et al.)
- LoRA paper (Hu et al., 2021)

---

### Usage Instructions for Agents

When this skill is loaded:

1. **Read this entire file** before implementing GRPO training
2. **Start with the simplest reward function** (e.g., length-based) to validate setup
3. **Use the templates** in `templates/` directory as starting points
4. **Reference examples** in `examples/` for task-specific implementations
5. **Follow the workflow** sequentially (don't skip steps)
6. **Debug incrementally** - add one reward function at a time

**Critical Reminders:**
- Always use multiple reward functions (3-5 is optimal)
- Monitor reward metrics, not loss
- Test reward functions before training
- Start small (num_generations=4), scale up gradually
- Save checkpoints frequently (every 100 steps)

This skill is designed for **expert-level implementation**. Beginners should start with supervised fine-tuning before attempting GRPO.


---

## Module 5: `peft-fine-tuning`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\training\peft\SKILL.md`
- **Rôle / Objectif :** Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter serving. HuggingFace's official library integrated with transformers ecosystem.

## PEFT (Parameter-Efficient Fine-Tuning)

Fine-tune LLMs by training <1% of parameters using LoRA, QLoRA, and 25+ adapter methods.

### When to use PEFT

**Use PEFT/LoRA when:**
- Fine-tuning 7B-70B models on consumer GPUs (RTX 4090, A100)
- Need to train <1% parameters (6MB adapters vs 14GB full model)
- Want fast iteration with multiple task-specific adapters
- Deploying multiple fine-tuned variants from one base model

**Use QLoRA (PEFT + quantization) when:**
- Fine-tuning 70B models on single 24GB GPU
- Memory is the primary constraint
- Can accept ~5% quality trade-off vs full fine-tuning

**Use full fine-tuning instead when:**
- Training small models (<1B parameters)
- Need maximum quality and have compute budget
- Significant domain shift requires updating all weights

### Quick start

#### Installation

```bash
## Basic installation
pip install peft

## With quantization support (recommended)
pip install peft bitsandbytes

## Full stack
pip install peft transformers accelerate bitsandbytes datasets
```

#### LoRA fine-tuning (standard)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset

## Load base model
model_name = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

## LoRA configuration
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # Rank (8-64, higher = more capacity)
    lora_alpha=32,                 # Scaling factor (typically 2*r)
    lora_dropout=0.05,             # Dropout for regularization
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Attention layers
    bias="none"                    # Don't train biases
)

## Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
## Output: trainable params: 13,631,488 || all params: 8,043,307,008 || trainable%: 0.17%

## Prepare dataset
dataset = load_dataset("databricks/databricks-dolly-15k", split="train")

def tokenize(example):
    text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['response']}"
    return tokenizer(text, truncation=True, max_length=512, padding="max_length")

tokenized = dataset.map(tokenize, remove_columns=dataset.column_names)

## Training
training_args = TrainingArguments(
    output_dir="./lora-llama",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=lambda data: {"input_ids": torch.stack([f["input_ids"] for f in data]),
                                 "attention_mask": torch.stack([f["attention_mask"] for f in data]),
                                 "labels": torch.stack([f["input_ids"] for f in data])}
)

trainer.train()

## Save adapter only (6MB vs 16GB)
model.save_pretrained("./lora-llama-adapter")
```

#### QLoRA fine-tuning (memory-efficient)

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, prepare_model_for_kbit_training

## 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4 (best for LLMs)
    bnb_4bit_compute_dtype="bfloat16",   # Compute in bf16
    bnb_4bit_use_double_quant=True       # Nested quantization
)

## Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B",
    quantization_config=bnb_config,
    device_map="auto"
)

## Prepare for training (enables gradient checkpointing)
model = prepare_model_for_kbit_training(model)

## LoRA config for QLoRA
lora_config = LoraConfig(
    r=64,                              # Higher rank for 70B
    lora_alpha=128,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
## 70B model now fits on single 24GB GPU!
```

### LoRA parameter selection

#### Rank (r) - capacity vs efficiency

| Rank | Trainable Params | Memory | Quality | Use Case |
|------|-----------------|--------|---------|----------|
| 4 | ~3M | Minimal | Lower | Simple tasks, prototyping |
| **8** | ~7M | Low | Good | **Recommended starting point** |
| **16** | ~14M | Medium | Better | **General fine-tuning** |
| 32 | ~27M | Higher | High | Complex tasks |
| 64 | ~54M | High | Highest | Domain adaptation, 70B models |

#### Alpha (lora_alpha) - scaling factor

```python
## Rule of thumb: alpha = 2 * rank
LoraConfig(r=16, lora_alpha=32)  # Standard
LoraConfig(r=16, lora_alpha=16)  # Conservative (lower learning rate effect)
LoraConfig(r=16, lora_alpha=64)  # Aggressive (higher learning rate effect)
```

#### Target modules by architecture

```python
## Llama / Mistral / Qwen
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

## GPT-2 / GPT-Neo
target_modules = ["c_attn", "c_proj", "c_fc"]

## Falcon
target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]

## BLOOM
target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]

## Auto-detect all linear layers
target_modules = "all-linear"  # PEFT 0.6.0+
```

### Loading and merging adapters

#### Load trained adapter

```python
from peft import PeftModel, AutoPeftModelForCausalLM
from transformers import AutoModelForCausalLM

## Option 1: Load with PeftModel
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
model = PeftModel.from_pretrained(base_model, "./lora-llama-adapter")

## Option 2: Load directly (recommended)
model = AutoPeftModelForCausalLM.from_pretrained(
    "./lora-llama-adapter",
    device_map="auto"
)
```

#### Merge adapter into base model

```python
## Merge for deployment (no adapter overhead)
merged_model = model.merge_and_unload()

## Save merged model
merged_model.save_pretrained("./llama-merged")
tokenizer.save_pretrained("./llama-merged")

## Push to Hub
merged_model.push_to_hub("username/llama-finetuned")
```

#### Multi-adapter serving

```python
from peft import PeftModel

## Load base with first adapter
model = AutoPeftModelForCausalLM.from_pretrained("./adapter-task1")

## Load additional adapters
model.load_adapter("./adapter-task2", adapter_name="task2")
model.load_adapter("./adapter-task3", adapter_name="task3")

## Switch between adapters at runtime
model.set_adapter("task1")  # Use task1 adapter
output1 = model.generate(**inputs)

model.set_adapter("task2")  # Switch to task2
output2 = model.generate(**inputs)

## Disable adapters (use base model)
with model.disable_adapter():
    base_output = model.generate(**inputs)
```

### PEFT methods comparison

| Method | Trainable % | Memory | Speed | Best For |
|--------|------------|--------|-------|----------|
| **LoRA** | 0.1-1% | Low | Fast | General fine-tuning |
| **QLoRA** | 0.1-1% | Very Low | Medium | Memory-constrained |
| AdaLoRA | 0.1-1% | Low | Medium | Automatic rank selection |
| IA3 | 0.01% | Minimal | Fastest | Few-shot adaptation |
| Prefix Tuning | 0.1% | Low | Medium | Generation control |
| Prompt Tuning | 0.001% | Minimal | Fast | Simple task adaptation |
| P-Tuning v2 | 0.1% | Low | Medium | NLU tasks |

#### IA3 (minimal parameters)

```python
from peft import IA3Config

ia3_config = IA3Config(
    target_modules=["q_proj", "v_proj", "k_proj", "down_proj"],
    feedforward_modules=["down_proj"]
)
model = get_peft_model(model, ia3_config)
## Trains only 0.01% of parameters!
```

#### Prefix Tuning

```python
from peft import PrefixTuningConfig

prefix_config = PrefixTuningConfig(
    task_type="CAUSAL_LM",
    num_virtual_tokens=20,      # Prepended tokens
    prefix_projection=True       # Use MLP projection
)
model = get_peft_model(model, prefix_config)
```

### Integration patterns

#### With TRL (SFTTrainer)

```python
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules="all-linear")

trainer = SFTTrainer(
    model=model,
    args=SFTConfig(output_dir="./output", max_seq_length=512),
    train_dataset=dataset,
    peft_config=lora_config,  # Pass LoRA config directly
)
trainer.train()
```

#### With Axolotl (YAML config)

```yaml
## axolotl config.yaml
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj
lora_target_linear: true  # Target all linear layers
```

#### With vLLM (inference)

```python
from vllm import LLM
from vllm.lora.request import LoRARequest

## Load base model with LoRA support
llm = LLM(model="meta-llama/Llama-3.1-8B", enable_lora=True)

## Serve with adapter
outputs = llm.generate(
    prompts,
    lora_request=LoRARequest("adapter1", 1, "./lora-adapter")
)
```

### Performance benchmarks

#### Memory usage (Llama 3.1 8B)

| Method | GPU Memory | Trainable Params |
|--------|-----------|------------------|
| Full fine-tuning | 60+ GB | 8B (100%) |
| LoRA r=16 | 18 GB | 14M (0.17%) |
| QLoRA r=16 | 6 GB | 14M (0.17%) |
| IA3 | 16 GB | 800K (0.01%) |

#### Training speed (A100 80GB)

| Method | Tokens/sec | vs Full FT |
|--------|-----------|------------|
| Full FT | 2,500 | 1x |
| LoRA | 3,200 | 1.3x |
| QLoRA | 2,100 | 0.84x |

#### Quality (MMLU benchmark)

| Model | Full FT | LoRA | QLoRA |
|-------|---------|------|-------|
| Llama 2-7B | 45.3 | 44.8 | 44.1 |
| Llama 2-13B | 54.8 | 54.2 | 53.5 |

### Common issues

#### CUDA OOM during training

```python
## Solution 1: Enable gradient checkpointing
model.gradient_checkpointing_enable()

## Solution 2: Reduce batch size + increase accumulation
TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16
)

## Solution 3: Use QLoRA
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
```

#### Adapter not applying

```python
## Verify adapter is active
print(model.active_adapters)  # Should show adapter name

## Check trainable parameters
model.print_trainable_parameters()

## Ensure model in training mode
model.train()
```

#### Quality degradation

```python
## Increase rank
LoraConfig(r=32, lora_alpha=64)

## Target more modules
target_modules = "all-linear"

## Use more training data and epochs
TrainingArguments(num_train_epochs=5)

## Lower learning rate
TrainingArguments(learning_rate=1e-4)
```

### Best practices

1. **Start with r=8-16**, increase if quality insufficient
2. **Use alpha = 2 * rank** as starting point
3. **Target attention + MLP layers** for best quality/efficiency
4. **Enable gradient checkpointing** for memory savings
5. **Save adapters frequently** (small files, easy rollback)
6. **Evaluate on held-out data** before merging
7. **Use QLoRA for 70B+ models** on consumer hardware

### References

- **[Advanced Usage](references/peft-fine-tuning_advanced-usage.md)** - DoRA, LoftQ, rank stabilization, custom modules
- **[Troubleshooting](references/peft-fine-tuning_troubleshooting.md)** - Common errors, debugging, optimization

### Resources

- **GitHub**: https://github.com/huggingface/peft
- **Docs**: https://huggingface.co/docs/peft
- **LoRA Paper**: arXiv:2106.09685
- **QLoRA Paper**: arXiv:2305.14314
- **Models**: https://huggingface.co/models?library=peft


---

## Module 6: `pytorch-fsdp`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\training\pytorch-fsdp\SKILL.md`
- **Rôle / Objectif :** Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP - parameter sharding, mixed precision, CPU offloading, FSDP2

## Pytorch-Fsdp Skill

Comprehensive assistance with pytorch-fsdp development, generated from official documentation.

### When to Use This Skill

This skill should be triggered when:
- Working with pytorch-fsdp
- Asking about pytorch-fsdp features or APIs
- Implementing pytorch-fsdp solutions
- Debugging pytorch-fsdp code
- Learning pytorch-fsdp best practices

### Quick Reference

#### Common Patterns

**Pattern 1:** Generic Join Context Manager# Created On: Jun 06, 2025 | Last Updated On: Jun 06, 2025 The generic join context manager facilitates distributed training on uneven inputs. This page outlines the API of the relevant classes: Join, Joinable, and JoinHook. For a tutorial, see Distributed Training with Uneven Inputs Using the Join Context Manager. class torch.distributed.algorithms.Join(joinables, enable=True, throw_on_early_termination=False, **kwargs)[source]# This class defines the generic join context manager, which allows custom hooks to be called after a process joins. These hooks should shadow the collective communications of non-joined processes to prevent hanging and erroring and to ensure algorithmic correctness. Refer to JoinHook for details about the hook definition. Warning The context manager requires each participating Joinable to call the method notify_join_context() before its own per- iteration collective communications to ensure correctness. Warning The context manager requires that all process_group attributes in the JoinHook objects are the same. If there are multiple JoinHook objects, then the device of the first is used. The process group and device information is used for checking for non- joined processes and for notifying processes to throw an exception if throw_on_early_termination is enabled, both of which using an all- reduce. Parameters joinables (List[Joinable]) – a list of the participating Joinable s; their hooks are iterated over in the given order. enable (bool) – a flag enabling uneven input detection; setting to False disables the context manager’s functionality and should only be set when the user knows the inputs will not be uneven (default: True). throw_on_early_termination (bool) – a flag controlling whether to throw an exception upon detecting uneven inputs (default: False). Example: >>> import os >>> import torch >>> import torch.distributed as dist >>> import torch.multiprocessing as mp >>> import torch.nn.parallel.DistributedDataParallel as DDP >>> import torch.distributed.optim.ZeroRedundancyOptimizer as ZeRO >>> from torch.distributed.algorithms.join import Join >>> >>> # On each spawned worker >>> def worker(rank): >>> dist.init_process_group("nccl", rank=rank, world_size=2) >>> model = DDP(torch.nn.Linear(1, 1).to(rank), device_ids=[rank]) >>> optim = ZeRO(model.parameters(), torch.optim.Adam, lr=0.01) >>> # Rank 1 gets one more input than rank 0 >>> inputs = [torch.tensor([1.]).to(rank) for _ in range(10 + rank)] >>> with Join([model, optim]): >>> for input in inputs: >>> loss = model(input).sum() >>> loss.backward() >>> optim.step() >>> # All ranks reach here without hanging/erroring static notify_join_context(joinable)[source]# Notifies the join context manager that the calling process has not yet joined. Then, if throw_on_early_termination=True, checks if uneven inputs have been detected (i.e. if one process has already joined) and throws an exception if so. This method should be called from a Joinable object before its per-iteration collective communications. For example, this should be called at the beginning of the forward pass in DistributedDataParallel. Only the first Joinable object passed into the context manager performs the collective communications in this method, and for the others, this method is vacuous. Parameters joinable (Joinable) – the Joinable object calling this method. Returns An async work handle for the all-reduce meant to notify the context manager that the process has not yet joined if joinable is the first one passed into the context manager; None otherwise. class torch.distributed.algorithms.Joinable[source]# This defines an abstract base class for joinable classes. A joinable class (inheriting from Joinable) should implement join_hook(), which returns a JoinHook instance, in addition to join_device() and join_process_group() that return device and process group information, respectively. abstract property join_device: device# Return the device from which to perform collective communications needed by the join context manager. abstract join_hook(**kwargs)[source]# Return a JoinHook instance for the given Joinable. Parameters kwargs (dict) – a dict containing any keyword arguments to modify the behavior of the join hook at run time; all Joinable instances sharing the same join context manager are forwarded the same value for kwargs. Return type JoinHook abstract property join_process_group: Any# Returns the process group for the collective communications needed by the join context manager itself. class torch.distributed.algorithms.JoinHook[source]# This defines a join hook, which provides two entry points in the join context manager. Entry points : a main hook, which is called repeatedly while there exists a non-joined process, and a post-hook, which is called once all processes have joined. To implement a join hook for the generic join context manager, define a class that inherits from JoinHook and override main_hook() and post_hook() as appropriate. main_hook()[source]# Call this hook while there exists a non-joined process to shadow collective communications in a training iteration. Training iteration i.e., in one forward pass, backward pass, and optimizer step. post_hook(is_last_joiner)[source]# Call hook after all processes have joined. It is passed an additional bool argument is_last_joiner, which indicates if the rank is one of the last to join. Parameters is_last_joiner (bool) – True if the rank is one of the last to join; False otherwise.

```
Join
```

**Pattern 2:** Distributed communication package - torch.distributed# Created On: Jul 12, 2017 | Last Updated On: Sep 04, 2025 Note Please refer to PyTorch Distributed Overview for a brief introduction to all features related to distributed training. Backends# torch.distributed supports four built-in backends, each with different capabilities. The table below shows which functions are available for use with a CPU or GPU for each backend. For NCCL, GPU refers to CUDA GPU while for XCCL to XPU GPU. MPI supports CUDA only if the implementation used to build PyTorch supports it. Backend gloo mpi nccl xccl Device CPU GPU CPU GPU CPU GPU CPU GPU send ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ recv ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ broadcast ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ all_reduce ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ reduce ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ all_gather ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ gather ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ scatter ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ reduce_scatter ✓ ✓ ✘ ✘ ✘ ✓ ✘ ✓ all_to_all ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ barrier ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ Backends that come with PyTorch# PyTorch distributed package supports Linux (stable), MacOS (stable), and Windows (prototype). By default for Linux, the Gloo and NCCL backends are built and included in PyTorch distributed (NCCL only when building with CUDA). MPI is an optional backend that can only be included if you build PyTorch from source. (e.g. building PyTorch on a host that has MPI installed.) Note As of PyTorch v1.8, Windows supports all collective communications backend but NCCL, If the init_method argument of init_process_group() points to a file it must adhere to the following schema: Local file system, init_method="file:///d:/tmp/some_file" Shared file system, init_method="file://////{machine_name}/{share_folder_name}/some_file" Same as on Linux platform, you can enable TcpStore by setting environment variables, MASTER_ADDR and MASTER_PORT. Which backend to use?# In the past, we were often asked: “which backend should I use?”. Rule of thumb Use the NCCL backend for distributed training with CUDA GPU. Use the XCCL backend for distributed training with XPU GPU. Use the Gloo backend for distributed training with CPU. GPU hosts with InfiniBand interconnect Use NCCL, since it’s the only backend that currently supports InfiniBand and GPUDirect. GPU hosts with Ethernet interconnect Use NCCL, since it currently provides the best distributed GPU training performance, especially for multiprocess single-node or multi-node distributed training. If you encounter any problem with NCCL, use Gloo as the fallback option. (Note that Gloo currently runs slower than NCCL for GPUs.) CPU hosts with InfiniBand interconnect If your InfiniBand has enabled IP over IB, use Gloo, otherwise, use MPI instead. We are planning on adding InfiniBand support for Gloo in the upcoming releases. CPU hosts with Ethernet interconnect Use Gloo, unless you have specific reasons to use MPI. Common environment variables# Choosing the network interface to use# By default, both the NCCL and Gloo backends will try to find the right network interface to use. If the automatically detected interface is not correct, you can override it using the following environment variables (applicable to the respective backend): NCCL_SOCKET_IFNAME, for example export NCCL_SOCKET_IFNAME=eth0 GLOO_SOCKET_IFNAME, for example export GLOO_SOCKET_IFNAME=eth0 If you’re using the Gloo backend, you can specify multiple interfaces by separating them by a comma, like this: export GLOO_SOCKET_IFNAME=eth0,eth1,eth2,eth3. The backend will dispatch operations in a round-robin fashion across these interfaces. It is imperative that all processes specify the same number of interfaces in this variable. Other NCCL environment variables# Debugging - in case of NCCL failure, you can set NCCL_DEBUG=INFO to print an explicit warning message as well as basic NCCL initialization information. You may also use NCCL_DEBUG_SUBSYS to get more details about a specific aspect of NCCL. For example, NCCL_DEBUG_SUBSYS=COLL would print logs of collective calls, which may be helpful when debugging hangs, especially those caused by collective type or message size mismatch. In case of topology detection failure, it would be helpful to set NCCL_DEBUG_SUBSYS=GRAPH to inspect the detailed detection result and save as reference if further help from NCCL team is needed. Performance tuning - NCCL performs automatic tuning based on its topology detection to save users’ tuning effort. On some socket-based systems, users may still try tuning NCCL_SOCKET_NTHREADS and NCCL_NSOCKS_PERTHREAD to increase socket network bandwidth. These two environment variables have been pre-tuned by NCCL for some cloud providers, such as AWS or GCP. For a full list of NCCL environment variables, please refer to NVIDIA NCCL’s official documentation You can tune NCCL communicators even further using torch.distributed.ProcessGroupNCCL.NCCLConfig and torch.distributed.ProcessGroupNCCL.Options. Learn more about them using help (e.g. help(torch.distributed.ProcessGroupNCCL.NCCLConfig)) in the interpreter. Basics# The torch.distributed package provides PyTorch support and communication primitives for multiprocess parallelism across several computation nodes running on one or more machines. The class torch.nn.parallel.DistributedDataParallel() builds on this functionality to provide synchronous distributed training as a wrapper around any PyTorch model. This differs from the kinds of parallelism provided by Multiprocessing package - torch.multiprocessing and torch.nn.DataParallel() in that it supports multiple network-connected machines and in that the user must explicitly launch a separate copy of the main training script for each process. In the single-machine synchronous case, torch.distributed or the torch.nn.parallel.DistributedDataParallel() wrapper may still have advantages over other approaches to data-parallelism, including torch.nn.DataParallel(): Each process maintains its own optimizer and performs a complete optimization step with each iteration. While this may appear redundant, since the gradients have already been gathered together and averaged across processes and are thus the same for every process, this means that no parameter broadcast step is needed, reducing time spent transferring tensors between nodes. Each process contains an independent Python interpreter, eliminating the extra interpreter overhead and “GIL-thrashing” that comes from driving several execution threads, model replicas, or GPUs from a single Python process. This is especially important for models that make heavy use of the Python runtime, including models with recurrent layers or many small components. Initialization# The package needs to be initialized using the torch.distributed.init_process_group() or torch.distributed.device_mesh.init_device_mesh() function before calling any other methods. Both block until all processes have joined. Warning Initialization is not thread-safe. Process group creation should be performed from a single thread, to prevent inconsistent ‘UUID’ assignment across ranks, and to prevent races during initialization that can lead to hangs. torch.distributed.is_available()[source]# Return True if the distributed package is available. Otherwise, torch.distributed does not expose any other APIs. Currently, torch.distributed is available on Linux, MacOS and Windows. Set USE_DISTRIBUTED=1 to enable it when building PyTorch from source. Currently, the default value is USE_DISTRIBUTED=1 for Linux and Windows, USE_DISTRIBUTED=0 for MacOS. Return type bool torch.distributed.init_process_group(backend=None, init_method=None, timeout=None, world_size=-1, rank=-1, store=None, group_name='', pg_options=None, device_id=None)[source]# Initialize the default distributed process group. This will also initialize the distributed package. There are 2 main ways to initialize a process group: Specify store, rank, and world_size explicitly. Specify init_method (a URL string) which indicates where/how to discover peers. Optionally specify rank and world_size, or encode all required parameters in the URL and omit them. If neither is specified, init_method is assumed to be “env://”. Parameters backend (str or Backend, optional) – The backend to use. Depending on build-time configurations, valid values include mpi, gloo, nccl, ucc, xccl or one that is registered by a third-party plugin. Since 2.6, if backend is not provided, c10d will use a backend registered for the device type indicated by the device_id kwarg (if provided). The known default registrations today are: nccl for cuda, gloo for cpu, xccl for xpu. If neither backend nor device_id is provided, c10d will detect the accelerator on the run-time machine and use a backend registered for that detected accelerator (or cpu). This field can be given as a lowercase string (e.g., "gloo"), which can also be accessed via Backend attributes (e.g., Backend.GLOO). If using multiple processes per machine with nccl backend, each process must have exclusive access to every GPU it uses, as sharing GPUs between processes can result in deadlock or NCCL invalid usage. ucc backend is experimental. Default backend for the device can be queried with get_default_backend_for_device(). init_method (str, optional) – URL specifying how to initialize the process group. Default is “env://” if no init_method or store is specified. Mutually exclusive with store. world_size (int, optional) – Number of processes participating in the job. Required if store is specified. rank (int, optional) – Rank of the current process (it should be a number between 0 and world_size-1). Required if store is specified. store (Store, optional) – Key/value store accessible to all workers, used to exchange connection/address information. Mutually exclusive with init_method. timeout (timedelta, optional) – Timeout for operations executed against the process group. Default value is 10 minutes for NCCL and 30 minutes for other backends. This is the duration after which collectives will be aborted asynchronously and the process will crash. This is done since CUDA execution is async and it is no longer safe to continue executing user code since failed async NCCL operations might result in subsequent CUDA operations running on corrupted data. When TORCH_NCCL_BLOCKING_WAIT is set, the process will block and wait for this timeout. group_name (str, optional, deprecated) – Group name. This argument is ignored pg_options (ProcessGroupOptions, optional) – process group options specifying what additional options need to be passed in during the construction of specific process groups. As of now, the only options we support is ProcessGroupNCCL.Options for the nccl backend, is_high_priority_stream can be specified so that the nccl backend can pick up high priority cuda streams when there’re compute kernels waiting. For other available options to config nccl, See https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/api/types.html#ncclconfig-t device_id (torch.device | int, optional) – a single, specific device this process will work on, allowing for backend-specific optimizations. Currently this has two effects, only under NCCL: the communicator is immediately formed (calling ncclCommInit* immediately rather than the normal lazy call) and sub-groups will use ncclCommSplit when possible to avoid unnecessary overhead of group creation. If you want to know NCCL initialization error early, you can also use this field. If an int is provided, the API assumes that the accelerator type at compile time will be used. Note To enable backend == Backend.MPI, PyTorch needs to be built from source on a system that supports MPI. Note Support for multiple backends is experimental. Currently when no backend is specified, both gloo and nccl backends will be created. The gloo backend will be used for collectives with CPU tensors and the nccl backend will be used for collectives with CUDA tensors. A custom backend can be specified by passing in a string with format “<device_type>:<backend_name>,<device_type>:<backend_name>”, e.g. “cpu:gloo,cuda:custom_backend”. torch.distributed.device_mesh.init_device_mesh(device_type, mesh_shape, *, mesh_dim_names=None, backend_override=None)[source]# Initializes a DeviceMesh based on device_type, mesh_shape, and mesh_dim_names parameters. This creates a DeviceMesh with an n-dimensional array layout, where n is the length of mesh_shape. If mesh_dim_names is provided, each dimension is labeled as mesh_dim_names[i]. Note init_device_mesh follows SPMD programming model, meaning the same PyTorch Python program runs on all processes/ranks in the cluster. Ensure mesh_shape (the dimensions of the nD array describing device layout) is identical across all ranks. Inconsistent mesh_shape may lead to hanging. Note If no process group is found, init_device_mesh will initialize distributed process group/groups required for distributed communications behind the scene. Parameters device_type (str) – The device type of the mesh. Currently supports: “cpu”, “cuda/cuda-like”, “xpu”. Passing in a device type with a GPU index, such as “cuda:0”, is not allowed. mesh_shape (Tuple[int]) – A tuple defining the dimensions of the multi-dimensional array describing the layout of devices. mesh_dim_names (Tuple[str], optional) – A tuple of mesh dimension names to assign to each dimension of the multi-dimensional array describing the layout of devices. Its length must match the length of mesh_shape. Each string in mesh_dim_names must be unique. backend_override (Dict[int | str, tuple[str, Options] | str | Options], optional) – Overrides for some or all of the ProcessGroups that will be created for each mesh dimension. Each key can be either the index of a dimension or its name (if mesh_dim_names is provided). Each value can be a tuple containing the name of the backend and its options, or just one of these two components (in which case the other will be set to its default value). Returns A DeviceMesh object representing the device layout. Return type DeviceMesh Example: >>> from torch.distributed.device_mesh import init_device_mesh >>> >>> mesh_1d = init_device_mesh("cuda", mesh_shape=(8,)) >>> mesh_2d = init_device_mesh("cuda", mesh_shape=(2, 8), mesh_dim_names=("dp", "tp")) torch.distributed.is_initialized()[source]# Check if the default process group has been initialized. Return type bool torch.distributed.is_mpi_available()[source]# Check if the MPI backend is available. Return type bool torch.distributed.is_nccl_available()[source]# Check if the NCCL backend is available. Return type bool torch.distributed.is_gloo_available()[source]# Check if the Gloo backend is available. Return type bool torch.distributed.distributed_c10d.is_xccl_available()[source]# Check if the XCCL backend is available. Return type bool torch.distributed.is_torchelastic_launched()[source]# Check whether this process was launched with torch.distributed.elastic (aka torchelastic). The existence of TORCHELASTIC_RUN_ID environment variable is used as a proxy to determine whether the current process was launched with torchelastic. This is a reasonable proxy since TORCHELASTIC_RUN_ID maps to the rendezvous id which is always a non-null value indicating the job id for peer discovery purposes.. Return type bool torch.distributed.get_default_backend_for_device(device)[source]# Return the default backend for the given device. Parameters device (Union[str, torch.device]) – The device to get the default backend for. Returns The default backend for the given device as a lower case string. Return type str Currently three initialization methods are supported: TCP initialization# There are two ways to initialize using TCP, both requiring a network address reachable from all processes and a desired world_size. The first way requires specifying an address that belongs to the rank 0 process. This initialization method requires that all processes have manually specified ranks. Note that multicast address is not supported anymore in the latest distributed package. group_name is deprecated as well. import torch.distributed as dist # Use address of one of the machines dist.init_process_group(backend, init_method='tcp://10.1.1.20:23456', rank=args.rank, world_size=4) Shared file-system initialization# Another initialization method makes use of a file system that is shared and visible from all machines in a group, along with a desired world_size. The URL should start with file:// and contain a path to a non-existent file (in an existing directory) on a shared file system. File-system initialization will automatically create that file if it doesn’t exist, but will not delete the file. Therefore, it is your responsibility to make sure that the file is cleaned up before the next init_process_group() call on the same file path/name. Note that automatic rank assignment is not supported anymore in the latest distributed package and group_name is deprecated as well. Warning This method assumes that the file system supports locking using fcntl - most local systems and NFS support it. Warning This method will always create the file and try its best to clean up and remove the file at the end of the program. In other words, each initialization with the file init method will need a brand new empty file in order for the initialization to succeed. If the same file used by the previous initialization (which happens not to get cleaned up) is used again, this is unexpected behavior and can often cause deadlocks and failures. Therefore, even though this method will try its best to clean up the file, if the auto-delete happens to be unsuccessful, it is your responsibility to ensure that the file is removed at the end of the training to prevent the same file to be reused again during the next time. This is especially important if you plan to call init_process_group() multiple times on the same file name. In other words, if the file is not removed/cleaned up and you call init_process_group() again on that file, failures are expected. The rule of thumb here is that, make sure that the file is non-existent or empty every time init_process_group() is called. import torch.distributed as dist # rank should always be specified dist.init_process_group(backend, init_method='file:///mnt/nfs/sharedfile', world_size=4, rank=args.rank) Environment variable initialization# This method will read the configuration from environment variables, allowing one to fully customize how the information is obtained. The variables to be set are: MASTER_PORT - required; has to be a free port on machine with rank 0 MASTER_ADDR - required (except for rank 0); address of rank 0 node WORLD_SIZE - required; can be set either here, or in a call to init function RANK - required; can be set either here, or in a call to init function The machine with rank 0 will be used to set up all connections. This is the default method, meaning that init_method does not have to be specified (or can be env://). Improving initialization time# TORCH_GLOO_LAZY_INIT - establishes connections on demand rather than using a full mesh which can greatly improve initialization time for non all2all operations. Post-Initialization# Once torch.distributed.init_process_group() was run, the following functions can be used. To check whether the process group has already been initialized use torch.distributed.is_initialized(). class torch.distributed.Backend(name)[source]# An enum-like class for backends. Available backends: GLOO, NCCL, UCC, MPI, XCCL, and other registered backends. The values of this class are lowercase strings, e.g., "gloo". They can be accessed as attributes, e.g., Backend.NCCL. This class can be directly called to parse the string, e.g., Backend(backend_str) will check if backend_str is valid, and return the parsed lowercase string if so. It also accepts uppercase strings, e.g., Backend("GLOO") returns "gloo". Note The entry Backend.UNDEFINED is present but only used as initial value of some fields. Users should neither use it directly nor assume its existence. classmethod register_backend(name, func, extended_api=False, devices=None)[source]# Register a new backend with the given name and instantiating function. This class method is used by 3rd party ProcessGroup extension to register new backends. Parameters name (str) – Backend name of the ProcessGroup extension. It should match the one in init_process_group(). func (function) – Function handler that instantiates the backend. The function should be implemented in the backend extension and takes four arguments, including store, rank, world_size, and timeout. extended_api (bool, optional) – Whether the backend supports extended argument structure. Default: False. If set to True, the backend will get an instance of c10d::DistributedBackendOptions, and a process group options object as defined by the backend implementation. device (str or list of str, optional) – device type this backend supports, e.g. “cpu”, “cuda”, etc. If None, assuming both “cpu” and “cuda” Note This support of 3rd party backend is experimental and subject to change. torch.distributed.get_backend(group=None)[source]# Return the backend of the given process group. Parameters group (ProcessGroup, optional) – The process group to work on. The default is the general main process group. If another specific group is specified, the calling process must be part of group. Returns The backend of the given process group as a lower case string. Return type Backend torch.distributed.get_rank(group=None)[source]# Return the rank of the current process in the provided group, default otherwise. Rank is a unique identifier assigned to each process within a distributed process group. They are always consecutive integers ranging from 0 to world_size. Parameters group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. Returns The rank of the process group -1, if not part of the group Return type int torch.distributed.get_world_size(group=None)[source]# Return the number of processes in the current process group. Parameters group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. Returns The world size of the process group -1, if not part of the group Return type int Shutdown# It is important to clean up resources on exit by calling destroy_process_group(). The simplest pattern to follow is to destroy every process group and backend by calling destroy_process_group() with the default value of None for the group argument, at a point in the training script where communications are no longer needed, usually near the end of main(). The call should be made once per trainer-process, not at the outer process-launcher level. if destroy_process_group() is not called by all ranks in a pg within the timeout duration, especially when there are multiple process-groups in the application e.g. for N-D parallelism, hangs on exit are possible. This is because the destructor for ProcessGroupNCCL calls ncclCommAbort, which must be called collectively, but the order of calling ProcessGroupNCCL’s destructor if called by python’s GC is not deterministic. Calling destroy_process_group() helps by ensuring ncclCommAbort is called in a consistent order across ranks, and avoids calling ncclCommAbort during ProcessGroupNCCL’s destructor. Reinitialization# destroy_process_group can also be used to destroy individual process groups. One use case could be fault tolerant training, where a process group may be destroyed and then a new one initialized during runtime. In this case, it’s critical to synchronize the trainer processes using some means other than torch.distributed primitives _after_ calling destroy and before subsequently initializing. This behavior is currently unsupported/untested, due to the difficulty of achieving this synchronization, and is considered a known issue. Please file a github issue or RFC if this is a use case that’s blocking you. Groups# By default collectives operate on the default group (also called the world) and require all processes to enter the distributed function call. However, some workloads can benefit from more fine-grained communication. This is where distributed groups come into play. new_group() function can be used to create new groups, with arbitrary subsets of all processes. It returns an opaque group handle that can be given as a group argument to all collectives (collectives are distributed functions to exchange information in certain well-known programming patterns). torch.distributed.new_group(ranks=None, timeout=None, backend=None, pg_options=None, use_local_synchronization=False, group_desc=None, device_id=None)[source]# Create a new distributed group. This function requires that all processes in the main group (i.e. all processes that are part of the distributed job) enter this function, even if they are not going to be members of the group. Additionally, groups should be created in the same order in all processes. Warning Safe concurrent usage: When using multiple process groups with the NCCL backend, the user must ensure a globally consistent execution order of collectives across ranks. If multiple threads within a process issue collectives, explicit synchronization is necessary to ensure consistent ordering. When using async variants of torch.distributed communication APIs, a work object is returned and the communication kernel is enqueued on a separate CUDA stream, allowing overlap of communication and computation. Once one or more async ops have been issued on one process group, they must be synchronized with other cuda streams by calling work.wait() before using another process group. See Using multiple NCCL communicators concurrently <https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently> for more details. Parameters ranks (list[int]) – List of ranks of group members. If None, will be set to all ranks. Default is None. timeout (timedelta, optional) – see init_process_group for details and default value. backend (str or Backend, optional) – The backend to use. Depending on build-time configurations, valid values are gloo and nccl. By default uses the same backend as the global group. This field should be given as a lowercase string (e.g., "gloo"), which can also be accessed via Backend attributes (e.g., Backend.GLOO). If None is passed in, the backend corresponding to the default process group will be used. Default is None. pg_options (ProcessGroupOptions, optional) – process group options specifying what additional options need to be passed in during the construction of specific process groups. i.e. for the nccl backend, is_high_priority_stream can be specified so that process group can pick up high priority cuda streams. For other available options to config nccl, See https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/api/types.html#ncclconfig-tuse_local_synchronization (bool, optional): perform a group-local barrier at the end of the process group creation. This is different in that non-member ranks don’t need to call into API and don’t join the barrier. group_desc (str, optional) – a string to describe the process group. device_id (torch.device, optional) – a single, specific device to “bind” this process to, The new_group call will try to initialize a communication backend immediately for the device if this field is given. Returns A handle of distributed group that can be given to collective calls or GroupMember.NON_GROUP_MEMBER if the rank is not part of ranks. N.B. use_local_synchronization doesn’t work with MPI. N.B. While use_local_synchronization=True can be significantly faster with larger clusters and small process groups, care must be taken since it changes cluster behavior as non-member ranks don’t join the group barrier(). N.B. use_local_synchronization=True can lead to deadlocks when each rank creates multiple overlapping process groups. To avoid that, make sure all ranks follow the same global creation order. torch.distributed.get_group_rank(group, global_rank)[source]# Translate a global rank into a group rank. global_rank must be part of group otherwise this raises RuntimeError. Parameters group (ProcessGroup) – ProcessGroup to find the relative rank. global_rank (int) – Global rank to query. Returns Group rank of global_rank relative to group Return type int N.B. calling this function on the default process group returns identity torch.distributed.get_global_rank(group, group_rank)[source]# Translate a group rank into a global rank. group_rank must be part of group otherwise this raises RuntimeError. Parameters group (ProcessGroup) – ProcessGroup to find the global rank from. group_rank (int) – Group rank to query. Returns Global rank of group_rank relative to group Return type int N.B. calling this function on the default process group returns identity torch.distributed.get_process_group_ranks(group)[source]# Get all ranks associated with group. Parameters group (Optional[ProcessGroup]) – ProcessGroup to get all ranks from. If None, the default process group will be used. Returns List of global ranks ordered by group rank. Return type list[int] DeviceMesh# DeviceMesh is a higher level abstraction that manages process groups (or NCCL communicators). It allows user to easily create inter node and intra node process groups without worrying about how to set up the ranks correctly for different sub process groups, and it helps manage those distributed process group easily. init_device_mesh() function can be used to create new DeviceMesh, with a mesh shape describing the device topology. class torch.distributed.device_mesh.DeviceMesh(device_type, mesh, *, mesh_dim_names=None, backend_override=None, _init_backend=True)[source]# DeviceMesh represents a mesh of devices, where layout of devices could be represented as a n-d dimension array, and each value of the n-d dimensional array is the global id of the default process group ranks. DeviceMesh could be used to setup the N dimensional device connections across the cluster, and manage the ProcessGroups for N dimensional parallelisms. Communications could happen on each dimension of the DeviceMesh separately. DeviceMesh respects the device that user selects already (i.e. if user call torch.cuda.set_device before the DeviceMesh initialization), and will select/set the device for the current process if user does not set the device beforehand. Note that manual device selection should happen BEFORE the DeviceMesh initialization. DeviceMesh can also be used as a context manager when using together with DTensor APIs. Note DeviceMesh follows SPMD programming model, which means the same PyTorch Python program is running on all processes/ranks in the cluster. Therefore, users need to make sure the mesh array (which describes the layout of devices) should be identical across all ranks. Inconsistent mesh will lead to silent hang. Parameters device_type (str) – The device type of the mesh. Currently supports: “cpu”, “cuda/cuda-like”. mesh (ndarray) – A multi-dimensional array or an integer tensor describing the layout of devices, where the IDs are global IDs of the default process group. Returns A DeviceMesh object representing the device layout. Return type DeviceMesh The following program runs on each process/rank in an SPMD manner. In this example, we have 2 hosts with 4 GPUs each. A reduction over the first dimension of mesh will reduce across columns (0, 4), .. and (3, 7), a reduction over the second dimension of mesh reduces across rows (0, 1, 2, 3) and (4, 5, 6, 7). Example: >>> from torch.distributed.device_mesh import DeviceMesh >>> >>> # Initialize device mesh as (2, 4) to represent the topology >>> # of cross-host(dim 0), and within-host (dim 1). >>> mesh = DeviceMesh(device_type="cuda", mesh=[[0, 1, 2, 3],[4, 5, 6, 7]]) static from_group(group, device_type, mesh=None, *, mesh_dim_names=None)[source]# Constructs a DeviceMesh with device_type from an existing ProcessGroup or a list of existing ProcessGroup. The constructed device mesh has number of dimensions equal to the number of groups passed. For example, if a single process group is passed in, the resulted DeviceMesh is a 1D mesh. If a list of 2 process groups is passed in, the resulted DeviceMesh is a 2D mesh. If more than one group is passed, then the mesh and mesh_dim_names arguments are required. The order of the process groups passed in determines the topology of the mesh. For example, the first process group will be the 0th dimension of the DeviceMesh. The mesh tensor passed in must have the same number of dimensions as the number of process groups passed in, and the order of the dimensions in the mesh tensor must match the order in the process groups passed in. Parameters group (ProcessGroup or list[ProcessGroup]) – the existing ProcessGroup or a list of existing ProcessGroups. device_type (str) – The device type of the mesh. Currently supports: “cpu”, “cuda/cuda-like”. Passing in a device type with a GPU index, such as “cuda:0”, is not allowed. mesh (torch.Tensor or ArrayLike, optional) – A multi-dimensional array or an integer tensor describing the layout of devices, where the IDs are global IDs of the default process group. Default is None. mesh_dim_names (tuple[str], optional) – A tuple of mesh dimension names to assign to each dimension of the multi-dimensional array describing the layout of devices. Its length must match the length of mesh_shape. Each string in mesh_dim_names must be unique. Default is None. Returns A DeviceMesh object representing the device layout. Return type DeviceMesh get_all_groups()[source]# Returns a list of ProcessGroups for all mesh dimensions. Returns A list of ProcessGroup object. Return type list[torch.distributed.distributed_c10d.ProcessGroup] get_coordinate()[source]# Return the relative indices of this rank relative to all dimensions of the mesh. If this rank is not part of the mesh, return None. Return type Optional[list[int]] get_group(mesh_dim=None)[source]# Returns the single ProcessGroup specified by mesh_dim, or, if mesh_dim is not specified and the DeviceMesh is 1-dimensional, returns the only ProcessGroup in the mesh. Parameters mesh_dim (str/python:int, optional) – it can be the name of the mesh dimension or the index None. (of the mesh dimension. Default is) – Returns A ProcessGroup object. Return type ProcessGroup get_local_rank(mesh_dim=None)[source]# Returns the local rank of the given mesh_dim of the DeviceMesh. Parameters mesh_dim (str/python:int, optional) – it can be the name of the mesh dimension or the index None. (of the mesh dimension. Default is) – Returns An integer denotes the local rank. Return type int The following program runs on each process/rank in an SPMD manner. In this example, we have 2 hosts with 4 GPUs each. Calling mesh_2d.get_local_rank(mesh_dim=0) on rank 0, 1, 2, 3 would return 0. Calling mesh_2d.get_local_rank(mesh_dim=0) on rank 4, 5, 6, 7 would return 1. Calling mesh_2d.get_local_rank(mesh_dim=1) on rank 0, 4 would return 0. Calling mesh_2d.get_local_rank(mesh_dim=1) on rank 1, 5 would return 1. Calling mesh_2d.get_local_rank(mesh_dim=1) on rank 2, 6 would return 2. Calling mesh_2d.get_local_rank(mesh_dim=1) on rank 3, 7 would return 3. Example: >>> from torch.distributed.device_mesh import DeviceMesh >>> >>> # Initialize device mesh as (2, 4) to represent the topology >>> # of cross-host(dim 0), and within-host (dim 1). >>> mesh = DeviceMesh(device_type="cuda", mesh=[[0, 1, 2, 3],[4, 5, 6, 7]]) get_rank()[source]# Returns the current global rank. Return type int Point-to-point communication# torch.distributed.send(tensor, dst=None, group=None, tag=0, group_dst=None)[source]# Send a tensor synchronously. Warning tag is not supported with the NCCL backend. Parameters tensor (Tensor) – Tensor to send. dst (int) – Destination rank on global process group (regardless of group argument). Destination rank should not be the same as the rank of the current process. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. tag (int, optional) – Tag to match send with remote recv group_dst (int, optional) – Destination rank on group. Invalid to specify both dst and group_dst. torch.distributed.recv(tensor, src=None, group=None, tag=0, group_src=None)[source]# Receives a tensor synchronously. Warning tag is not supported with the NCCL backend. Parameters tensor (Tensor) – Tensor to fill with received data. src (int, optional) – Source rank on global process group (regardless of group argument). Will receive from any process if unspecified. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. tag (int, optional) – Tag to match recv with remote send group_src (int, optional) – Destination rank on group. Invalid to specify both src and group_src. Returns Sender rank -1, if not part of the group Return type int isend() and irecv() return distributed request objects when used. In general, the type of this object is unspecified as they should never be created manually, but they are guaranteed to support two methods: is_completed() - returns True if the operation has finished wait() - will block the process until the operation is finished. is_completed() is guaranteed to return True once it returns. torch.distributed.isend(tensor, dst=None, group=None, tag=0, group_dst=None)[source]# Send a tensor asynchronously. Warning Modifying tensor before the request completes causes undefined behavior. Warning tag is not supported with the NCCL backend. Unlike send, which is blocking, isend allows src == dst rank, i.e. send to self. Parameters tensor (Tensor) – Tensor to send. dst (int) – Destination rank on global process group (regardless of group argument) group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. tag (int, optional) – Tag to match send with remote recv group_dst (int, optional) – Destination rank on group. Invalid to specify both dst and group_dst Returns A distributed request object. None, if not part of the group Return type Optional[Work] torch.distributed.irecv(tensor, src=None, group=None, tag=0, group_src=None)[source]# Receives a tensor asynchronously. Warning tag is not supported with the NCCL backend. Unlike recv, which is blocking, irecv allows src == dst rank, i.e. recv from self. Parameters tensor (Tensor) – Tensor to fill with received data. src (int, optional) – Source rank on global process group (regardless of group argument). Will receive from any process if unspecified. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. tag (int, optional) – Tag to match recv with remote send group_src (int, optional) – Destination rank on group. Invalid to specify both src and group_src. Returns A distributed request object. None, if not part of the group Return type Optional[Work] torch.distributed.send_object_list(object_list, dst=None, group=None, device=None, group_dst=None, use_batch=False)[source]# Sends picklable objects in object_list synchronously. Similar to send(), but Python objects can be passed in. Note that all objects in object_list must be picklable in order to be sent. Parameters object_list (List[Any]) – List of input objects to sent. Each object must be picklable. Receiver must provide lists of equal sizes. dst (int) – Destination rank to send object_list to. Destination rank is based on global process group (regardless of group argument) group (Optional[ProcessGroup]) – (ProcessGroup, optional): The process group to work on. If None, the default process group will be used. Default is None. device (torch.device, optional) – If not None, the objects are serialized and converted to tensors which are moved to the device before sending. Default is None. group_dst (int, optional) – Destination rank on group. Must specify one of dst and group_dst but not both use_batch (bool, optional) – If True, use batch p2p operations instead of regular send operations. This avoids initializing 2-rank communicators and uses existing entire group communicators. See batch_isend_irecv for usage and assumptions. Default is False. Returns None. Note For NCCL-based process groups, internal tensor representations of objects must be moved to the GPU device before communication takes place. In this case, the device used is given by torch.cuda.current_device() and it is the user’s responsibility to ensure that this is set so that each rank has an individual GPU, via torch.cuda.set_device(). Warning Object collectives have a number of serious performance and scalability limitations. See Object collectives for details. Warning send_object_list() uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Only call this function with data you trust. Warning Calling send_object_list() with GPU tensors is not well supported and inefficient as it incurs GPU -> CPU transfer since tensors would be pickled. Please consider using send() instead. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> # Assumes backend is not NCCL >>> device = torch.device("cpu") >>> if dist.get_rank() == 0: >>> # Assumes world_size of 2. >>> objects = ["foo", 12, {1: 2}] # any picklable object >>> dist.send_object_list(objects, dst=1, device=device) >>> else: >>> objects = [None, None, None] >>> dist.recv_object_list(objects, src=0, device=device) >>> objects ['foo', 12, {1: 2}] torch.distributed.recv_object_list(object_list, src=None, group=None, device=None, group_src=None, use_batch=False)[source]# Receives picklable objects in object_list synchronously. Similar to recv(), but can receive Python objects. Parameters object_list (List[Any]) – List of objects to receive into. Must provide a list of sizes equal to the size of the list being sent. src (int, optional) – Source rank from which to recv object_list. Source rank is based on global process group (regardless of group argument) Will receive from any rank if set to None. Default is None. group (Optional[ProcessGroup]) – (ProcessGroup, optional): The process group to work on. If None, the default process group will be used. Default is None. device (torch.device, optional) – If not None, receives on this device. Default is None. group_src (int, optional) – Destination rank on group. Invalid to specify both src and group_src. use_batch (bool, optional) – If True, use batch p2p operations instead of regular send operations. This avoids initializing 2-rank communicators and uses existing entire group communicators. See batch_isend_irecv for usage and assumptions. Default is False. Returns Sender rank. -1 if rank is not part of the group. If rank is part of the group, object_list will contain the sent objects from src rank. Note For NCCL-based process groups, internal tensor representations of objects must be moved to the GPU device before communication takes place. In this case, the device used is given by torch.cuda.current_device() and it is the user’s responsibility to ensure that this is set so that each rank has an individual GPU, via torch.cuda.set_device(). Warning Object collectives have a number of serious performance and scalability limitations. See Object collectives for details. Warning recv_object_list() uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Only call this function with data you trust. Warning Calling recv_object_list() with GPU tensors is not well supported and inefficient as it incurs GPU -> CPU transfer since tensors would be pickled. Please consider using recv() instead. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> # Assumes backend is not NCCL >>> device = torch.device("cpu") >>> if dist.get_rank() == 0: >>> # Assumes world_size of 2. >>> objects = ["foo", 12, {1: 2}] # any picklable object >>> dist.send_object_list(objects, dst=1, device=device) >>> else: >>> objects = [None, None, None] >>> dist.recv_object_list(objects, src=0, device=device) >>> objects ['foo', 12, {1: 2}] torch.distributed.batch_isend_irecv(p2p_op_list)[source]# Send or Receive a batch of tensors asynchronously and return a list of requests. Process each of the operations in p2p_op_list and return the corresponding requests. NCCL, Gloo, and UCC backend are currently supported. Parameters p2p_op_list (list[torch.distributed.distributed_c10d.P2POp]) – A list of point-to-point operations(type of each operator is torch.distributed.P2POp). The order of the isend/irecv in the list matters and it needs to match with corresponding isend/irecv on the remote end. Returns A list of distributed request objects returned by calling the corresponding op in the op_list. Return type list[torch.distributed.distributed_c10d.Work] Examples >>> send_tensor = torch.arange(2, dtype=torch.float32) + 2 * rank >>> recv_tensor = torch.randn(2, dtype=torch.float32) >>> send_op = dist.P2POp(dist.isend, send_tensor, (rank + 1) % world_size) >>> recv_op = dist.P2POp( ... dist.irecv, recv_tensor, (rank - 1 + world_size) % world_size ... ) >>> reqs = batch_isend_irecv([send_op, recv_op]) >>> for req in reqs: >>> req.wait() >>> recv_tensor tensor([2, 3]) # Rank 0 tensor([0, 1]) # Rank 1 Note Note that when this API is used with the NCCL PG backend, users must set the current GPU device with torch.cuda.set_device, otherwise it will lead to unexpected hang issues. In addition, if this API is the first collective call in the group passed to dist.P2POp, all ranks of the group must participate in this API call; otherwise, the behavior is undefined. If this API call is not the first collective call in the group, batched P2P operations involving only a subset of ranks of the group are allowed. class torch.distributed.P2POp(op, tensor, peer=None, group=None, tag=0, group_peer=None)[source]# A class to build point-to-point operations for batch_isend_irecv. This class builds the type of P2P operation, communication buffer, peer rank, Process Group, and tag. Instances of this class will be passed to batch_isend_irecv for point-to-point communications. Parameters op (Callable) – A function to send data to or receive data from a peer process. The type of op is either torch.distributed.isend or torch.distributed.irecv. tensor (Tensor) – Tensor to send or receive. peer (int, optional) – Destination or source rank. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. tag (int, optional) – Tag to match send with recv. group_peer (int, optional) – Destination or source rank. Synchronous and asynchronous collective operations# Every collective operation function supports the following two kinds of operations, depending on the setting of the async_op flag passed into the collective: Synchronous operation - the default mode, when async_op is set to False. When the function returns, it is guaranteed that the collective operation is performed. In the case of CUDA operations, it is not guaranteed that the CUDA operation is completed, since CUDA operations are asynchronous. For CPU collectives, any further function calls utilizing the output of the collective call will behave as expected. For CUDA collectives, function calls utilizing the output on the same CUDA stream will behave as expected. Users must take care of synchronization under the scenario of running under different streams. For details on CUDA semantics such as stream synchronization, see CUDA Semantics. See the below script to see examples of differences in these semantics for CPU and CUDA operations. Asynchronous operation - when async_op is set to True. The collective operation function returns a distributed request object. In general, you don’t need to create it manually and it is guaranteed to support two methods: is_completed() - in the case of CPU collectives, returns True if completed. In the case of CUDA operations, returns True if the operation has been successfully enqueued onto a CUDA stream and the output can be utilized on the default stream without further synchronization. wait() - in the case of CPU collectives, will block the process until the operation is completed. In the case of CUDA collectives, will block the currently active CUDA stream until the operation is completed (but will not block the CPU). get_future() - returns torch._C.Future object. Supported for NCCL, also supported for most operations on GLOO and MPI, except for peer to peer operations. Note: as we continue adopting Futures and merging APIs, get_future() call might become redundant. Example The following code can serve as a reference regarding semantics for CUDA operations when using distributed collectives. It shows the explicit need to synchronize when using collective outputs on different CUDA streams: # Code runs on each rank. dist.init_process_group("nccl", rank=rank, world_size=2) output = torch.tensor([rank]).cuda(rank) s = torch.cuda.Stream() handle = dist.all_reduce(output, async_op=True) # Wait ensures the operation is enqueued, but not necessarily complete. handle.wait() # Using result on non-default stream. with torch.cuda.stream(s): s.wait_stream(torch.cuda.default_stream()) output.add_(100) if rank == 0: # if the explicit call to wait_stream was omitted, the output below will be # non-deterministically 1 or 101, depending on whether the allreduce overwrote # the value after the add completed. print(output) Collective functions# torch.distributed.broadcast(tensor, src=None, group=None, async_op=False, group_src=None)[source]# Broadcasts the tensor to the whole group. tensor must have the same number of elements in all processes participating in the collective. Parameters tensor (Tensor) – Data to be sent if src is the rank of current process, and tensor to be used to save received data otherwise. src (int) – Source rank on global process group (regardless of group argument). group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op group_src (int) – Source rank on group. Must specify one of group_src and src but not both. Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group torch.distributed.broadcast_object_list(object_list, src=None, group=None, device=None, group_src=None)[source]# Broadcasts picklable objects in object_list to the whole group. Similar to broadcast(), but Python objects can be passed in. Note that all objects in object_list must be picklable in order to be broadcasted. Parameters object_list (List[Any]) – List of input objects to broadcast. Each object must be picklable. Only objects on the src rank will be broadcast, but each rank must provide lists of equal sizes. src (int) – Source rank from which to broadcast object_list. Source rank is based on global process group (regardless of group argument) group (Optional[ProcessGroup]) – (ProcessGroup, optional): The process group to work on. If None, the default process group will be used. Default is None. device (torch.device, optional) – If not None, the objects are serialized and converted to tensors which are moved to the device before broadcasting. Default is None. group_src (int) – Source rank on group. Must not specify one of group_src and src but not both. Returns None. If rank is part of the group, object_list will contain the broadcasted objects from src rank. Note For NCCL-based process groups, internal tensor representations of objects must be moved to the GPU device before communication takes place. In this case, the device used is given by torch.cuda.current_device() and it is the user’s responsibility to ensure that this is set so that each rank has an individual GPU, via torch.cuda.set_device(). Note Note that this API differs slightly from the broadcast() collective since it does not provide an async_op handle and thus will be a blocking call. Warning Object collectives have a number of serious performance and scalability limitations. See Object collectives for details. Warning broadcast_object_list() uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Only call this function with data you trust. Warning Calling broadcast_object_list() with GPU tensors is not well supported and inefficient as it incurs GPU -> CPU transfer since tensors would be pickled. Please consider using broadcast() instead. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> if dist.get_rank() == 0: >>> # Assumes world_size of 3. >>> objects = ["foo", 12, {1: 2}] # any picklable object >>> else: >>> objects = [None, None, None] >>> # Assumes backend is not NCCL >>> device = torch.device("cpu") >>> dist.broadcast_object_list(objects, src=0, device=device) >>> objects ['foo', 12, {1: 2}] torch.distributed.all_reduce(tensor, op=<RedOpType.SUM: 0>, group=None, async_op=False)[source]# Reduces the tensor data across all machines in a way that all get the final result. After the call tensor is going to be bitwise identical in all processes. Complex tensors are supported. Parameters tensor (Tensor) – Input and output of the collective. The function operates in-place. op (optional) – One of the values from torch.distributed.ReduceOp enum. Specifies an operation used for element-wise reductions. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group Examples >>> # All tensors below are of torch.int64 type. >>> # We have 2 process groups, 2 ranks. >>> device = torch.device(f"cuda:{rank}") >>> tensor = torch.arange(2, dtype=torch.int64, device=device) + 1 + 2 * rank >>> tensor tensor([1, 2], device='cuda:0') # Rank 0 tensor([3, 4], device='cuda:1') # Rank 1 >>> dist.all_reduce(tensor, op=ReduceOp.SUM) >>> tensor tensor([4, 6], device='cuda:0') # Rank 0 tensor([4, 6], device='cuda:1') # Rank 1 >>> # All tensors below are of torch.cfloat type. >>> # We have 2 process groups, 2 ranks. >>> tensor = torch.tensor( ... [1 + 1j, 2 + 2j], dtype=torch.cfloat, device=device ... ) + 2 * rank * (1 + 1j) >>> tensor tensor([1.+1.j, 2.+2.j], device='cuda:0') # Rank 0 tensor([3.+3.j, 4.+4.j], device='cuda:1') # Rank 1 >>> dist.all_reduce(tensor, op=ReduceOp.SUM) >>> tensor tensor([4.+4.j, 6.+6.j], device='cuda:0') # Rank 0 tensor([4.+4.j, 6.+6.j], device='cuda:1') # Rank 1 torch.distributed.reduce(tensor, dst=None, op=<RedOpType.SUM: 0>, group=None, async_op=False, group_dst=None)[source]# Reduces the tensor data across all machines. Only the process with rank dst is going to receive the final result. Parameters tensor (Tensor) – Input and output of the collective. The function operates in-place. dst (int) – Destination rank on global process group (regardless of group argument) op (optional) – One of the values from torch.distributed.ReduceOp enum. Specifies an operation used for element-wise reductions. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op group_dst (int) – Destination rank on group. Must specify one of group_dst and dst but not both. Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group torch.distributed.all_gather(tensor_list, tensor, group=None, async_op=False)[source]# Gathers tensors from the whole group in a list. Complex and uneven sized tensors are supported. Parameters tensor_list (list[Tensor]) – Output list. It should contain correctly-sized tensors to be used for output of the collective. Uneven sized tensors are supported. tensor (Tensor) – Tensor to be broadcast from current process. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group Examples >>> # All tensors below are of torch.int64 dtype. >>> # We have 2 process groups, 2 ranks. >>> device = torch.device(f"cuda:{rank}") >>> tensor_list = [ ... torch.zeros(2, dtype=torch.int64, device=device) for _ in range(2) ... ] >>> tensor_list [tensor([0, 0], device='cuda:0'), tensor([0, 0], device='cuda:0')] # Rank 0 [tensor([0, 0], device='cuda:1'), tensor([0, 0], device='cuda:1')] # Rank 1 >>> tensor = torch.arange(2, dtype=torch.int64, device=device) + 1 + 2 * rank >>> tensor tensor([1, 2], device='cuda:0') # Rank 0 tensor([3, 4], device='cuda:1') # Rank 1 >>> dist.all_gather(tensor_list, tensor) >>> tensor_list [tensor([1, 2], device='cuda:0'), tensor([3, 4], device='cuda:0')] # Rank 0 [tensor([1, 2], device='cuda:1'), tensor([3, 4], device='cuda:1')] # Rank 1 >>> # All tensors below are of torch.cfloat dtype. >>> # We have 2 process groups, 2 ranks. >>> tensor_list = [ ... torch.zeros(2, dtype=torch.cfloat, device=device) for _ in range(2) ... ] >>> tensor_list [tensor([0.+0.j, 0.+0.j], device='cuda:0'), tensor([0.+0.j, 0.+0.j], device='cuda:0')] # Rank 0 [tensor([0.+0.j, 0.+0.j], device='cuda:1'), tensor([0.+0.j, 0.+0.j], device='cuda:1')] # Rank 1 >>> tensor = torch.tensor( ... [1 + 1j, 2 + 2j], dtype=torch.cfloat, device=device ... ) + 2 * rank * (1 + 1j) >>> tensor tensor([1.+1.j, 2.+2.j], device='cuda:0') # Rank 0 tensor([3.+3.j, 4.+4.j], device='cuda:1') # Rank 1 >>> dist.all_gather(tensor_list, tensor) >>> tensor_list [tensor([1.+1.j, 2.+2.j], device='cuda:0'), tensor([3.+3.j, 4.+4.j], device='cuda:0')] # Rank 0 [tensor([1.+1.j, 2.+2.j], device='cuda:1'), tensor([3.+3.j, 4.+4.j], device='cuda:1')] # Rank 1 torch.distributed.all_gather_into_tensor(output_tensor, input_tensor, group=None, async_op=False)[source]# Gather tensors from all ranks and put them in a single output tensor. This function requires all tensors to be the same size on each process. Parameters output_tensor (Tensor) – Output tensor to accommodate tensor elements from all ranks. It must be correctly sized to have one of the following forms: (i) a concatenation of all the input tensors along the primary dimension; for definition of “concatenation”, see torch.cat(); (ii) a stack of all the input tensors along the primary dimension; for definition of “stack”, see torch.stack(). Examples below may better explain the supported output forms. input_tensor (Tensor) – Tensor to be gathered from current rank. Different from the all_gather API, the input tensors in this API must have the same size across all ranks. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group Examples >>> # All tensors below are of torch.int64 dtype and on CUDA devices. >>> # We have two ranks. >>> device = torch.device(f"cuda:{rank}") >>> tensor_in = torch.arange(2, dtype=torch.int64, device=device) + 1 + 2 * rank >>> tensor_in tensor([1, 2], device='cuda:0') # Rank 0 tensor([3, 4], device='cuda:1') # Rank 1 >>> # Output in concatenation form >>> tensor_out = torch.zeros(world_size * 2, dtype=torch.int64, device=device) >>> dist.all_gather_into_tensor(tensor_out, tensor_in) >>> tensor_out tensor([1, 2, 3, 4], device='cuda:0') # Rank 0 tensor([1, 2, 3, 4], device='cuda:1') # Rank 1 >>> # Output in stack form >>> tensor_out2 = torch.zeros(world_size, 2, dtype=torch.int64, device=device) >>> dist.all_gather_into_tensor(tensor_out2, tensor_in) >>> tensor_out2 tensor([[1, 2], [3, 4]], device='cuda:0') # Rank 0 tensor([[1, 2], [3, 4]], device='cuda:1') # Rank 1 torch.distributed.all_gather_object(object_list, obj, group=None)[source]# Gathers picklable objects from the whole group into a list. Similar to all_gather(), but Python objects can be passed in. Note that the object must be picklable in order to be gathered. Parameters object_list (list[Any]) – Output list. It should be correctly sized as the size of the group for this collective and will contain the output. obj (Any) – Pickable Python object to be broadcast from current process. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. Default is None. Returns None. If the calling rank is part of this group, the output of the collective will be populated into the input object_list. If the calling rank is not part of the group, the passed in object_list will be unmodified. Note Note that this API differs slightly from the all_gather() collective since it does not provide an async_op handle and thus will be a blocking call. Note For NCCL-based processed groups, internal tensor representations of objects must be moved to the GPU device before communication takes place. In this case, the device used is given by torch.cuda.current_device() and it is the user’s responsibility to ensure that this is set so that each rank has an individual GPU, via torch.cuda.set_device(). Warning Object collectives have a number of serious performance and scalability limitations. See Object collectives for details. Warning all_gather_object() uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Only call this function with data you trust. Warning Calling all_gather_object() with GPU tensors is not well supported and inefficient as it incurs GPU -> CPU transfer since tensors would be pickled. Please consider using all_gather() instead. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> # Assumes world_size of 3. >>> gather_objects = ["foo", 12, {1: 2}] # any picklable object >>> output = [None for _ in gather_objects] >>> dist.all_gather_object(output, gather_objects[dist.get_rank()]) >>> output ['foo', 12, {1: 2}] torch.distributed.gather(tensor, gather_list=None, dst=None, group=None, async_op=False, group_dst=None)[source]# Gathers a list of tensors in a single process. This function requires all tensors to be the same size on each process. Parameters tensor (Tensor) – Input tensor. gather_list (list[Tensor], optional) – List of appropriately, same-sized tensors to use for gathered data (default is None, must be specified on the destination rank) dst (int, optional) – Destination rank on global process group (regardless of group argument). (If both dst and group_dst are None, default is global rank 0) group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op group_dst (int, optional) – Destination rank on group. Invalid to specify both dst and group_dst Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group Note Note that all Tensors in gather_list must have the same size. Example::>>> # We have 2 process groups, 2 ranks. >>> tensor_size = 2 >>> device = torch.device(f'cuda:{rank}') >>> tensor = torch.ones(tensor_size, device=device) + rank >>> if dist.get_rank() == 0: >>> gather_list = [torch.zeros_like(tensor, device=device) for i in range(2)] >>> else: >>> gather_list = None >>> dist.gather(tensor, gather_list, dst=0) >>> # Rank 0 gets gathered data. >>> gather_list [tensor([1., 1.], device='cuda:0'), tensor([2., 2.], device='cuda:0')] # Rank 0 None # Rank 1 torch.distributed.gather_object(obj, object_gather_list=None, dst=None, group=None, group_dst=None)[source]# Gathers picklable objects from the whole group in a single process. Similar to gather(), but Python objects can be passed in. Note that the object must be picklable in order to be gathered. Parameters obj (Any) – Input object. Must be picklable. object_gather_list (list[Any]) – Output list. On the dst rank, it should be correctly sized as the size of the group for this collective and will contain the output. Must be None on non-dst ranks. (default is None) dst (int, optional) – Destination rank on global process group (regardless of group argument). (If both dst and group_dst are None, default is global rank 0) group (Optional[ProcessGroup]) – (ProcessGroup, optional): The process group to work on. If None, the default process group will be used. Default is None. group_dst (int, optional) – Destination rank on group. Invalid to specify both dst and group_dst Returns None. On the dst rank, object_gather_list will contain the output of the collective. Note Note that this API differs slightly from the gather collective since it does not provide an async_op handle and thus will be a blocking call. Note For NCCL-based processed groups, internal tensor representations of objects must be moved to the GPU device before communication takes place. In this case, the device used is given by torch.cuda.current_device() and it is the user’s responsibility to ensure that this is set so that each rank has an individual GPU, via torch.cuda.set_device(). Warning Object collectives have a number of serious performance and scalability limitations. See Object collectives for details. Warning gather_object() uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Only call this function with data you trust. Warning Calling gather_object() with GPU tensors is not well supported and inefficient as it incurs GPU -> CPU transfer since tensors would be pickled. Please consider using gather() instead. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> # Assumes world_size of 3. >>> gather_objects = ["foo", 12, {1: 2}] # any picklable object >>> output = [None for _ in gather_objects] >>> dist.gather_object( ... gather_objects[dist.get_rank()], ... output if dist.get_rank() == 0 else None, ... dst=0 ... ) >>> # On rank 0 >>> output ['foo', 12, {1: 2}] torch.distributed.scatter(tensor, scatter_list=None, src=None, group=None, async_op=False, group_src=None)[source]# Scatters a list of tensors to all processes in a group. Each process will receive exactly one tensor and store its data in the tensor argument. Complex tensors are supported. Parameters tensor (Tensor) – Output tensor. scatter_list (list[Tensor]) – List of tensors to scatter (default is None, must be specified on the source rank) src (int) – Source rank on global process group (regardless of group argument). (If both src and group_src are None, default is global rank 0) group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op group_src (int, optional) – Source rank on group. Invalid to specify both src and group_src Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group Note Note that all Tensors in scatter_list must have the same size. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> tensor_size = 2 >>> device = torch.device(f'cuda:{rank}') >>> output_tensor = torch.zeros(tensor_size, device=device) >>> if dist.get_rank() == 0: >>> # Assumes world_size of 2. >>> # Only tensors, all of which must be the same size. >>> t_ones = torch.ones(tensor_size, device=device) >>> t_fives = torch.ones(tensor_size, device=device) * 5 >>> scatter_list = [t_ones, t_fives] >>> else: >>> scatter_list = None >>> dist.scatter(output_tensor, scatter_list, src=0) >>> # Rank i gets scatter_list[i]. >>> output_tensor tensor([1., 1.], device='cuda:0') # Rank 0 tensor([5., 5.], device='cuda:1') # Rank 1 torch.distributed.scatter_object_list(scatter_object_output_list, scatter_object_input_list=None, src=None, group=None, group_src=None)[source]# Scatters picklable objects in scatter_object_input_list to the whole group. Similar to scatter(), but Python objects can be passed in. On each rank, the scattered object will be stored as the first element of scatter_object_output_list. Note that all objects in scatter_object_input_list must be picklable in order to be scattered. Parameters scatter_object_output_list (List[Any]) – Non-empty list whose first element will store the object scattered to this rank. scatter_object_input_list (List[Any], optional) – List of input objects to scatter. Each object must be picklable. Only objects on the src rank will be scattered, and the argument can be None for non-src ranks. src (int) – Source rank from which to scatter scatter_object_input_list. Source rank is based on global process group (regardless of group argument). (If both src and group_src are None, default is global rank 0) group (Optional[ProcessGroup]) – (ProcessGroup, optional): The process group to work on. If None, the default process group will be used. Default is None. group_src (int, optional) – Source rank on group. Invalid to specify both src and group_src Returns None. If rank is part of the group, scatter_object_output_list will have its first element set to the scattered object for this rank. Note Note that this API differs slightly from the scatter collective since it does not provide an async_op handle and thus will be a blocking call. Warning Object collectives have a number of serious performance and scalability limitations. See Object collectives for details. Warning scatter_object_list() uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Only call this function with data you trust. Warning Calling scatter_object_list() with GPU tensors is not well supported and inefficient as it incurs GPU -> CPU transfer since tensors would be pickled. Please consider using scatter() instead. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> if dist.get_rank() == 0: >>> # Assumes world_size of 3. >>> objects = ["foo", 12, {1: 2}] # any picklable object >>> else: >>> # Can be any list on non-src ranks, elements are not used. >>> objects = [None, None, None] >>> output_list = [None] >>> dist.scatter_object_list(output_list, objects, src=0) >>> # Rank i gets objects[i]. For example, on rank 2: >>> output_list [{1: 2}] torch.distributed.reduce_scatter(output, input_list, op=<RedOpType.SUM: 0>, group=None, async_op=False)[source]# Reduces, then scatters a list of tensors to all processes in a group. Parameters output (Tensor) – Output tensor. input_list (list[Tensor]) – List of tensors to reduce and scatter. op (optional) – One of the values from torch.distributed.ReduceOp enum. Specifies an operation used for element-wise reductions. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op. Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group. torch.distributed.reduce_scatter_tensor(output, input, op=<RedOpType.SUM: 0>, group=None, async_op=False)[source]# Reduces, then scatters a tensor to all ranks in a group. Parameters output (Tensor) – Output tensor. It should have the same size across all ranks. input (Tensor) – Input tensor to be reduced and scattered. Its size should be output tensor size times the world size. The input tensor can have one of the following shapes: (i) a concatenation of the output tensors along the primary dimension, or (ii) a stack of the output tensors along the primary dimension. For definition of “concatenation”, see torch.cat(). For definition of “stack”, see torch.stack(). group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op. Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group. Examples >>> # All tensors below are of torch.int64 dtype and on CUDA devices. >>> # We have two ranks. >>> device = torch.device(f"cuda:{rank}") >>> tensor_out = torch.zeros(2, dtype=torch.int64, device=device) >>> # Input in concatenation form >>> tensor_in = torch.arange(world_size * 2, dtype=torch.int64, device=device) >>> tensor_in tensor([0, 1, 2, 3], device='cuda:0') # Rank 0 tensor([0, 1, 2, 3], device='cuda:1') # Rank 1 >>> dist.reduce_scatter_tensor(tensor_out, tensor_in) >>> tensor_out tensor([0, 2], device='cuda:0') # Rank 0 tensor([4, 6], device='cuda:1') # Rank 1 >>> # Input in stack form >>> tensor_in = torch.reshape(tensor_in, (world_size, 2)) >>> tensor_in tensor([[0, 1], [2, 3]], device='cuda:0') # Rank 0 tensor([[0, 1], [2, 3]], device='cuda:1') # Rank 1 >>> dist.reduce_scatter_tensor(tensor_out, tensor_in) >>> tensor_out tensor([0, 2], device='cuda:0') # Rank 0 tensor([4, 6], device='cuda:1') # Rank 1 torch.distributed.all_to_all_single(output, input, output_split_sizes=None, input_split_sizes=None, group=None, async_op=False)[source]# Split input tensor and then scatter the split list to all processes in a group. Later the received tensors are concatenated from all the processes in the group and returned as a single output tensor. Complex tensors are supported. Parameters output (Tensor) – Gathered concatenated output tensor. input (Tensor) – Input tensor to scatter. output_split_sizes – (list[Int], optional): Output split sizes for dim 0 if specified None or empty, dim 0 of output tensor must divide equally by world_size. input_split_sizes – (list[Int], optional): Input split sizes for dim 0 if specified None or empty, dim 0 of input tensor must divide equally by world_size. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op. Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group. Warning all_to_all_single is experimental and subject to change. Examples >>> input = torch.arange(4) + rank * 4 >>> input tensor([0, 1, 2, 3]) # Rank 0 tensor([4, 5, 6, 7]) # Rank 1 tensor([8, 9, 10, 11]) # Rank 2 tensor([12, 13, 14, 15]) # Rank 3 >>> output = torch.empty([4], dtype=torch.int64) >>> dist.all_to_all_single(output, input) >>> output tensor([0, 4, 8, 12]) # Rank 0 tensor([1, 5, 9, 13]) # Rank 1 tensor([2, 6, 10, 14]) # Rank 2 tensor([3, 7, 11, 15]) # Rank 3 >>> # Essentially, it is similar to following operation: >>> scatter_list = list(input.chunk(world_size)) >>> gather_list = list(output.chunk(world_size)) >>> for i in range(world_size): >>> dist.scatter(gather_list[i], scatter_list if i == rank else [], src = i) >>> # Another example with uneven split >>> input tensor([0, 1, 2, 3, 4, 5]) # Rank 0 tensor([10, 11, 12, 13, 14, 15, 16, 17, 18]) # Rank 1 tensor([20, 21, 22, 23, 24]) # Rank 2 tensor([30, 31, 32, 33, 34, 35, 36]) # Rank 3 >>> input_splits [2, 2, 1, 1] # Rank 0 [3, 2, 2, 2] # Rank 1 [2, 1, 1, 1] # Rank 2 [2, 2, 2, 1] # Rank 3 >>> output_splits [2, 3, 2, 2] # Rank 0 [2, 2, 1, 2] # Rank 1 [1, 2, 1, 2] # Rank 2 [1, 2, 1, 1] # Rank 3 >>> output = ... >>> dist.all_to_all_single(output, input, output_splits, input_splits) >>> output tensor([ 0, 1, 10, 11, 12, 20, 21, 30, 31]) # Rank 0 tensor([ 2, 3, 13, 14, 22, 32, 33]) # Rank 1 tensor([ 4, 15, 16, 23, 34, 35]) # Rank 2 tensor([ 5, 17, 18, 24, 36]) # Rank 3 >>> # Another example with tensors of torch.cfloat type. >>> input = torch.tensor( ... [1 + 1j, 2 + 2j, 3 + 3j, 4 + 4j], dtype=torch.cfloat ... ) + 4 * rank * (1 + 1j) >>> input tensor([1+1j, 2+2j, 3+3j, 4+4j]) # Rank 0 tensor([5+5j, 6+6j, 7+7j, 8+8j]) # Rank 1 tensor([9+9j, 10+10j, 11+11j, 12+12j]) # Rank 2 tensor([13+13j, 14+14j, 15+15j, 16+16j]) # Rank 3 >>> output = torch.empty([4], dtype=torch.int64) >>> dist.all_to_all_single(output, input) >>> output tensor([1+1j, 5+5j, 9+9j, 13+13j]) # Rank 0 tensor([2+2j, 6+6j, 10+10j, 14+14j]) # Rank 1 tensor([3+3j, 7+7j, 11+11j, 15+15j]) # Rank 2 tensor([4+4j, 8+8j, 12+12j, 16+16j]) # Rank 3 torch.distributed.all_to_all(output_tensor_list, input_tensor_list, group=None, async_op=False)[source]# Scatters list of input tensors to all processes in a group and return gathered list of tensors in output list. Complex tensors are supported. Parameters output_tensor_list (list[Tensor]) – List of tensors to be gathered one per rank. input_tensor_list (list[Tensor]) – List of tensors to scatter one per rank. group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op. Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group. Warning all_to_all is experimental and subject to change. Examples >>> input = torch.arange(4) + rank * 4 >>> input = list(input.chunk(4)) >>> input [tensor([0]), tensor([1]), tensor([2]), tensor([3])] # Rank 0 [tensor([4]), tensor([5]), tensor([6]), tensor([7])] # Rank 1 [tensor([8]), tensor([9]), tensor([10]), tensor([11])] # Rank 2 [tensor([12]), tensor([13]), tensor([14]), tensor([15])] # Rank 3 >>> output = list(torch.empty([4], dtype=torch.int64).chunk(4)) >>> dist.all_to_all(output, input) >>> output [tensor([0]), tensor([4]), tensor([8]), tensor([12])] # Rank 0 [tensor([1]), tensor([5]), tensor([9]), tensor([13])] # Rank 1 [tensor([2]), tensor([6]), tensor([10]), tensor([14])] # Rank 2 [tensor([3]), tensor([7]), tensor([11]), tensor([15])] # Rank 3 >>> # Essentially, it is similar to following operation: >>> scatter_list = input >>> gather_list = output >>> for i in range(world_size): >>> dist.scatter(gather_list[i], scatter_list if i == rank else [], src=i) >>> input tensor([0, 1, 2, 3, 4, 5]) # Rank 0 tensor([10, 11, 12, 13, 14, 15, 16, 17, 18]) # Rank 1 tensor([20, 21, 22, 23, 24]) # Rank 2 tensor([30, 31, 32, 33, 34, 35, 36]) # Rank 3 >>> input_splits [2, 2, 1, 1] # Rank 0 [3, 2, 2, 2] # Rank 1 [2, 1, 1, 1] # Rank 2 [2, 2, 2, 1] # Rank 3 >>> output_splits [2, 3, 2, 2] # Rank 0 [2, 2, 1, 2] # Rank 1 [1, 2, 1, 2] # Rank 2 [1, 2, 1, 1] # Rank 3 >>> input = list(input.split(input_splits)) >>> input [tensor([0, 1]), tensor([2, 3]), tensor([4]), tensor([5])] # Rank 0 [tensor([10, 11, 12]), tensor([13, 14]), tensor([15, 16]), tensor([17, 18])] # Rank 1 [tensor([20, 21]), tensor([22]), tensor([23]), tensor([24])] # Rank 2 [tensor([30, 31]), tensor([32, 33]), tensor([34, 35]), tensor([36])] # Rank 3 >>> output = ... >>> dist.all_to_all(output, input) >>> output [tensor([0, 1]), tensor([10, 11, 12]), tensor([20, 21]), tensor([30, 31])] # Rank 0 [tensor([2, 3]), tensor([13, 14]), tensor([22]), tensor([32, 33])] # Rank 1 [tensor([4]), tensor([15, 16]), tensor([23]), tensor([34, 35])] # Rank 2 [tensor([5]), tensor([17, 18]), tensor([24]), tensor([36])] # Rank 3 >>> # Another example with tensors of torch.cfloat type. >>> input = torch.tensor( ... [1 + 1j, 2 + 2j, 3 + 3j, 4 + 4j], dtype=torch.cfloat ... ) + 4 * rank * (1 + 1j) >>> input = list(input.chunk(4)) >>> input [tensor([1+1j]), tensor([2+2j]), tensor([3+3j]), tensor([4+4j])] # Rank 0 [tensor([5+5j]), tensor([6+6j]), tensor([7+7j]), tensor([8+8j])] # Rank 1 [tensor([9+9j]), tensor([10+10j]), tensor([11+11j]), tensor([12+12j])] # Rank 2 [tensor([13+13j]), tensor([14+14j]), tensor([15+15j]), tensor([16+16j])] # Rank 3 >>> output = list(torch.empty([4], dtype=torch.int64).chunk(4)) >>> dist.all_to_all(output, input) >>> output [tensor([1+1j]), tensor([5+5j]), tensor([9+9j]), tensor([13+13j])] # Rank 0 [tensor([2+2j]), tensor([6+6j]), tensor([10+10j]), tensor([14+14j])] # Rank 1 [tensor([3+3j]), tensor([7+7j]), tensor([11+11j]), tensor([15+15j])] # Rank 2 [tensor([4+4j]), tensor([8+8j]), tensor([12+12j]), tensor([16+16j])] # Rank 3 torch.distributed.barrier(group=None, async_op=False, device_ids=None)[source]# Synchronize all processes. This collective blocks processes until the whole group enters this function, if async_op is False, or if async work handle is called on wait(). Parameters group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. async_op (bool, optional) – Whether this op should be an async op device_ids ([int], optional) – List of device/GPU ids. Only one id is expected. Returns Async work handle, if async_op is set to True. None, if not async_op or if not part of the group Note ProcessGroupNCCL now blocks the cpu thread till the completion of the barrier collective. Note ProcessGroupNCCL implements barrier as an all_reduce of a 1-element tensor. A device must be chosen for allocating this tensor. The device choice is made by checking in this order (1) the first device passed to device_ids arg of barrier if not None, (2) the device passed to init_process_group if not None, (3) the device that was first used with this process group, if another collective with tensor inputs has been performed, (4) the device index indicated by the global rank mod local device count. torch.distributed.monitored_barrier(group=None, timeout=None, wait_all_ranks=False)[source]# Synchronize processes similar to torch.distributed.barrier, but consider a configurable timeout. It is able to report ranks that did not pass this barrier within the provided timeout. Specifically, for non-zero ranks, will block until a send/recv is processed from rank 0. Rank 0 will block until all send /recv from other ranks are processed, and will report failures for ranks that failed to respond in time. Note that if one rank does not reach the monitored_barrier (for example due to a hang), all other ranks would fail in monitored_barrier. This collective will block all processes/ranks in the group, until the whole group exits the function successfully, making it useful for debugging and synchronizing. However, it can have a performance impact and should only be used for debugging or scenarios that require full synchronization points on the host-side. For debugging purposes, this barrier can be inserted before the application’s collective calls to check if any ranks are desynchronized. Note Note that this collective is only supported with the GLOO backend. Parameters group (ProcessGroup, optional) – The process group to work on. If None, the default process group will be used. timeout (datetime.timedelta, optional) – Timeout for monitored_barrier. If None, the default process group timeout will be used. wait_all_ranks (bool, optional) – Whether to collect all failed ranks or not. By default, this is False and monitored_barrier on rank 0 will throw on the first failed rank it encounters in order to fail fast. By setting wait_all_ranks=True monitored_barrier will collect all failed ranks and throw an error containing information about all failed ranks. Returns None. Example::>>> # Note: Process group initialization omitted on each rank. >>> import torch.distributed as dist >>> if dist.get_rank() != 1: >>> dist.monitored_barrier() # Raises exception indicating that >>> # rank 1 did not call into monitored_barrier. >>> # Example with wait_all_ranks=True >>> if dist.get_rank() == 0: >>> dist.monitored_barrier(wait_all_ranks=True) # Raises exception >>> # indicating that ranks 1, 2, ... world_size - 1 did not call into >>> # monitored_barrier. class torch.distributed.Work# A Work object represents the handle to a pending asynchronous operation in PyTorch’s distributed package. It is returned by non-blocking collective operations, such as dist.all_reduce(tensor, async_op=True). block_current_stream(self: torch._C._distributed_c10d.Work) → None# Blocks the currently active GPU stream on the operation to complete. For GPU based collectives this is equivalent to synchronize. For CPU initiated collectives such as with Gloo this will block the CUDA stream until the operation is complete. This returns immediately in all cases. To check whether an operation was successful you should check the Work object result asynchronously. boxed(self: torch._C._distributed_c10d.Work) → object# exception(self: torch._C._distributed_c10d.Work) → std::__exception_ptr::exception_ptr# get_future(self: torch._C._distributed_c10d.Work) → torch.Future# Returns A torch.futures.Future object which is associated with the completion of the Work. As an example, a future object can be retrieved by fut = process_group.allreduce(tensors).get_future(). Example::Below is an example of a simple allreduce DDP communication hook that uses get_future API to retrieve a Future associated with the completion of allreduce. >>> def allreduce(process_group: dist.ProcessGroup, bucket: dist.GradBucket): -> torch.futures.Future >>> group_to_use = process_group if process_group is not None else torch.distributed.group.WORLD >>> tensor = bucket.buffer().div_(group_to_use.size()) >>> return torch.distributed.all_reduce(tensor, group=group_to_use, async_op=True).get_future() >>> ddp_model.register_comm_hook(state=None, hook=allreduce) Warning get_future API supports NCCL, and partially GLOO and MPI backends (no support for peer-to-peer operations like send/recv) and will return a torch.futures.Future. In the example above, allreduce work will be done on GPU using NCCL backend, fut.wait() will return after synchronizing the appropriate NCCL streams with PyTorch’s current device streams to ensure we can have asynchronous CUDA execution and it does not wait for the entire operation to complete on GPU. Note that CUDAFuture does not support TORCH_NCCL_BLOCKING_WAIT flag or NCCL’s barrier(). In addition, if a callback function was added by fut.then(), it will wait until WorkNCCL’s NCCL streams synchronize with ProcessGroupNCCL’s dedicated callback stream and invoke the callback inline after running the callback on the callback stream. fut.then() will return another CUDAFuture that holds the return value of the callback and a CUDAEvent that recorded the callback stream. For CPU work, fut.done() returns true when work has been completed and value() tensors are ready. For GPU work, fut.done() returns true only whether the operation has been enqueued. For mixed CPU-GPU work (e.g. sending GPU tensors with GLOO), fut.done() returns true when tensors have arrived on respective nodes, but not yet necessarily synched on respective GPUs (similarly to GPU work). get_future_result(self: torch._C._distributed_c10d.Work) → torch.Future# Returns A torch.futures.Future object of int type which maps to the enum type of WorkResult As an example, a future object can be retrieved by fut = process_group.allreduce(tensor).get_future_result(). Example::users can use fut.wait() to blocking wait for the completion of the work and get the WorkResult by fut.value(). Also, users can use fut.then(call_back_func) to register a callback function to be called when the work is completed, without blocking the current thread. Warning get_future_result API supports NCCL is_completed(self: torch._C._distributed_c10d.Work) → bool# is_success(self: torch._C._distributed_c10d.Work) → bool# result(self: torch._C._distributed_c10d.Work) → list[torch.Tensor]# source_rank(self: torch._C._distributed_c10d.Work) → int# synchronize(self: torch._C._distributed_c10d.Work) → None# static unbox(arg0: object) → torch._C._distributed_c10d.Work# wait(self: torch._C._distributed_c10d.Work, timeout: datetime.timedelta = datetime.timedelta(0)) → bool# Returns true/false. Example:: try:work.wait(timeout) except:# some handling Warning In normal cases, users do not need to set the timeout. calling wait() is the same as calling synchronize(): Letting the current stream block on the completion of the NCCL work. However, if timeout is set, it will block the CPU thread until the NCCL work is completed or timed out. If timeout, exception will be thrown. class torch.distributed.ReduceOp# An enum-like class for available reduction operations: SUM, PRODUCT, MIN, MAX, BAND, BOR, BXOR, and PREMUL_SUM. BAND, BOR, and BXOR reductions are not available when using the NCCL backend. AVG divides values by the world size before summing across ranks. AVG is only available with the NCCL backend, and only for NCCL versions 2.10 or later. PREMUL_SUM multiplies inputs by a given scalar locally before reduction. PREMUL_SUM is only available with the NCCL backend, and only available for NCCL versions 2.11 or later. Users are supposed to use torch.distributed._make_nccl_premul_sum. Additionally, MAX, MIN and PRODUCT are not supported for complex tensors. The values of this class can be accessed as attributes, e.g., ReduceOp.SUM. They are used in specifying strategies for reduction collectives, e.g., reduce(). This class does not support __members__ property. class torch.distributed.reduce_op# Deprecated enum-like class for reduction operations: SUM, PRODUCT, MIN, and MAX. ReduceOp is recommended to use instead. Distributed Key-Value Store# The distributed package comes with a distributed key-value store, which can be used to share information between processes in the group as well as to initialize the distributed package in torch.distributed.init_process_group() (by explicitly creating the store as an alternative to specifying init_method.) There are 3 choices for Key-Value Stores: TCPStore, FileStore, and HashStore. class torch.distributed.Store# Base class for all store implementations, such as the 3 provided by PyTorch distributed: (TCPStore, FileStore, and HashStore). __init__(self: torch._C._distributed_c10d.Store) → None# add(self: torch._C._distributed_c10d.Store, arg0: str, arg1: SupportsInt) → int# The first call to add for a given key creates a counter associated with key in the store, initialized to amount. Subsequent calls to add with the same key increment the counter by the specified amount. Calling add() with a key that has already been set in the store by set() will result in an exception. Parameters key (str) – The key in the store whose counter will be incremented. amount (int) – The quantity by which the counter will be incremented. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Using TCPStore as an example, other store types can also be used >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.add("first_key", 1) >>> store.add("first_key", 6) >>> # Should return 7 >>> store.get("first_key") append(self: torch._C._distributed_c10d.Store, arg0: str, arg1: str) → None# Append the key-value pair into the store based on the supplied key and value. If key does not exists in the store, it will be created. Parameters key (str) – The key to be appended to the store. value (str) – The value associated with key to be added to the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.append("first_key", "po") >>> store.append("first_key", "tato") >>> # Should return "potato" >>> store.get("first_key") check(self: torch._C._distributed_c10d.Store, arg0: collections.abc.Sequence[str]) → bool# The call to check whether a given list of keys have value stored in the store. This call immediately returns in normal cases but still suffers from some edge deadlock cases, e.g, calling check after TCPStore has been destroyed. Calling check() with a list of keys that one wants to check whether stored in the store or not. Parameters keys (list[str]) – The keys to query whether stored in the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Using TCPStore as an example, other store types can also be used >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.add("first_key", 1) >>> # Should return 7 >>> store.check(["first_key"]) clone(self: torch._C._distributed_c10d.Store) → torch._C._distributed_c10d.Store# Clones the store and returns a new object that points to the same underlying store. The returned store can be used concurrently with the original object. This is intended to provide a safe way to use a store from multiple threads by cloning one store per thread. compare_set(self: torch._C._distributed_c10d.Store, arg0: str, arg1: str, arg2: str) → bytes# Inserts the key-value pair into the store based on the supplied key and performs comparison between expected_value and desired_value before inserting. desired_value will only be set if expected_value for the key already exists in the store or if expected_value is an empty string. Parameters key (str) – The key to be checked in the store. expected_value (str) – The value associated with key to be checked before insertion. desired_value (str) – The value associated with key to be added to the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.set("key", "first_value") >>> store.compare_set("key", "first_value", "second_value") >>> # Should return "second_value" >>> store.get("key") delete_key(self: torch._C._distributed_c10d.Store, arg0: str) → bool# Deletes the key-value pair associated with key from the store. Returns true if the key was successfully deleted, and false if it was not. Warning The delete_key API is only supported by the TCPStore and HashStore. Using this API with the FileStore will result in an exception. Parameters key (str) – The key to be deleted from the store Returns True if key was deleted, otherwise False. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Using TCPStore as an example, HashStore can also be used >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.set("first_key") >>> # This should return true >>> store.delete_key("first_key") >>> # This should return false >>> store.delete_key("bad_key") get(self: torch._C._distributed_c10d.Store, arg0: str) → bytes# Retrieves the value associated with the given key in the store. If key is not present in the store, the function will wait for timeout, which is defined when initializing the store, before throwing an exception. Parameters key (str) – The function will return the value associated with this key. Returns Value associated with key if key is in the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.set("first_key", "first_value") >>> # Should return "first_value" >>> store.get("first_key") has_extended_api(self: torch._C._distributed_c10d.Store) → bool# Returns true if the store supports extended operations. multi_get(self: torch._C._distributed_c10d.Store, arg0: collections.abc.Sequence[str]) → list[bytes]# Retrieve all values in keys. If any key in keys is not present in the store, the function will wait for timeout Parameters keys (List[str]) – The keys to be retrieved from the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.set("first_key", "po") >>> store.set("second_key", "tato") >>> # Should return [b"po", b"tato"] >>> store.multi_get(["first_key", "second_key"]) multi_set(self: torch._C._distributed_c10d.Store, arg0: collections.abc.Sequence[str], arg1: collections.abc.Sequence[str]) → None# Inserts a list key-value pair into the store based on the supplied keys and values Parameters keys (List[str]) – The keys to insert. values (List[str]) – The values to insert. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.multi_set(["first_key", "second_key"], ["po", "tato"]) >>> # Should return b"po" >>> store.get("first_key") num_keys(self: torch._C._distributed_c10d.Store) → int# Returns the number of keys set in the store. Note that this number will typically be one greater than the number of keys added by set() and add() since one key is used to coordinate all the workers using the store. Warning When used with the TCPStore, num_keys returns the number of keys written to the underlying file. If the store is destructed and another store is created with the same file, the original keys will be retained. Returns The number of keys present in the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Using TCPStore as an example, other store types can also be used >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.set("first_key", "first_value") >>> # This should return 2 >>> store.num_keys() queue_len(self: torch._C._distributed_c10d.Store, arg0: str) → int# Returns the length of the specified queue. If the queue doesn’t exist it returns 0. See queue_push for more details. Parameters key (str) – The key of the queue to get the length. queue_pop(self: torch._C._distributed_c10d.Store, key: str, block: bool = True) → bytes# Pops a value from the specified queue or waits until timeout if the queue is empty. See queue_push for more details. If block is False, a dist.QueueEmptyError will be raised if the queue is empty. Parameters key (str) – The key of the queue to pop from. block (bool) – Whether to block waiting for the key or immediately return. queue_push(self: torch._C._distributed_c10d.Store, arg0: str, arg1: str) → None# Pushes a value into the specified queue. Using the same key for queues and set/get operations may result in unexpected behavior. wait/check operations are supported for queues. wait with queues will only wake one waiting worker rather than all. Parameters key (str) – The key of the queue to push to. value (str) – The value to push into the queue. set(self: torch._C._distributed_c10d.Store, arg0: str, arg1: str) → None# Inserts the key-value pair into the store based on the supplied key and value. If key already exists in the store, it will overwrite the old value with the new supplied value. Parameters key (str) – The key to be added to the store. value (str) – The value associated with key to be added to the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.set("first_key", "first_value") >>> # Should return "first_value" >>> store.get("first_key") set_timeout(self: torch._C._distributed_c10d.Store, arg0: datetime.timedelta) → None# Sets the store’s default timeout. This timeout is used during initialization and in wait() and get(). Parameters timeout (timedelta) – timeout to be set in the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Using TCPStore as an example, other store types can also be used >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> store.set_timeout(timedelta(seconds=10)) >>> # This will throw an exception after 10 seconds >>> store.wait(["bad_key"]) property timeout# Gets the timeout of the store. wait(*args, **kwargs)# Overloaded function. wait(self: torch._C._distributed_c10d.Store, arg0: collections.abc.Sequence[str]) -> None Waits for each key in keys to be added to the store. If not all keys are set before the timeout (set during store initialization), then wait will throw an exception. Parameters keys (list) – List of keys on which to wait until they are set in the store. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Using TCPStore as an example, other store types can also be used >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> # This will throw an exception after 30 seconds >>> store.wait(["bad_key"]) wait(self: torch._C._distributed_c10d.Store, arg0: collections.abc.Sequence[str], arg1: datetime.timedelta) -> None Waits for each key in keys to be added to the store, and throws an exception if the keys have not been set by the supplied timeout. Parameters keys (list) – List of keys on which to wait until they are set in the store. timeout (timedelta) – Time to wait for the keys to be added before throwing an exception. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Using TCPStore as an example, other store types can also be used >>> store = dist.TCPStore("127.0.0.1", 0, 1, True, timedelta(seconds=30)) >>> # This will throw an exception after 10 seconds >>> store.wait(["bad_key"], timedelta(seconds=10)) class torch.distributed.TCPStore# A TCP-based distributed key-value store implementation. The server store holds the data, while the client stores can connect to the server store over TCP and perform actions such as set() to insert a key-value pair, get() to retrieve a key-value pair, etc. There should always be one server store initialized because the client store(s) will wait for the server to establish a connection. Parameters host_name (str) – The hostname or IP Address the server store should run on. port (int) – The port on which the server store should listen for incoming requests. world_size (int, optional) – The total number of store users (number of clients + 1 for the server). Default is None (None indicates a non-fixed number of store users). is_master (bool, optional) – True when initializing the server store and False for client stores. Default is False. timeout (timedelta, optional) – Timeout used by the store during initialization and for methods such as get() and wait(). Default is timedelta(seconds=300) wait_for_workers (bool, optional) – Whether to wait for all the workers to connect with the server store. This is only applicable when world_size is a fixed value. Default is True. multi_tenant (bool, optional) – If True, all TCPStore instances in the current process with the same host/port will use the same underlying TCPServer. Default is False. master_listen_fd (int, optional) – If specified, the underlying TCPServer will listen on this file descriptor, which must be a socket already bound to port. To bind an ephemeral port we recommend setting the port to 0 and reading .port. Default is None (meaning the server creates a new socket and attempts to bind it to port). use_libuv (bool, optional) – If True, use libuv for TCPServer backend. Default is True. Example::>>> import torch.distributed as dist >>> from datetime import timedelta >>> # Run on process 1 (server) >>> server_store = dist.TCPStore("127.0.0.1", 1234, 2, True, timedelta(seconds=30)) >>> # Run on process 2 (client) >>> client_store = dist.TCPStore("127.0.0.1", 1234, 2, False) >>> # Use any of the store methods from either the client or server after initialization >>> server_store.set("first_key", "first_value") >>> client_store.get("first_key") __init__(self: torch._C._distributed_c10d.TCPStore, host_name: str, port: SupportsInt, world_size: SupportsInt | None = None, is_master: bool = False, timeout: datetime.timedelta = datetime.timedelta(seconds=300), wait_for_workers: bool = True, multi_tenant: bool = False, master_listen_fd: SupportsInt | None = None, use_libuv: bool = True) → None# Creates a new TCPStore. property host# Gets the hostname on which the store listens for requests. property libuvBackend# Returns True if it’s using the libuv backend. property port# Gets the port number on which the store listens for requests. class torch.distributed.HashStore# A thread-safe store implementation based on an underlying hashmap. This store can be used within the same process (for example, by other threads), but cannot be used across processes. Example::>>> import torch.distributed as dist >>> store = dist.HashStore() >>> # store can be used from other threads >>> # Use any of the store methods after initialization >>> store.set("first_key", "first_value") __init__(self: torch._C._distributed_c10d.HashStore) → None# Creates a new HashStore. class torch.distributed.FileStore# A store implementation that uses a file to store the underlying key-value pairs. Parameters file_name (str) – path of the file in which to store the key-value pairs world_size (int, optional) – The total number of processes using the store. Default is -1 (a negative value indicates a non-fixed number of store users). Example::>>> import torch.distributed as dist >>> store1 = dist.FileStore("/tmp/filestore", 2) >>> store2 = dist.FileStore("/tmp/filestore", 2) >>> # Use any of the store methods from either the client or server after initialization >>> store1.set("first_key", "first_value") >>> store2.get("first_key") __init__(self: torch._C._distributed_c10d.FileStore, file_name: str, world_size: SupportsInt = -1) → None# Creates a new FileStore. property path# Gets the path of the file used by FileStore to store key-value pairs. class torch.distributed.PrefixStore# A wrapper around any of the 3 key-value stores (TCPStore, FileStore, and HashStore) that adds a prefix to each key inserted to the store. Parameters prefix (str) – The prefix string that is prepended to each key before being inserted into the store. store (torch.distributed.store) – A store object that forms the underlying key-value store. __init__(self: torch._C._distributed_c10d.PrefixStore, prefix: str, store: torch._C._distributed_c10d.Store) → None# Creates a new PrefixStore. property underlying_store# Gets the underlying store object that PrefixStore wraps around. Profiling Collective Communication# Note that you can use torch.profiler (recommended, only available after 1.8.1) or torch.autograd.profiler to profile collective communication and point-to-point communication APIs mentioned here. All out-of-the-box backends (gloo, nccl, mpi) are supported and collective communication usage will be rendered as expected in profiling output/traces. Profiling your code is the same as any regular torch operator: import torch import torch.distributed as dist with torch.profiler(): tensor = torch.randn(20, 10) dist.all_reduce(tensor) Please refer to the profiler documentation for a full overview of profiler features. Multi-GPU collective functions# Warning The multi-GPU functions (which stand for multiple GPUs per CPU thread) are deprecated. As of today, PyTorch Distributed’s preferred programming model is one device per thread, as exemplified by the APIs in this document. If you are a backend developer and want to support multiple devices per thread, please contact PyTorch Distributed’s maintainers. Object collectives# Warning Object collectives have a number of serious limitations. Read further to determine if they are safe to use for your use case. Object collectives are a set of collective-like operations that work on arbitrary Python objects, as long as they can be pickled. There are various collective patterns implemented (e.g. broadcast, all_gather, …) but they each roughly follow this pattern: convert the input object into a pickle (raw bytes), then shove it into a byte tensor communicate the size of this byte tensor to peers (first collective operation) allocate appropriately sized tensor to perform the real collective communicate the object data (second collective operation) convert raw data back into Python (unpickle) Object collectives sometimes have surprising performance or memory characteristics that lead to long runtimes or OOMs, and thus they should be used with caution. Here are some common issues. Asymmetric pickle/unpickle time - Pickling objects can be slow, depending on the number, type and size of the objects. When the collective has a fan-in (e.g. gather_object), the receiving rank(s) must unpickle N times more objects than the sending rank(s) had to pickle, which can cause other ranks to time out on their next collective. Inefficient tensor communication - Tensors should be sent via regular collective APIs, not object collective APIs. It is possible to send Tensors via object collective APIs, but they will be serialized and deserialized (including a CPU-sync and device-to-host copy in the case of non-CPU tensors), and in almost every case other than debugging or troubleshooting code, it would be worth the trouble to refactor the code to use non-object collectives instead. Unexpected tensor devices - If you still want to send tensors via object collectives, there is another aspect specific to cuda (and possibly other accelerators) tensors. If you pickle a tensor that is currently on cuda:3, and then unpickle it, you will get another tensor on cuda:3 regardless of which process you are on, or which CUDA device is the ‘default’ device for that process. With regular tensor collective APIs, ‘output tensors’ will always be on the same, local device, which is generally what you’d expect. Unpickling a tensor will implicitly activate a CUDA context if it is the first time a GPU is used by the process, which can waste significant amounts of GPU memory. This issue can be avoided by moving tensors to CPU before passing them as inputs to an object collective. Third-party backends# Besides the builtin GLOO/MPI/NCCL backends, PyTorch distributed supports third-party backends through a run-time register mechanism. For references on how to develop a third-party backend through C++ Extension, please refer to Tutorials - Custom C++ and CUDA Extensions and test/cpp_extensions/cpp_c10d_extension.cpp. The capability of third-party backends are decided by their own implementations. The new backend derives from c10d::ProcessGroup and registers the backend name and the instantiating interface through torch.distributed.Backend.register_backend() when imported. When manually importing this backend and invoking torch.distributed.init_process_group() with the corresponding backend name, the torch.distributed package runs on the new backend. Warning The support of third-party backend is experimental and subject to change. Launch utility# The torch.distributed package also provides a launch utility in torch.distributed.launch. This helper utility can be used to launch multiple processes per node for distributed training. Module torch.distributed.launch. torch.distributed.launch is a module that spawns up multiple distributed training processes on each of the training nodes. Warning This module is going to be deprecated in favor of torchrun. The utility can be used for single-node distributed training, in which one or more processes per node will be spawned. The utility can be used for either CPU training or GPU training. If the utility is used for GPU training, each distributed process will be operating on a single GPU. This can achieve well-improved single-node training performance. It can also be used in multi-node distributed training, by spawning up multiple processes on each node for well-improved multi-node distributed training performance as well. This will especially be beneficial for systems with multiple Infiniband interfaces that have direct-GPU support, since all of them can be utilized for aggregated communication bandwidth. In both cases of single-node distributed training or multi-node distributed training, this utility will launch the given number of processes per node (--nproc-per-node). If used for GPU training, this number needs to be less or equal to the number of GPUs on the current system (nproc_per_node), and each process will be operating on a single GPU from GPU 0 to GPU (nproc_per_node - 1). How to use this module: Single-Node multi-process distributed training python -m torch.distributed.launch --nproc-per-node=NUM_GPUS_YOU_HAVE YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3 and all other arguments of your training script) Multi-Node multi-process distributed training: (e.g. two nodes) Node 1: (IP: 192.168.1.1, and has a free port: 1234) python -m torch.distributed.launch --nproc-per-node=NUM_GPUS_YOU_HAVE --nnodes=2 --node-rank=0 --master-addr="192.168.1.1" --master-port=1234 YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3 and all other arguments of your training script) Node 2: python -m torch.distributed.launch --nproc-per-node=NUM_GPUS_YOU_HAVE --nnodes=2 --node-rank=1 --master-addr="192.168.1.1" --master-port=1234 YOUR_TRAINING_SCRIPT.py (--arg1 --arg2 --arg3 and all other arguments of your training script) To look up what optional arguments this module offers: python -m torch.distributed.launch --help Important Notices: 1. This utility and multi-process distributed (single-node or multi-node) GPU training currently only achieves the best performance using the NCCL distributed backend. Thus NCCL backend is the recommended backend to use for GPU training. 2. In your training program, you must parse the command-line argument: --local-rank=LOCAL_PROCESS_RANK, which will be provided by this module. If your training program uses GPUs, you should ensure that your code only runs on the GPU device of LOCAL_PROCESS_RANK. This can be done by: Parsing the local_rank argument >>> import argparse >>> parser = argparse.ArgumentParser() >>> parser.add_argument("--local-rank", "--local_rank", type=int) >>> args = parser.parse_args() Set your device to local rank using either >>> torch.cuda.set_device(args.local_rank) # before your code runs or >>> with torch.cuda.device(args.local_rank): >>> # your code to run >>> ... Changed in version 2.0.0: The launcher will passes the --local-rank=<rank> argument to your script. From PyTorch 2.0.0 onwards, the dashed --local-rank is preferred over the previously used underscored --local_rank. For backward compatibility, it may be necessary for users to handle both cases in their argument parsing code. This means including both "--local-rank" and "--local_rank" in the argument parser. If only "--local_rank" is provided, the launcher will trigger an error: “error: unrecognized arguments: –local-rank=<rank>”. For training code that only supports PyTorch 2.0.0+, including "--local-rank" should be sufficient. 3. In your training program, you are supposed to call the following function at the beginning to start the distributed backend. It is strongly recommended that init_method=env://. Other init methods (e.g. tcp://) may work, but env:// is the one that is officially supported by this module. >>> torch.distributed.init_process_group(backend='YOUR BACKEND', >>> init_method='env://') 4. In your training program, you can either use regular distributed functions or use torch.nn.parallel.DistributedDataParallel() module. If your training program uses GPUs for training and you would like to use torch.nn.parallel.DistributedDataParallel() module, here is how to configure it. >>> model = torch.nn.parallel.DistributedDataParallel(model, >>> device_ids=[args.local_rank], >>> output_device=args.local_rank) Please ensure that device_ids argument is set to be the only GPU device id that your code will be operating on. This is generally the local rank of the process. In other words, the device_ids needs to be [args.local_rank], and output_device needs to be args.local_rank in order to use this utility 5. Another way to pass local_rank to the subprocesses via environment variable LOCAL_RANK. This behavior is enabled when you launch the script with --use-env=True. You must adjust the subprocess example above to replace args.local_rank with os.environ['LOCAL_RANK']; the launcher will not pass --local-rank when you specify this flag. Warning local_rank is NOT globally unique: it is only unique per process on a machine. Thus, don’t use it to decide if you should, e.g., write to a networked filesystem. See pytorch/pytorch#12042 for an example of how things can go wrong if you don’t do this correctly. Spawn utility# The Multiprocessing package - torch.multiprocessing package also provides a spawn function in torch.multiprocessing.spawn(). This helper function can be used to spawn multiple processes. It works by passing in the function that you want to run and spawns N processes to run it. This can be used for multiprocess distributed training as well. For references on how to use it, please refer to PyTorch example - ImageNet implementation Note that this function requires Python 3.4 or higher. Debugging torch.distributed applications# Debugging distributed applications can be challenging due to hard to understand hangs, crashes, or inconsistent behavior across ranks. torch.distributed provides a suite of tools to help debug training applications in a self-serve fashion: Python Breakpoint# It is extremely convenient to use python’s debugger in a distributed environment, but because it does not work out of the box many people do not use it at all. PyTorch offers a customized wrapper around pdb that streamlines the process. torch.distributed.breakpoint makes this process easy. Internally, it customizes pdb’s breakpoint behavior in two ways but otherwise behaves as normal pdb. Attaches the debugger only on one rank (specified by the user). Ensures all other ranks stop, by using a torch.distributed.barrier() that will release once the debugged rank issues a continue Reroutes stdin from the child process such that it connects to your terminal. To use it, simply issue torch.distributed.breakpoint(rank) on all ranks, using the same value for rank in each case. Monitored Barrier# As of v1.10, torch.distributed.monitored_barrier() exists as an alternative to torch.distributed.barrier() which fails with helpful information about which rank may be faulty when crashing, i.e. not all ranks calling into torch.distributed.monitored_barrier() within the provided timeout. torch.distributed.monitored_barrier() implements a host-side barrier using send/recv communication primitives in a process similar to acknowledgements, allowing rank 0 to report which rank(s) failed to acknowledge the barrier in time. As an example, consider the following function where rank 1 fails to call into torch.distributed.monitored_barrier() (in practice this could be due to an application bug or hang in a previous collective): import os from datetime import timedelta import torch import torch.distributed as dist import torch.multiprocessing as mp def worker(rank): dist.init_process_group("nccl", rank=rank, world_size=2) # monitored barrier requires gloo process group to perform host-side sync. group_gloo = dist.new_group(backend="gloo") if rank not in [1]: dist.monitored_barrier(group=group_gloo, timeout=timedelta(seconds=2)) if __name__ == "__main__": os.environ["MASTER_ADDR"] = "localhost" os.environ["MASTER_PORT"] = "29501" mp.spawn(worker, nprocs=2, args=()) The following error message is produced on rank 0, allowing the user to determine which rank(s) may be faulty and investigate further: RuntimeError: Rank 1 failed to pass monitoredBarrier in 2000 ms Original exception: [gloo/transport/tcp/pair.cc:598] Connection closed by peer [2401:db00:eef0:1100:3560:0:1c05:25d]:8594 TORCH_DISTRIBUTED_DEBUG# With TORCH_CPP_LOG_LEVEL=INFO, the environment variable TORCH_DISTRIBUTED_DEBUG can be used to trigger additional useful logging and collective synchronization checks to ensure all ranks are synchronized appropriately. TORCH_DISTRIBUTED_DEBUG can be set to either OFF (default), INFO, or DETAIL depending on the debugging level required. Please note that the most verbose option, DETAIL may impact the application performance and thus should only be used when debugging issues. Setting TORCH_DISTRIBUTED_DEBUG=INFO will result in additional debug logging when models trained with torch.nn.parallel.DistributedDataParallel() are initialized, and TORCH_DISTRIBUTED_DEBUG=DETAIL will additionally log runtime performance statistics a select number of iterations. These runtime statistics include data such as forward time, backward time, gradient communication time, etc. As an example, given the following application: import os import torch import torch.distributed as dist import torch.multiprocessing as mp class TwoLinLayerNet(torch.nn.Module): def __init__(self): super().__init__() self.a = torch.nn.Linear(10, 10, bias=False) self.b = torch.nn.Linear(10, 1, bias=False) def forward(self, x): a = self.a(x) b = self.b(x) return (a, b) def worker(rank): dist.init_process_group("nccl", rank=rank, world_size=2) torch.cuda.set_device(rank) print("init model") model = TwoLinLayerNet().cuda() print("init ddp") ddp_model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[rank]) inp = torch.randn(10, 10).cuda() print("train") for _ in range(20): output = ddp_model(inp) loss = output[0] + output[1] loss.sum().backward() if __name__ == "__main__": os.environ["MASTER_ADDR"] = "localhost" os.environ["MASTER_PORT"] = "29501" os.environ["TORCH_CPP_LOG_LEVEL"]="INFO" os.environ[ "TORCH_DISTRIBUTED_DEBUG" ] = "DETAIL" # set to DETAIL for runtime logging. mp.spawn(worker, nprocs=2, args=()) The following logs are rendered at initialization time: I0607 16:10:35.739390 515217 logger.cpp:173] [Rank 0]: DDP Initialized with: broadcast_buffers: 1 bucket_cap_bytes: 26214400 find_unused_parameters: 0 gradient_as_bucket_view: 0 is_multi_device_module: 0 iteration: 0 num_parameter_tensors: 2 output_device: 0 rank: 0 total_parameter_size_bytes: 440 world_size: 2 backend_name: nccl bucket_sizes: 440 cuda_visible_devices: N/A device_ids: 0 dtypes: float master_addr: localhost master_port: 29501 module_name: TwoLinLayerNet nccl_async_error_handling: N/A nccl_blocking_wait: N/A nccl_debug: WARN nccl_ib_timeout: N/A nccl_nthreads: N/A nccl_socket_ifname: N/A torch_distributed_debug: INFO The following logs are rendered during runtime (when TORCH_DISTRIBUTED_DEBUG=DETAIL is set): I0607 16:18:58.085681 544067 logger.cpp:344] [Rank 1 / 2] Training TwoLinLayerNet unused_parameter_size=0 Avg forward compute time: 40838608 Avg backward compute time: 5983335 Avg backward comm. time: 4326421 Avg backward comm/comp overlap time: 4207652 I0607 16:18:58.085693 544066 logger.cpp:344] [Rank 0 / 2] Training TwoLinLayerNet unused_parameter_size=0 Avg forward compute time: 42850427 Avg backward compute time: 3885553 Avg backward comm. time: 2357981 Avg backward comm/comp overlap time: 2234674 In addition, TORCH_DISTRIBUTED_DEBUG=INFO enhances crash logging in torch.nn.parallel.DistributedDataParallel() due to unused parameters in the model. Currently, find_unused_parameters=True must be passed into torch.nn.parallel.DistributedDataParallel() initialization if there are parameters that may be unused in the forward pass, and as of v1.10, all model outputs are required to be used in loss computation as torch.nn.parallel.DistributedDataParallel() does not support unused parameters in the backwards pass. These constraints are challenging especially for larger models, thus when crashing with an error, torch.nn.parallel.DistributedDataParallel() will log the fully qualified name of all parameters that went unused. For example, in the above application, if we modify loss to be instead computed as loss = output[1], then TwoLinLayerNet.a does not receive a gradient in the backwards pass, and thus results in DDP failing. On a crash, the user is passed information about parameters which went unused, which may be challenging to manually find for large models: RuntimeError: Expected to have finished reduction in the prior iteration before starting a new one. This error indicates that your module has parameters that were not used in producing loss. You can enable unused parameter detection by passing the keyword argument `find_unused_parameters=True` to `torch.nn.parallel.DistributedDataParallel`, and by making sure all `forward` function outputs participate in calculating loss. If you already have done the above, then the distributed data parallel module wasn't able to locate the output tensors in the return value of your module's `forward` function. Please include the loss function and the structure of the return va lue of `forward` of your module when reporting this issue (e.g. list, dict, iterable). Parameters which did not receive grad for rank 0: a.weight Parameter indices which did not receive grad for rank 0: 0 Setting TORCH_DISTRIBUTED_DEBUG=DETAIL will trigger additional consistency and synchronization checks on every collective call issued by the user either directly or indirectly (such as DDP allreduce). This is done by creating a wrapper process group that wraps all process groups returned by torch.distributed.init_process_group() and torch.distributed.new_group() APIs. As a result, these APIs will return a wrapper process group that can be used exactly like a regular process group, but performs consistency checks before dispatching the collective to an underlying process group. Currently, these checks include a torch.distributed.monitored_barrier(), which ensures all ranks complete their outstanding collective calls and reports ranks which are stuck. Next, the collective itself is checked for consistency by ensuring all collective functions match and are called with consistent tensor shapes. If this is not the case, a detailed error report is included when the application crashes, rather than a hang or uninformative error message. As an example, consider the following function which has mismatched input shapes into torch.distributed.all_reduce(): import torch import torch.distributed as dist import torch.multiprocessing as mp def worker(rank): dist.init_process_group("nccl", rank=rank, world_size=2) torch.cuda.set_device(rank) tensor = torch.randn(10 if rank == 0 else 20).cuda() dist.all_reduce(tensor) torch.cuda.synchronize(device=rank) if __name__ == "__main__": os.environ["MASTER_ADDR"] = "localhost" os.environ["MASTER_PORT"] = "29501" os.environ["TORCH_CPP_LOG_LEVEL"]="INFO" os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL" mp.spawn(worker, nprocs=2, args=()) With the NCCL backend, such an application would likely result in a hang which can be challenging to root-cause in nontrivial scenarios. If the user enables TORCH_DISTRIBUTED_DEBUG=DETAIL and reruns the application, the following error message reveals the root cause: work = default_pg.allreduce([tensor], opts) RuntimeError: Error when verifying shape tensors for collective ALLREDUCE on rank 0. This likely indicates that input shapes into the collective are mismatched across ranks. Got shapes: 10 [ torch.LongTensor{1} ] Note For fine-grained control of the debug level during runtime the functions torch.distributed.set_debug_level(), torch.distributed.set_debug_level_from_env(), and torch.distributed.get_debug_level() can also be used. In addition, TORCH_DISTRIBUTED_DEBUG=DETAIL can be used in conjunction with TORCH_SHOW_CPP_STACKTRACES=1 to log the entire callstack when a collective desynchronization is detected. These collective desynchronization checks will work for all applications that use c10d collective calls backed by process groups created with the torch.distributed.init_process_group() and torch.distributed.new_group() APIs. Logging# In addition to explicit debugging support via torch.distributed.monitored_barrier() and TORCH_DISTRIBUTED_DEBUG, the underlying C++ library of torch.distributed also outputs log messages at various levels. These messages can be helpful to understand the execution state of a distributed training job and to troubleshoot problems such as network connection failures. The following matrix shows how the log level can be adjusted via the combination of TORCH_CPP_LOG_LEVEL and TORCH_DISTRIBUTED_DEBUG environment variables. TORCH_CPP_LOG_LEVEL TORCH_DISTRIBUTED_DEBUG Effective Log Level ERROR ignored Error WARNING ignored Warning INFO ignored Info INFO INFO Debug INFO DETAIL Trace (a.k.a. All) Distributed components raise custom Exception types derived from RuntimeError: torch.distributed.DistError: This is the base type of all distributed exceptions. torch.distributed.DistBackendError: This exception is thrown when a backend-specific error occurs. For example, if the NCCL backend is used and the user attempts to use a GPU that is not available to the NCCL library. torch.distributed.DistNetworkError: This exception is thrown when networking libraries encounter errors (ex: Connection reset by peer) torch.distributed.DistStoreError: This exception is thrown when the Store encounters an error (ex: TCPStore timeout) class torch.distributed.DistError# Exception raised when an error occurs in the distributed library class torch.distributed.DistBackendError# Exception raised when a backend error occurs in distributed class torch.distributed.DistNetworkError# Exception raised when a network error occurs in distributed class torch.distributed.DistStoreError# Exception raised when an error occurs in the distributed store If you are running single node training, it may be convenient to interactively breakpoint your script. We offer a way to conveniently breakpoint a single rank: torch.distributed.breakpoint(rank=0, skip=0, timeout_s=3600)[source]# Set a breakpoint, but only on a single rank. All other ranks will wait for you to be done with the breakpoint before continuing. Parameters rank (int) – Which rank to break on. Default: 0 skip (int) – Skip the first skip calls to this breakpoint. Default: 0.

```
torch.distributed
```

**Pattern 3:** Initialization# The package needs to be initialized using the torch.distributed.init_process_group() or torch.distributed.device_mesh.init_device_mesh() function before calling any other methods. Both block until all processes have joined. Warning Initialization is not thread-safe. Process group creation should be performed from a single thread, to prevent inconsistent ‘UUID’ assignment across ranks, and to prevent races during initialization that can lead to hangs. torch.distributed.is_available()[source]# Return True if the distributed package is available. Otherwise, torch.distributed does not expose any other APIs. Currently, torch.distributed is available on Linux, MacOS and Windows. Set USE_DISTRIBUTED=1 to enable it when building PyTorch from source. Currently, the default value is USE_DISTRIBUTED=1 for Linux and Windows, USE_DISTRIBUTED=0 for MacOS. Return type bool torch.distributed.init_process_group(backend=None, init_method=None, timeout=None, world_size=-1, rank=-1, store=None, group_name='', pg_options=None, device_id=None)[source]# Initialize the default distributed process group. This will also initialize the distributed package. There are 2 main ways to initialize a process group: Specify store, rank, and world_size explicitly. Specify init_method (a URL string) which indicates where/how to discover peers. Optionally specify rank and world_size, or encode all required parameters in the URL and omit them. If neither is specified, init_method is assumed to be “env://”. Parameters backend (str or Backend, optional) – The backend to use. Depending on build-time configurations, valid values include mpi, gloo, nccl, ucc, xccl or one that is registered by a third-party plugin. Since 2.6, if backend is not provided, c10d will use a backend registered for the device type indicated by the device_id kwarg (if provided). The known default registrations today are: nccl for cuda, gloo for cpu, xccl for xpu. If neither backend nor device_id is provided, c10d will detect the accelerator on the run-time machine and use a backend registered for that detected accelerator (or cpu). This field can be given as a lowercase string (e.g., "gloo"), which can also be accessed via Backend attributes (e.g., Backend.GLOO). If using multiple processes per machine with nccl backend, each process must have exclusive access to every GPU it uses, as sharing GPUs between processes can result in deadlock or NCCL invalid usage. ucc backend is experimental. Default backend for the device can be queried with get_default_backend_for_device(). init_method (str, optional) – URL specifying how to initialize the process group. Default is “env://” if no init_method or store is specified. Mutually exclusive with store. world_size (int, optional) – Number of processes participating in the job. Required if store is specified. rank (int, optional) – Rank of the current process (it should be a number between 0 and world_size-1). Required if store is specified. store (Store, optional) – Key/value store accessible to all workers, used to exchange connection/address information. Mutually exclusive with init_method. timeout (timedelta, optional) – Timeout for operations executed against the process group. Default value is 10 minutes for NCCL and 30 minutes for other backends. This is the duration after which collectives will be aborted asynchronously and the process will crash. This is done since CUDA execution is async and it is no longer safe to continue executing user code since failed async NCCL operations might result in subsequent CUDA operations running on corrupted data. When TORCH_NCCL_BLOCKING_WAIT is set, the process will block and wait for this timeout. group_name (str, optional, deprecated) – Group name. This argument is ignored pg_options (ProcessGroupOptions, optional) – process group options specifying what additional options need to be passed in during the construction of specific process groups. As of now, the only options we support is ProcessGroupNCCL.Options for the nccl backend, is_high_priority_stream can be specified so that the nccl backend can pick up high priority cuda streams when there’re compute kernels waiting. For other available options to config nccl, See https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/api/types.html#ncclconfig-t device_id (torch.device | int, optional) – a single, specific device this process will work on, allowing for backend-specific optimizations. Currently this has two effects, only under NCCL: the communicator is immediately formed (calling ncclCommInit* immediately rather than the normal lazy call) and sub-groups will use ncclCommSplit when possible to avoid unnecessary overhead of group creation. If you want to know NCCL initialization error early, you can also use this field. If an int is provided, the API assumes that the accelerator type at compile time will be used. Note To enable backend == Backend.MPI, PyTorch needs to be built from source on a system that supports MPI. Note Support for multiple backends is experimental. Currently when no backend is specified, both gloo and nccl backends will be created. The gloo backend will be used for collectives with CPU tensors and the nccl backend will be used for collectives with CUDA tensors. A custom backend can be specified by passing in a string with format “<device_type>:<backend_name>,<device_type>:<backend_name>”, e.g. “cpu:gloo,cuda:custom_backend”. torch.distributed.device_mesh.init_device_mesh(device_type, mesh_shape, *, mesh_dim_names=None, backend_override=None)[source]# Initializes a DeviceMesh based on device_type, mesh_shape, and mesh_dim_names parameters. This creates a DeviceMesh with an n-dimensional array layout, where n is the length of mesh_shape. If mesh_dim_names is provided, each dimension is labeled as mesh_dim_names[i]. Note init_device_mesh follows SPMD programming model, meaning the same PyTorch Python program runs on all processes/ranks in the cluster. Ensure mesh_shape (the dimensions of the nD array describing device layout) is identical across all ranks. Inconsistent mesh_shape may lead to hanging. Note If no process group is found, init_device_mesh will initialize distributed process group/groups required for distributed communications behind the scene. Parameters device_type (str) – The device type of the mesh. Currently supports: “cpu”, “cuda/cuda-like”, “xpu”. Passing in a device type with a GPU index, such as “cuda:0”, is not allowed. mesh_shape (Tuple[int]) – A tuple defining the dimensions of the multi-dimensional array describing the layout of devices. mesh_dim_names (Tuple[str], optional) – A tuple of mesh dimension names to assign to each dimension of the multi-dimensional array describing the layout of devices. Its length must match the length of mesh_shape. Each string in mesh_dim_names must be unique. backend_override (Dict[int | str, tuple[str, Options] | str | Options], optional) – Overrides for some or all of the ProcessGroups that will be created for each mesh dimension. Each key can be either the index of a dimension or its name (if mesh_dim_names is provided). Each value can be a tuple containing the name of the backend and its options, or just one of these two components (in which case the other will be set to its default value). Returns A DeviceMesh object representing the device layout. Return type DeviceMesh Example: >>> from torch.distributed.device_mesh import init_device_mesh >>> >>> mesh_1d = init_device_mesh("cuda", mesh_shape=(8,)) >>> mesh_2d = init_device_mesh("cuda", mesh_shape=(2, 8), mesh_dim_names=("dp", "tp")) torch.distributed.is_initialized()[source]# Check if the default process group has been initialized. Return type bool torch.distributed.is_mpi_available()[source]# Check if the MPI backend is available. Return type bool torch.distributed.is_nccl_available()[source]# Check if the NCCL backend is available. Return type bool torch.distributed.is_gloo_available()[source]# Check if the Gloo backend is available. Return type bool torch.distributed.distributed_c10d.is_xccl_available()[source]# Check if the XCCL backend is available. Return type bool torch.distributed.is_torchelastic_launched()[source]# Check whether this process was launched with torch.distributed.elastic (aka torchelastic). The existence of TORCHELASTIC_RUN_ID environment variable is used as a proxy to determine whether the current process was launched with torchelastic. This is a reasonable proxy since TORCHELASTIC_RUN_ID maps to the rendezvous id which is always a non-null value indicating the job id for peer discovery purposes.. Return type bool torch.distributed.get_default_backend_for_device(device)[source]# Return the default backend for the given device. Parameters device (Union[str, torch.device]) – The device to get the default backend for. Returns The default backend for the given device as a lower case string. Return type str Currently three initialization methods are supported: TCP initialization# There are two ways to initialize using TCP, both requiring a network address reachable from all processes and a desired world_size. The first way requires specifying an address that belongs to the rank 0 process. This initialization method requires that all processes have manually specified ranks. Note that multicast address is not supported anymore in the latest distributed package. group_name is deprecated as well. import torch.distributed as dist # Use address of one of the machines dist.init_process_group(backend, init_method='tcp://10.1.1.20:23456', rank=args.rank, world_size=4) Shared file-system initialization# Another initialization method makes use of a file system that is shared and visible from all machines in a group, along with a desired world_size. The URL should start with file:// and contain a path to a non-existent file (in an existing directory) on a shared file system. File-system initialization will automatically create that file if it doesn’t exist, but will not delete the file. Therefore, it is your responsibility to make sure that the file is cleaned up before the next init_process_group() call on the same file path/name. Note that automatic rank assignment is not supported anymore in the latest distributed package and group_name is deprecated as well. Warning This method assumes that the file system supports locking using fcntl - most local systems and NFS support it. Warning This method will always create the file and try its best to clean up and remove the file at the end of the program. In other words, each initialization with the file init method will need a brand new empty file in order for the initialization to succeed. If the same file used by the previous initialization (which happens not to get cleaned up) is used again, this is unexpected behavior and can often cause deadlocks and failures. Therefore, even though this method will try its best to clean up the file, if the auto-delete happens to be unsuccessful, it is your responsibility to ensure that the file is removed at the end of the training to prevent the same file to be reused again during the next time. This is especially important if you plan to call init_process_group() multiple times on the same file name. In other words, if the file is not removed/cleaned up and you call init_process_group() again on that file, failures are expected. The rule of thumb here is that, make sure that the file is non-existent or empty every time init_process_group() is called. import torch.distributed as dist # rank should always be specified dist.init_process_group(backend, init_method='file:///mnt/nfs/sharedfile', world_size=4, rank=args.rank) Environment variable initialization# This method will read the configuration from environment variables, allowing one to fully customize how the information is obtained. The variables to be set are: MASTER_PORT - required; has to be a free port on machine with rank 0 MASTER_ADDR - required (except for rank 0); address of rank 0 node WORLD_SIZE - required; can be set either here, or in a call to init function RANK - required; can be set either here, or in a call to init function The machine with rank 0 will be used to set up all connections. This is the default method, meaning that init_method does not have to be specified (or can be env://). Improving initialization time# TORCH_GLOO_LAZY_INIT - establishes connections on demand rather than using a full mesh which can greatly improve initialization time for non all2all operations.

```
torch.distributed.init_process_group()
```

**Pattern 4:** Example:

```
>>> from torch.distributed.device_mesh import init_device_mesh
>>>
>>> mesh_1d = init_device_mesh("cuda", mesh_shape=(8,))
>>> mesh_2d = init_device_mesh("cuda", mesh_shape=(2, 8), mesh_dim_names=("dp", "tp"))
```

**Pattern 5:** Groups# By default collectives operate on the default group (also called the world) and require all processes to enter the distributed function call. However, some workloads can benefit from more fine-grained communication. This is where distributed groups come into play. new_group() function can be used to create new groups, with arbitrary subsets of all processes. It returns an opaque group handle that can be given as a group argument to all collectives (collectives are distributed functions to exchange information in certain well-known programming patterns). torch.distributed.new_group(ranks=None, timeout=None, backend=None, pg_options=None, use_local_synchronization=False, group_desc=None, device_id=None)[source]# Create a new distributed group. This function requires that all processes in the main group (i.e. all processes that are part of the distributed job) enter this function, even if they are not going to be members of the group. Additionally, groups should be created in the same order in all processes. Warning Safe concurrent usage: When using multiple process groups with the NCCL backend, the user must ensure a globally consistent execution order of collectives across ranks. If multiple threads within a process issue collectives, explicit synchronization is necessary to ensure consistent ordering. When using async variants of torch.distributed communication APIs, a work object is returned and the communication kernel is enqueued on a separate CUDA stream, allowing overlap of communication and computation. Once one or more async ops have been issued on one process group, they must be synchronized with other cuda streams by calling work.wait() before using another process group. See Using multiple NCCL communicators concurrently <https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently> for more details. Parameters ranks (list[int]) – List of ranks of group members. If None, will be set to all ranks. Default is None. timeout (timedelta, optional) – see init_process_group for details and default value. backend (str or Backend, optional) – The backend to use. Depending on build-time configurations, valid values are gloo and nccl. By default uses the same backend as the global group. This field should be given as a lowercase string (e.g., "gloo"), which can also be accessed via Backend attributes (e.g., Backend.GLOO). If None is passed in, the backend corresponding to the default process group will be used. Default is None. pg_options (ProcessGroupOptions, optional) – process group options specifying what additional options need to be passed in during the construction of specific process groups. i.e. for the nccl backend, is_high_priority_stream can be specified so that process group can pick up high priority cuda streams. For other available options to config nccl, See https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/api/types.html#ncclconfig-tuse_local_synchronization (bool, optional): perform a group-local barrier at the end of the process group creation. This is different in that non-member ranks don’t need to call into API and don’t join the barrier. group_desc (str, optional) – a string to describe the process group. device_id (torch.device, optional) – a single, specific device to “bind” this process to, The new_group call will try to initialize a communication backend immediately for the device if this field is given. Returns A handle of distributed group that can be given to collective calls or GroupMember.NON_GROUP_MEMBER if the rank is not part of ranks. N.B. use_local_synchronization doesn’t work with MPI. N.B. While use_local_synchronization=True can be significantly faster with larger clusters and small process groups, care must be taken since it changes cluster behavior as non-member ranks don’t join the group barrier(). N.B. use_local_synchronization=True can lead to deadlocks when each rank creates multiple overlapping process groups. To avoid that, make sure all ranks follow the same global creation order. torch.distributed.get_group_rank(group, global_rank)[source]# Translate a global rank into a group rank. global_rank must be part of group otherwise this raises RuntimeError. Parameters group (ProcessGroup) – ProcessGroup to find the relative rank. global_rank (int) – Global rank to query. Returns Group rank of global_rank relative to group Return type int N.B. calling this function on the default process group returns identity torch.distributed.get_global_rank(group, group_rank)[source]# Translate a group rank into a global rank. group_rank must be part of group otherwise this raises RuntimeError. Parameters group (ProcessGroup) – ProcessGroup to find the global rank from. group_rank (int) – Group rank to query. Returns Global rank of group_rank relative to group Return type int N.B. calling this function on the default process group returns identity torch.distributed.get_process_group_ranks(group)[source]# Get all ranks associated with group. Parameters group (Optional[ProcessGroup]) – ProcessGroup to get all ranks from. If None, the default process group will be used. Returns List of global ranks ordered by group rank. Return type list[int]

```
new_group()
```

**Pattern 6:** Warning Safe concurrent usage: When using multiple process groups with the NCCL backend, the user must ensure a globally consistent execution order of collectives across ranks. If multiple threads within a process issue collectives, explicit synchronization is necessary to ensure consistent ordering. When using async variants of torch.distributed communication APIs, a work object is returned and the communication kernel is enqueued on a separate CUDA stream, allowing overlap of communication and computation. Once one or more async ops have been issued on one process group, they must be synchronized with other cuda streams by calling work.wait() before using another process group. See Using multiple NCCL communicators concurrently <https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently> for more details.

```
NCCL
```

**Pattern 7:** Note If you are using DistributedDataParallel in conjunction with the Distributed RPC Framework, you should always use torch.distributed.autograd.backward() to compute gradients and torch.distributed.optim.DistributedOptimizer for optimizing parameters. Example: >>> import torch.distributed.autograd as dist_autograd >>> from torch.nn.parallel import DistributedDataParallel as DDP >>> import torch >>> from torch import optim >>> from torch.distributed.optim import DistributedOptimizer >>> import torch.distributed.rpc as rpc >>> from torch.distributed.rpc import RRef >>> >>> t1 = torch.rand((3, 3), requires_grad=True) >>> t2 = torch.rand((3, 3), requires_grad=True) >>> rref = rpc.remote("worker1", torch.add, args=(t1, t2)) >>> ddp_model = DDP(my_model) >>> >>> # Setup optimizer >>> optimizer_params = [rref] >>> for param in ddp_model.parameters(): >>> optimizer_params.append(RRef(param)) >>> >>> dist_optim = DistributedOptimizer( >>> optim.SGD, >>> optimizer_params, >>> lr=0.05, >>> ) >>> >>> with dist_autograd.context() as context_id: >>> pred = ddp_model(rref.to_here()) >>> loss = loss_func(pred, target) >>> dist_autograd.backward(context_id, [loss]) >>> dist_optim.step(context_id)

```
torch.distributed.autograd.backward()
```

**Pattern 8:** static_graph (bool) – When set to True, DDP knows the trained graph is static. Static graph means 1) The set of used and unused parameters will not change during the whole training loop; in this case, it does not matter whether users set find_unused_parameters = True or not. 2) How the graph is trained will not change during the whole training loop (meaning there is no control flow depending on iterations). When static_graph is set to be True, DDP will support cases that can not be supported in the past: 1) Reentrant backwards. 2) Activation checkpointing multiple times. 3) Activation checkpointing when model has unused parameters. 4) There are model parameters that are outside of forward function. 5) Potentially improve performance when there are unused parameters, as DDP will not search graph in each iteration to detect unused parameters when static_graph is set to be True. To check whether you can set static_graph to be True, one way is to check ddp logging data at the end of your previous model training, if ddp_logging_data.get("can_set_static_graph") == True, mostly you can set static_graph = True as well. Example::>>> model_DDP = torch.nn.parallel.DistributedDataParallel(model) >>> # Training loop >>> ... >>> ddp_logging_data = model_DDP._get_ddp_logging_data() >>> static_graph = ddp_logging_data.get("can_set_static_graph")

```
True
```

### Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Other documentation

Use `view` to read specific reference files when detailed information is needed.

### Working with This Skill

#### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

#### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

#### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

### Resources

#### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

#### scripts/
Add helper scripts here for common automation tasks.

#### assets/
Add templates, boilerplate, or example projects here.

### Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

### Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information


---

## Module 7: `unsloth`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\training\unsloth\SKILL.md`
- **Rôle / Objectif :** Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization

## Unsloth Skill

Comprehensive assistance with unsloth development, generated from official documentation.

### When to Use This Skill

This skill should be triggered when:
- Working with unsloth
- Asking about unsloth features or APIs
- Implementing unsloth solutions
- Debugging unsloth code
- Learning unsloth best practices

### Quick Reference

#### Common Patterns

*Quick reference patterns will be added as you use the skill.*

### Reference Files

This skill includes comprehensive documentation in `references/`:

- **llms-txt.md** - Llms-Txt documentation

Use `view` to read specific reference files when detailed information is needed.

### Working with This Skill

#### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

#### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

#### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

### Resources

#### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

#### scripts/
Add helper scripts here for common automation tasks.

#### assets/
Add templates, boilerplate, or example projects here.

### Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

### Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information

<!-- Trigger re-upload 1763621536 -->


---
