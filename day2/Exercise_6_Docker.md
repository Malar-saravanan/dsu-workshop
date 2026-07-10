# Exercise 6 — Containerize with Docker

**Day 2 · Slot 2 · Hands-on (~45 min)**

> Package the Gradio app into a container. HF deploy (Exercise 7) uses the same code without Docker.

---

## Part A — Read the `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag_agent.py app.py ./

ENV PINECONE_INDEX=story-llama \
    PINECONE_NAMESPACE=default \
    PINECONE_TEXT_FIELD=chunk_text \
    LLM_PROVIDER=google \
    GOOGLE_MODEL=gemini-2.0-flash \
    OPENAI_MODEL=gpt-4o-mini \
    RETRIEVAL_TOP_K=4

EXPOSE 7860

CMD ["python", "app.py"]
```

| Piece | Role |
|-------|------|
| `requirements.txt` | Same deps for local, Docker, and HF |
| `ENV ...` | Non-secret defaults (overridden by `--env-file`) |
| `.dockerignore` | Blocks `.env` from the image |
| `CMD python app.py` | Same as Exercise 5 |

API keys are **never** in the image — injected at run time via `--env-file`.

---

## Part B — Build

```bash
cd local_rag1
docker build -t rag-app .
```

---

## Part C — Run

```bash
./run_docker.sh
```

The script:

1. Finds `local_rag1/.env` (or `day2/.env` as fallback)
2. Builds `rag-app`
3. Runs with `--env-file` and port `7860`

Or manually:

```bash
docker run --rm --env-file .env -p 7860:7860 rag-app
```

Open **http://localhost:7860**

---

## Part D — Verify

Same questions as Exercise 5 — answers should match `python app.py`.

---

## Useful commands

```bash
docker ps
docker logs <container-id>
docker stop <container-id>
docker run -d --env-file .env -p 7860:7860 rag-app   # detached
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `no .env found` | `cp .env.example .env` in `local_rag1/` |
| `port is already allocated` | Stop other process on 7860 or use `-p 8000:7860` |
| Empty answers | Check `PINECONE_INDEX` in `.env` |
| Auth errors | Verify API keys in `.env` |

---

**Next:** [Exercise 7 — Hugging Face](Exercise_7_HuggingFace_Deploy.md)
