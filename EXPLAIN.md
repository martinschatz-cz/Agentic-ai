# Agentic-ai — Design Explanation

This document explains the refactor and the responsibilities of each module added to the repository.

Overview
--------

The original `local_multi_agent_manager.py` was a single notebook-exported script. The refactor splits the code into focused modules to improve maintainability, testability, and reuse.

Module responsibilities
-----------------------

- `models.py` — Contains dataclasses (`Task`, `Agent`) and `AGENT_REGISTRY`. These are plain data containers used by the manager and demos.
- `llm.py` — Encapsulates model/tokenizer loading and a `LocalLLM` class with a `generate(prompt, max_tokens)` method. The loader attempts to be robust across CPU/GPU environments.
- `manager.py` — Implements `ManagerAgent`, which: decomposes goals into tasks, executes tasks by calling the `LocalLLM`, and synthesizes results into a final answer. The orchestration logic (task dependency handling and execution loop) lives here.
- `utils.py` — Small utility functions such as `timestamped_log` for consistent logging and `safe_extract_json` for robust parsing of LLM outputs.
- `demos.py` — Example usage and a small CLI for running demos or custom goals.
- `environment.yml` — Conda environment specification for reproducible setups.

Design choices
--------------

- Dependency injection: `ManagerAgent` accepts an optional `LocalLLM` instance so you can mock or replace the LLM for testing.
- Safe parsing: LLM outputs are parsed with a helper (`safe_extract_json`) that attempts to recover JSON arrays or objects from noisy text.
- Minimal side effects: modules print logs via `timestamped_log` but avoid heavy global state.

Running locally
---------------

See `README.md` for quickstart steps including creating a Conda environment and running the demos.

Extending the project
---------------------

- Add unit tests that instantiate `ManagerAgent` with a mocked `LocalLLM` to verify decomposition, ordering, and synthesis behavior.
- Add configuration to select different model names via environment variables or a config file.
- Replace `print` logging with Python `logging` for production-grade logging and log levels.
