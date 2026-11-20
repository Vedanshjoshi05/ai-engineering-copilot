# Nexora-AI Software Enigeering Copilot
An intelligent AI-powered enigneering copilot designed to plan , build, debug, test, and imporve software through autonomous AI agents.

## AI Code Review

Start the Nexora backend and frontend, and run Ollama locally with the
backend's configured model (`qwen2.5-coder:3b` by default). Install the
Python review dependencies into the FastAPI environment. Install Semgrep
through pipx so it has its own Python dependencies. Ensure its executable
is on your PATH.

```bash
python -m pip install -r backend/review-requirements.txt
pipx install 'semgrep>=1.120,<2'
ollama pull qwen2.5-coder:3b
```

Open **Connect Repository**, connect a public GitHub repository, then select
**Run Code Review**. This feature works before indexing. It reviews excerpts
from up to five prioritized source files on the default branch and lists the
exact line coverage. Each finding identifies the file, line, category,
severity, analyzer, impact, and suggested fix. Python files are checked with
Tree-sitter, Ruff, Pylint, Bandit, and local Semgrep rules. Ollama with Qwen
2.5 Coder adds contextual explanations and suggestions for supported source
files. Static findings remain available if Ollama is unavailable. On Windows,
run the backend in WSL for Semgrep support. The review reads source code without
running it or modifying the repository.

The API endpoint is `POST /github/review` with a JSON body such as
`{"url":"https://github.com/owner/repository"}`.
