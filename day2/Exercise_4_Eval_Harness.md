# Exercise 4 — Build a Tiny Eval Harness

**Day 2 · Slot 1 · Hands-on (~40 min)**

> **Callback to Day 1:** Exercise 3's **Verifier** checks one answer online. This **eval harness**
> runs a **fixed batch** offline so you can catch regressions before you ship.

| | Verifier (Ex 3) | Eval harness (this exercise) |
|---|---|---|
| When | Online, per request | Offline, on demand / in CI |
| Scope | One answer | Fixed question set |
| Purpose | Guard a live response | Gate a deployment |

---

## What you'll do

Run `exercise4_eval_harness.py`, which:

1. Imports the **same agent** as `app.py` (`local_rag1/rag_agent.py`).
2. Runs **5 fixed questions** from `EVAL_SET` in the script.
3. Uses an **LLM judge** to score each answer PASS/FAIL.
4. Exits non-zero if anything fails (deploy gate).

---

## Prerequisites

- Python 3.11+
- Pinecone index `story-llama` with your document (Day 1 Colab).
- `local_rag1/.env` (copy from `local_rag1/.env.example`):

```bash
PINECONE_API_KEY=...
PINECONE_INDEX=story-llama
LLM_PROVIDER=google
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-2.0-flash
```

---

## Steps

### 1. Install dependencies

From `day2/`:

```bash
pip install -r local_rag1/requirements.txt
```

### 2. Run the harness

```bash
python exercise4_eval_harness.py
```

### 3. Read the output

```
[1/5] What is the story about?
   answer: The story follows Snow White...
   -> PASS: Answer is relevant and supported by the sources.
...
PASS RATE: 4/5 (80%)
```

Exit code `1` if any question fails.

---

## 🔧 Your turn

1. Edit `EVAL_SET` in `exercise4_eval_harness.py` — add an answerable question and one that isn't in the document.
2. Tighten `JUDGE_SYSTEM` (e.g. "FAIL if longer than 3 sentences") and re-run.
3. Use as a deploy gate: `python exercise4_eval_harness.py && echo "safe to ship"`

---

## How scoring works

No hardcoded correct answers. The judge re-retrieves sources and checks groundedness — same principle as the Exercise 3 verifier, applied offline.

---

**Next:** [Exercise 5 — Gradio App](Exercise_5_Gradio_App.md)
