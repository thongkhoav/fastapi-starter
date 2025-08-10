uv run uvicorn app.main:app --reload
uv remove passlib
uv sync
uv add passlib[bcrypt]
uv venv, .venv\Scripts\activate
