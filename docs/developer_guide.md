# Developer Guide

Welcome to the Multi-Modal Evidence Review codebase! This guide covers setup, testing, and contribution standards.

## Project Structure

```text
hackerrank-orchestrate-june26/
├── backend/          # FastAPI application entrypoints
├── code/             # Core 10-engine Python pipeline and LLM integration
├── dataset/          # CSV requirements and image assets
├── docs/             # MkDocs documentation
├── frontend/         # Next.js React Dashboard
└── tests/            # Pytest suite
```

## Running the Application Locally

The easiest way to boot the full stack (API + Dashboard) is to use the provided PowerShell script from the root directory:

```powershell
./start.ps1
```

## Static Type Checking (MyPy)

This codebase enforces strict typing. We use `mypy` to ensure type safety across all engines. 

To run the type checker:
```bash
python -m mypy code/ --ignore-missing-imports
python -m mypy backend/ --ignore-missing-imports
```
*Note: We run them separately to prevent duplicate module collisions on `main.py`.*

## Running the Test Suite (Pytest)

We maintain a suite of 142 unit tests to ensure absolute deterministic accuracy across the 10 engines.

To run the tests:
```bash
cd code
python -m pytest tests/
```

## Adding a New VLM Provider

To integrate a new LLM (e.g., Claude 3.5 Sonnet):
1. Open `code/llm/multi_provider_client.py`.
2. Add a new conditional block in `_call_provider()`.
3. Implement the specific API wrapper logic for the new provider.
4. Update `config.py` to allow the new provider string.
