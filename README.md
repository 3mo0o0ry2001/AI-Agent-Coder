# 🤖 Agentic-Python-Coder: Self-Correcting Execution Loop

An autonomous AI agent designed to bridge the gap between code generation and execution. This project implements a core concept from 2025 reasoning models: the iterative feedback loop.

## 🌟 Key Features
- **Agentic Reasoning:** Uses LLMs to generate and reflect on code logic.
- **Autonomous Execution:** Runs Python scripts locally via `subprocess`.
- **Self-Correction:** Automatically captures runtime errors and feeds them back to the model for fixing.
- **Provider Agility:** Built with a flexible architecture to switch between OpenAI, Gemini, and OpenRouter APIs.

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **Infrastructure:** OpenRouter API (Accessing Llama-3.3-70B/Gemini 2.0)
- **Concepts:** Prompt Engineering, Error Handling, Environment Management (`.env`).

## 🚀 How to Run
1. Clone the repo.
2. Add your API key to `.env`.
3. Run `python main.py`.

## 🛠️ Helper Tools

This project includes a utility script to help you find available free models on OpenRouter:

- **`utils/find_free.py`**: Run this script to get an up-to-date list of all models currently available for free on OpenRouter. This is useful for avoiding 429 (Rate Limit) errors by switching to less crowded models.

### How to run the tool:
```bash
python utils/find_free.py