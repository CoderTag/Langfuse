# Langfuse x Ollama: LLM Observability & Evaluation Demo

This repository serves as a comprehensive demonstration of how to integrate **Langfuse** (an open-source LLM engineering platform) with **Ollama** (a local LLM runner) to achieve full-stack observability, automated evaluation, and prompt management for local models like **Gemma 4**.

## 🚀 Overview

Building production-grade LLM applications requires more than just a good prompt. You need to know how your model is performing, how users are interacting with it, and how changes to your prompts affect your benchmarks. 

This demo showcases four critical patterns for modern LLM engineering:

1.  **Tracing & Observability**: Capturing traces, metadata, and context propagation using the `@observe` decorator.
2.  **User Feedback Loops**: Implementing manual user scoring to capture real-world feedback directly into Langfuse.
3.  **Dataset-Driven Benchmarking**: Running large-scale experiments against Langfuse Datasets to compare model performance.
4.  **LLM-as-a-Judge**: Automating the evaluation process by using a "Judge" LLM to grade the "Student" LLM's outputs.
5.  **Prompt Registry**: Decoupling prompt engineering from code using Langfuse's centralized Prompt Registry.

## 🛠️ Tech Stack

- **[Langfuse](https://langfuse.com/)**: Observability, tracing, and evaluation.
- **[Ollama](https://ollama.com/)**: Local LLM execution environment.
- **[Gemma 4](https://ai.google.dev/gemma)**: The primary model used for demonstrations.
- **Python**: Implementation language.
- **OpenAI Python SDK**: Used for interacting with Ollama's OpenAI-compatible API.

## 📋 Prerequisites

- Python 3.9+
- **Ollama** installed and running.
- The `gemma4-pro:latest` model pulled: `ollama pull gemma4-pro:latest`.
- A running **Langfuse** instance (either [Langfuse Cloud](https://cloud.langfuse.com) or self-hosted via Docker).

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Langfuse
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install langfuse openai python-dotenv
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your Langfuse credentials:
   ```env
   LANGFUSE_PUBLIC_KEY="pk-lf-..."
   LANGFUSE_SECRET_KEY="sk-lf-..."
   LANGFUSE_HOST="https://cloud.langfuse.com" # or your self-hosted URL
   ```

## 🧪 Demonstrations

### 1. Basic Tracing & User Feedback (`01_test_langfuse.py`)
This script demonstrates how to wrap LLM calls with `@observe()`, propagate metadata (like OS and model family), and capture manual user feedback (thumbs up/down) as a `score` in Langbase.

```bash
python 01_test_langfuse.py
```

### 2. Dataset Benchmarking (`02_experiment.py`)
Leverage Langfuse Datasets to run batch experiments. This script pulls a dataset named `Production-Benchmark` from Langfuse and runs a task against every item in the dataset, creating a traceable experiment.

```bash
python 02_experiment.py
```

### 3. Automated Evaluation with LLM-as-a-Judge (`03_judge.py`)
The "Gold Standard" of LLM testing. This script uses a second LLM call (the "Judge") to automatically grade the "Student" model's responses. It uses the `evaluators` parameter in `run_experiment` to automate the scoring process.

```bash
python 03_judge.py
```

### 4. Prompt Registry Management (`04_prompt_registry.py`)
Stop hardcoding prompts! This script demonstrates how to fetch a versioned, production-ready prompt from the Langfuse Prompt Registry, compile it with dynamic variables, and link the execution back to the specific prompt version.

```bash
python 04_prompt_registry.py
```

## 🏗️ Architecture

```mermaid
graph LR
    A[User/Script] --> B[Python App]
    B --> C[Ollama (Gemma 4)]
    B --> D[Langfuse (Tracing/Eval/Registry)]
    C --> D
```

## 📜 License

This project is licensed under the MIT License.

---
*Developed as a demonstration of modern LLM Engineering workflows.*
