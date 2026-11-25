# Nexora-AI Software Enigeering Copilot
An intelligent AI-powered enigneering copilot designed to plan , build, debug, test, and imporve software through autonomous AI agents.

## Development setup

The application has a FastAPI backend in `backend/` and a Vite/React frontend
in `frontend/`. Docker development files have not been added yet, so use the
local steps below to run the application today. Docker Desktop (or Docker
Engine with the Compose plugin) can be installed when you are ready to add
container support.

### Run locally

Open two terminals from the project root.

In the first terminal, create and activate a Python virtual environment, then
start the API:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux (use this instead of the PowerShell command):
# source .venv/bin/activate
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000
```

In the second terminal, install frontend dependencies and start Vite:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Open the Vite URL printed in the terminal (normally `http://localhost:5173`).
The API is available at `http://localhost:8000`, with interactive API docs at
`http://localhost:8000/docs`.

### Add Docker development support

To develop with Docker, add a `backend/Dockerfile`, a `frontend/Dockerfile`,
and a root `compose.yaml`. The Compose services should publish ports `8000`
and `5173`, mount the backend and frontend source folders for live reload, and
start the backend with Uvicorn's `--reload` option and the frontend with
Vite's `--host 0.0.0.0` option. The frontend container should install packages
from `package-lock.json` with `npm ci`.

The backend's default Ollama URL is `http://localhost:11434`. From inside a
container, `localhost` refers to that container, so set `OLLAMA_HOST` to the
host machine's Ollama address (for Docker Desktop, commonly
`http://host.docker.internal:11434`) in the backend container environment.
Keep credentials and other secrets in an untracked environment file; do not
copy `backend/.env` into an image.

Once those Docker files are in place, start development from the project root:

```bash
docker compose up --build
```

Stop with `Ctrl+C`; run `docker compose down` to remove the stopped containers.

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
