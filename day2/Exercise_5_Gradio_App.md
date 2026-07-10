# Exercise 5 — Run the Gradio Chat App Locally

**Day 2 · Slot 1–2 · Hands-on (~75 min)**

> Run the **same Exercise 2 agent** as local Python — Gradio chat UI (identical to HF deploy).

Everything lives in **`local_rag1/`**:

```
local_rag1/
├── rag_agent.py        # Agent logic (shared with eval harness)
├── app.py              # Gradio UI (local, Docker, HF)
├── requirements.txt    # Local, Docker, and HF
├── .env.example        # Template for secrets
├── upload_docs.py      # Optional ingest
├── Dockerfile          # Exercise 6
├── run_docker.sh       # Exercise 6
└── README.md           # HF Space config
```

---

## Part A — Understand the layout

### `rag_agent.py`

- Pinecone integrated search on `story-llama`
- `document_search` tool → `create_react_agent`
- Config from `.env`: `LLM_PROVIDER`, `GOOGLE_MODEL`, `PINECONE_INDEX`, etc.
- `chat(question, history)` — same as the Colab notebook

### `app.py`

| Piece | Purpose |
|-------|---------|
| `@spaces.GPU` on `respond()` | Required for HF ZeroGPU Spaces (no-op locally) |
| `gr.ChatInterface` | Chat UI with example questions |
| `if __name__ == "__main__"` | `demo.launch()` on port 7860 (local/Docker only) |

On Hugging Face, the Space imports `demo` — the `__main__` block does not run.

Use `pip install -r requirements.txt` for local, Docker, and HF (same file).

---

## Part B — Ingest your document (optional)

Skip if you already indexed in Colab Exercise 1 (`story-llama`).

```bash
cd local_rag1
cp .env.example .env
python upload_docs.py --file your_document.pdf
```

---

## Part C — Run locally

### 1. Environment

```bash
cd local_rag1
cp .env.example .env
```

Edit `.env`:

```bash
PINECONE_API_KEY=...
PINECONE_INDEX=story-llama
PINECONE_NAMESPACE=default
LLM_PROVIDER=google
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-2.0-flash
```

### 2. Install and launch

```bash
pip install -r requirements.txt
python app.py
```

### 3. Test

Open **http://localhost:7860** — try example questions and a follow-up message.

---

## Checkpoint

- [ ] Gradio UI loads at **http://localhost:7860**
- [ ] Example questions return grounded answers
- [ ] Follow-up messages use conversation history

If answers are empty, check `PINECONE_INDEX` matches your ingested index.

---

## 🔧 Your turn

1. Change `GOOGLE_MODEL` in `.env`, restart, confirm the UI description updates.
2. Re-run **Exercise 4** from `day2/`: `python exercise4_eval_harness.py`

---

**Next:** [Exercise 6 — Docker](Exercise_6_Docker.md)
