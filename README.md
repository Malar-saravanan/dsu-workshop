# Day 1 Workshop — RAG → Agent → Multi-Agent

Hands-on exercises for building a **grounded research assistant**: upload a document, store it in Pinecone, and answer questions using only what's in that document.

**Instructor slides:** [`Workshop_Presentation.md`](Workshop_Presentation.md)  
**RAG concepts:** [`RAG_From_Classic_to_Agentic.md`](RAG_From_Classic_to_Agentic.md)

---

## The four notebooks

| # | File | What you build | Time (approx.) |
|---|------|----------------|----------------|
| 1 | [`Exercise_1_RAG_Colab.ipynb`](Exercise_1_RAG_Colab.ipynb) | Classic RAG — ingest PDF → Pinecone → retrieval chain → Q&A | 75 min |
| 2 | [`Exercise_2_ToolAgent_Colab.ipynb`](Exercise_2_ToolAgent_Colab.ipynb) | Tool-calling agent — `document_search` tool, agent decides when to retrieve | 40 min |
| 3 | [`Exercise_3_MultiAgent_Colab.ipynb`](Exercise_3_MultiAgent_Colab.ipynb) | Multi-agent RAG — Supervisor + research + verifier | 75 min |
| — | [`Exercise_3_Bonus_SoftwareQA_Team_Colab.ipynb`](Exercise_3_Bonus_SoftwareQA_Team_Colab.ipynb) | *(Optional)* Same Supervisor pattern — software engineer + QA team | 30 min |

Run them **in order**. Each exercise reuses the same Pinecone index and the same `document_search` retrieval pattern.

---

## The storyline

> Build a research assistant for your PhD defense — answer questions **grounded in your document**, not from the model's memory.

```
Exercise 1   PDF → chunk → embed → Pinecone → always retrieve → answer
Exercise 2   Agent decides WHEN to call document_search
Exercise 3   Supervisor routes research_agent + verifier_agent
Bonus        Same orchestration, different workers (no RAG)
```

| Exercise | Who controls retrieval |
|----------|------------------------|
| 1 — RAG chain | Nobody — always retrieves |
| 2 — Tool agent | One agent chooses |
| 3 — Multi-agent | Supervisor routes a team |

---

## Before you start

### 1. Accounts & keys

| Service | Get a key | Used for |
|---------|-----------|----------|
| [Pinecone](https://www.pinecone.io/) | Starter (free) | Vector index — Exercises 1, 2, 3 |
| [Google AI Studio](https://aistudio.google.com/apikey) | Free | Gemini LLM (default) |
| [OpenAI](https://platform.openai.com/api-keys) | Paid billing | GPT LLM (optional) |

### 2. Colab secrets

Open each notebook in [Google Colab](https://colab.research.google.com/).  
Click **Secrets** (🔑) → add secrets → toggle **Notebook access** on:

| Secret | Required when |
|--------|----------------|
| `PINECONE_API_KEY` | Exercises 1, 2, 3 |
| `GOOGLE_API_KEY` | `LLM_PROVIDER = "google"` (default) |
| `OPENAI_API_KEY` | `LLM_PROVIDER = "openai"` |

You can add both LLM keys; pick one in Step 1 of each notebook.

### 3. Choose your LLM (every notebook)

In **Step 1**, set:

```python
LLM_PROVIDER = "google"   # default — gemini-2.0-flash (free)
# LLM_PROVIDER = "openai"  # gpt-4o-mini (needs billing)
```

| Provider | Model | Secret |
|----------|-------|--------|
| `"google"` | `gemini-2.0-flash` | `GOOGLE_API_KEY` |
| `"openai"` | `gpt-4o-mini` | `OPENAI_API_KEY` |

After changing provider: **Runtime → Restart session**, then run from Step 0.

---

## Tech stack (Day 1)

| Layer | Choice |
|-------|--------|
| Platform | Google Colab |
| Vector DB | Pinecone index **`story-llama`** |
| Embeddings | Pinecone integrated `llama-text-embed-v2` |
| Namespace | `default` |
| Text field | `chunk_text` |
| LLM | Gemini or OpenAI (your choice above) |

**Note:** Retrieval always uses `story-llama` regardless of LLM provider. Only the answer model switches.

---

## Run order

### Exercise 1 — RAG Q&A

1. Step 0 — install packages  
2. Step 1 — load keys, set `LLM_PROVIDER`  
3. Step 2 — upload PDF  
4. Step 3 — ingest into `story-llama`  
5. Step 3b — test retrieval (optional)  
6. Step 4 — build chain  
7. Step 5 — ask questions  

**Checkpoint:** `Done! PDF indexed into Pinecone successfully.`

### Exercise 2 — Tool agent

Requires Exercise 1 index populated.

1. Steps 0–1 — install + keys  
2. Step 2 — `document_search` tool + agent  
3. Steps 3–4 — test + live chat  

**Checkpoint:** Agent answers story questions; skips tool for off-topic questions.

### Exercise 3 — Multi-agent RAG

Requires Exercises 1–2 concepts; same index and tool.

1. Steps 0–2 — setup (Pinecone + tool + LLM helpers)  
2. Steps 3–8 — Supervisor, condition, workers, FINISH  
3. Step 9 — orchestrator  
4. Steps 10–11 — run + experiments  

**Checkpoint:** Trace shows Supervisor → research → verifier → FINISH.

### Bonus — Software + QA team

No Pinecone. LLM key only. Same Supervisor skeleton, different domain.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `SecretNotFoundError` | Add secret in Colab 🔑; enable Notebook access; name must match exactly |
| `langchain_google_genai` not found | Re-run Step 0 `%pip install`; restart runtime |
| Pinecone / index error | Re-run Exercise 1 Step 3; confirm index name `story-llama` |
| Empty or "I don't know" answers | Index empty — re-ingest PDF in Exercise 1 |
| OpenAI `insufficient_quota` | Switch to `LLM_PROVIDER = "google"` or enable billing |
| Gemini rate limit | Use `gemini-2.0-flash-lite` in `get_llm()` |
| Wrong LLM key loaded | Match `LLM_PROVIDER` to the secret you added; restart session |

---

## What carries through all four

| Constant | Value |
|----------|-------|
| Index | `story-llama` |
| Tool | `document_search` |
| Pattern | More autonomy at each level — chain → agent → team |

---

## Related materials (optional)

| File | Purpose |
|------|---------|
| [`Workshop_Presentation.md`](Workshop_Presentation.md) | Slide deck for the 2-day workshop |
| [`RAG_From_Classic_to_Agentic.md`](RAG_From_Classic_to_Agentic.md) | RAG concept deck (classic → variants → agentic) |
| [`Exercise_1b_RAG_Skill.md`](Exercise_1b_RAG_Skill.md) | Share retrieval as a Cursor skill (`plugins/`) |
| Day 2 exercises | `Exercise_4`–`7`, `local_rag1/`, `hf-space/` — eval, FastAPI, Docker, deploy |

---

*Open `Exercise_1_RAG_Colab.ipynb` in Colab and run top to bottom.*
