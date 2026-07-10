# Day 2 — Eval → Gradio → Docker → Hugging Face

Self-contained export folder. Zip `day2/` and share.

**Prerequisite:** Pinecone index `story-llama` with your document (from Day 1 Colab Exercise 1).

---

## Workshop flow

```
Eval harness  →  Local Gradio  →  Docker (optional)  →  HF Space
  (Exercise 4)     (Exercise 5)       (Ex. 6)           (Exercise 7)
```

| Step | What you do | Where |
|------|-------------|--------|
| 0. Setup | venv + `local_rag1/.env` | `day2/` |
| 1. Eval | Batch-test the agent | `exercise4_eval_harness.py` |
| 2. **Local Gradio** | `python app.py` | `local_rag1/` |
| 3. **Docker** | `./run_docker.sh` | `local_rag1/` |
| 4. **HF deploy** | Push 4 files + secrets | see Exercise 7 |

**`local_rag1/` is the only app folder** — local, Docker, and HF share the same code.

---

## Contents

```
day2/
├── README.md
├── exercise4_eval_harness.py      # Exercise 4
├── Exercise_4_Eval_Harness.md
├── Exercise_5_Gradio_App.md
├── Exercise_6_Docker.md
├── Exercise_7_HuggingFace_Deploy.md
└── local_rag1/
    ├── app.py                   # Gradio UI (local, Docker, HF)
    ├── rag_agent.py             # Agent logic
    ├── requirements.txt         # Local, Docker, and HF
    ├── README.md                # HF Space config (sdk: gradio)
    ├── .env.example             # Template → copy to .env
    ├── Dockerfile               # Exercise 6
    ├── run_docker.sh            # Exercise 6
    ├── .dockerignore
    └── upload_docs.py           # Optional ingest (skip if Colab indexed)
```

| Path | Exercise | Purpose |
|------|----------|---------|
| `exercise4_eval_harness.py` | 4 | Offline batch eval |
| `local_rag1/` | 5–7 | **Source of truth** |
| `Exercise_*_*.md` | 4–7 | Step-by-step runbooks |

---

## Quick start

### 0. Setup

```bash
cd day2
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

cp local_rag1/.env.example local_rag1/.env
# Edit local_rag1/.env — PINECONE_API_KEY, PINECONE_INDEX=story-llama,
# LLM_PROVIDER=google, GOOGLE_API_KEY, GOOGLE_MODEL=gemini-2.0-flash
```

### 1. Eval harness

```bash
pip install -r local_rag1/requirements.txt
python exercise4_eval_harness.py
```

### 2. Local Gradio

```bash
cd local_rag1
pip install -r requirements.txt
python app.py
```

Open **http://localhost:7860**

### 3. Docker (optional)

```bash
cd local_rag1
./run_docker.sh
```

Same URL — uses `local_rag1/.env` automatically.

### 4. Hugging Face

See **`Exercise_7_HuggingFace_Deploy.md`**.

Push 4 files from `local_rag1/`:

- `app.py`, `rag_agent.py`, `requirements.txt`, `README.md`

Copy `.env` values into HF **Settings → Variables and secrets** (never commit `.env`).

---

## Stack

| Layer | Value |
|-------|-------|
| Index | `story-llama` |
| Agent | `rag_agent.py` |
| UI | Gradio `ChatInterface` — `app.py` |
| LLM | `LLM_PROVIDER` + `GOOGLE_MODEL` from `.env` |
| Port | 7860 |

---

## Checkpoints

- [ ] Eval harness passes
- [ ] Gradio chat on **http://localhost:7860**
- [ ] Docker answers match `python app.py`
- [ ] HF Space **Running** — public URL works

---

## Optional — document ingestion

Skip if Pinecone already has your document.

```bash
cd local_rag1
python upload_docs.py --file your_document.pdf
```

Supported: **PDF**, **TXT**, **DOCX**
