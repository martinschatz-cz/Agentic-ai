# Agentic-ai

Refactored local multi-agent manager.

Quickstart
---------

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements:

```powershell
pip install -r requirements.txt
```

3. Run the demo (basic):

```powershell
python demos.py
```

4. Run with a custom goal:

```powershell
python demos.py --goal "Explain binary search algorithm with examples"
```

Files added:
- `models.py` — dataclasses and `AGENT_REGISTRY`
- `llm.py` — `LocalLLM` wrapper for the model/tokenizer
- `manager.py` — `ManagerAgent` orchestration
- `demos.py` — demo functions and CLI
- `utils.py` — logging and helpers
- `requirements.txt` — dependencies

Conda (recommended)
-------------------

If you prefer Conda, use the provided `environment.yml` to create an environment:

```powershell
conda env create -f environment.yml
conda activate agentic-ai
```

If you need to install additional packages or prefer pip in the Conda environment, run:

```powershell
pip install -r requirements.txt
```

Design explanation
------------------

See `EXPLAIN.md` for an overview of the refactor, module responsibilities, and suggestions for extending the project.


Notes
-----
- The repository keeps the original `local_multi_agent_manager.py` for reference but the refactor uses the modular files above.
- Model loading may require significant RAM or a GPU depending on the selected model. The default model name is a small chat model identifier but adjust as needed.

Docker
------

A Dockerfile is provided to build an image that creates the Conda environment and runs the demo.

Build the image:

```powershell
docker build -t agentic-ai:latest .
```

Run the container (interactive):

```powershell
docker run --rm -it agentic-ai:latest
```

If you need GPU support you'll need to adapt the Dockerfile to include CUDA-enabled base images and use `--gpus` or the NVIDIA Container Toolkit at runtime.



