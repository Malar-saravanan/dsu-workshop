# RAG Skill — Design Document (skills-only, v1)

**Status:** Phase 1 implemented (`plugins/` + `.cursor/skills/`)  
**Scope:** Share **Cursor skills** that connect to an **existing** Pinecone index — retrieval only. No ingest, no MCP, no LangChain tool harness in v1.

**Assumption:** Index and vectors **already exist** (e.g. workshop `story-llama` from Exercise 1, or your pre-built corpus). The skill is a **pointer + search recipe**, not a data pipeline.

**Deferred (see appendix):** Full `rag_harness` package, MCP server, `@tool` plugin registry — useful later, too heavy for now.

**Fits workshop arc:** Ex 1 ingest (once) → **RAG skill (share)** → Ex 2–3 agents (unchanged, inline `@tool` in Colab)

---

## 1. Problem (simplified)

You have a Pinecone index. You want teammates to **use the same RAG retrieval** in Cursor without:

- Copy-pasting Pinecone boilerplate into every chat
- Building MCP servers or agent tool frameworks
- Re-running ingest or shipping embeddings in a zip

**v1 goal:** A **skill folder** you zip and share. Recipient adds `PINECONE_API_KEY`, drops the folder into Cursor skills, and the agent knows **when** and **how** to search your index.

---

## 2. What we are building (one sentence)

> **A RAG skill = `SKILL.md` + minimal config + optional `search.py` script** that queries your existing index and returns context for grounded answers.

Not a plugin runtime. Not MCP. **Just a shareable skill.**

---

## 3. Architecture (two layers only)

```
┌──────────────────────────────────────────┐
│  CURSOR AGENT                             │
│  Reads SKILL.md → decides when to RAG     │
│  Runs scripts/search.py OR inline snippet   │
└────────────────────┬─────────────────────┘
                     │ PINECONE_API_KEY (env)
                     │ config.yaml (index name, namespace, field)
┌────────────────────▼─────────────────────┐
│  EXISTING PINECONE INDEX (already built)  │
│  story-llama · default · chunk_text       │
└──────────────────────────────────────────┘
```

| Layer | You already have | Skill provides |
|-------|------------------|----------------|
| Data | Vectors + text in Pinecone | Index name, namespace, field, `top_k` |
| Access | `PINECONE_API_KEY` in env | Instructions to read env, never commit keys |
| Behavior | — | When to search, how to format context, grounding rules |

---

## 4. Plugin folder layout (shareable unit)

```
plugins/<plugin-id>/
├── SKILL.md              # Required — Cursor skill (trigger + workflow)
├── config.yaml           # Index pointer (no secrets)
├── scripts/
│   └── search.py         # Query → printed context
└── README.md             # How to install & share
```

**Share:** Zip `plugins/story-llama-rag/` → recipient unzips to `~/.cursor/skills/`

**Showcase in this repo:** `./plugins/install-to-cursor.sh story-llama-rag` → `.cursor/skills/story-llama-rag/`

---

## 5. `config.yaml` (minimal pointer to your index)

```yaml
# No API keys here — env only
index: story-llama
namespace: default
text_field: chunk_text
embed_model: llama-text-embed-v2   # Pinecone integrated embed at query time
top_k: 4
```

**Your case:** You already created the index — edit only these fields if your names differ.

---

## 6. `SKILL.md` (core of v1)

```markdown
---
name: story-llama-rag
description: >-
  Search the workshop story in Pinecone index story-llama. Use when the user
  asks about the story document, characters, plot, events, or moral — not for
  general knowledge unrelated to the document.
---

# Story RAG Skill

## Prerequisites
- `PINECONE_API_KEY` set in environment (never in this repo)
- Index `story-llama` already populated (Exercise 1 or shared team index)

## When to use
- Question is about content **inside** the indexed document
- User wants a **grounded** answer with sources

## When NOT to use
- General knowledge (e.g. capital of France)
- User is editing code unrelated to the document

## How to retrieve
1. Read `config.yaml` in this skill folder for index, namespace, field, top_k
2. Run from skill directory:
   ```bash
   python scripts/search.py "user question here"
   ```
3. Use the printed **Source 1, Source 2, …** blocks as context
4. Answer **only** from those sources; if missing, say you don't know

## Grounding rule
Do not invent facts not present in search output.
```

**This is the entire “plugin” in v1** — instructions the agent follows, plus an optional script.

---

## 7. `scripts/search.py` (optional, ~30 lines)

Purpose: Agent (or human) runs one command; no notebook, no harness.

```python
# Pseudocode — implement in Phase 1
# - load config.yaml from parent dir
# - read PINECONE_API_KEY from os.environ
# - Pinecone().Index(name).search(namespace, query inputs, fields)
# - print "Source i:\n{text}\n" for each hit
# - exit 1 if key missing or zero hits (optional)
```

**Why a script:** Gives deterministic retrieval without teaching MCP or `@tool` in the same exercise. Agent uses Shell tool → reads output → answers.

**Alternative (no script):** SKILL.md embeds a **copy-paste Python snippet** — even lighter, but easier to drift. Script is recommended for sharing.

---

## 8. What we are NOT building (v1)

| Out of scope now | Why |
|------------------|-----|
| MCP server | Extra protocol, auth, deployment |
| LangChain `@tool` / `create_react_agent` in skill | Stays in Colab Ex 2–3 |
| `rag_harness` Python package | Registry, connectors — Phase 2+ |
| `manifest.yaml` + `plugin.py` | Full plugin contract — appendix only |
| Ingest / chunk / embed in skill | Index already exists |
| FastAPI / Docker wiring | Day 2 separate track |

Colab exercises **keep** inline `document_search` — the skill is for **Cursor sharing**, not replacing Ex 2–3 code.

---

## 9. Workshop exercise (proposed)

### **Exercise 1b — Build & Share a RAG Skill** (optional, ~25 min)

| Step | Activity |
|------|----------|
| 0 | Confirm index works (Ex 1 Step 3b or your existing index) |
| 1 | Open `skills/_template/story-llama-rag/` |
| 2 | Set `config.yaml` to your index (already done for workshop) |
| 3 | Run `python scripts/search.py "What is the story about?"` |
| 4 | Install skill in Cursor; ask a document question in Agent mode |
| 5 | **Your turn:** Copy folder → rename skill → change `config.yaml` for a second index |

**Checkpoint:** Search script returns sources; Cursor agent uses skill for a grounded answer.

**Placement:** After Ex 1 (index exists) or as a parallel “IDE track” — does not block Ex 2–3.

---

## 10. Sharing workflow

```
Author                          Recipient
──────                          ──────────
Has Pinecone index populated    Has PINECONE_API_KEY
Creates skills/my-corpus-rag/     Receives zip (skill folder only)
  SKILL.md + config.yaml          Unzips to ~/.cursor/skills/
  scripts/search.py               Same index name OR author shares
Zips & shares                     team index / re-points config.yaml
```

**What travels in the zip:** Skill folder only (~3 files). **Not** PDFs, not vectors, not API keys.

**Team pattern:** One shared Pinecone index + same `config.yaml` in every skill copy.

---

## 11. Security

| Rule | Detail |
|------|--------|
| No secrets in skill | `PINECONE_API_KEY` from env only |
| `config.yaml` is safe to commit | Index **names** are not secret |
| Query via Pinecone SDK | User question passed as API parameter — no shell injection in script if using argv/list |
| Fail closed | Script exits with clear message if key or index missing |

---

## 12. Mapping to workshop

| Artifact | Role with skills-only design |
|----------|------------------------------|
| Exercise 1 | Creates index (one-time) — **unchanged** |
| **Exercise 1b (new)** | Build / install / share RAG skill |
| Exercise 2–3 | Colab agents + `@tool` — **unchanged** |
| `RAG_From_Classic_to_Agentic.md` | Concept deck — **unchanged** |
| Day 2 FastAPI | Separate — can later read same `config.yaml` |

---

## 13. Phase 1 implementation checklist

- [x] `plugins/story-llama-rag/` (SKILL.md, config.yaml, search.py, README.md)
- [x] `plugins/_template/story-llama-rag/` copy template
- [x] `plugins/install-to-cursor.sh` → `.cursor/skills/`
- [x] `Exercise_1b_RAG_Skill.md`
- [x] `plugins/README.md`
- [ ] Smoke test with live `PINECONE_API_KEY` (run locally when key is set)

**Not in Phase 1:** harness package, MCP, plugin registry, Ex 2 refactor.

---

## 14. Success criteria

1. Explain: skill = **behavior + index pointer**, not a vector database
2. Share a skill zip without secrets or document files
3. Recipient retrieves from **existing** index with one script command
4. Relate to agentic RAG: skill ≈ “how an IDE agent does retrieval”; Ex 2 ≈ “how a Colab agent does retrieval”

---

## 15. One-slide summary

**RAG Skill (v1)**

- Index **already exists** — skill does not ingest
- **Share:** `SKILL.md` + `config.yaml` + `search.py`
- **Use:** Cursor agent searches Pinecone when document questions arise
- **Skip for now:** MCP, tool harness, Python plugin package

---

## Appendix — Full plugin + harness design (deferred)

The earlier **plugin registry + `rag_harness` + LangChain tool wiring** design remains a valid **Phase 2** when you want:

- Colab and Cursor to share one Python package
- Multiple corpora loaded as tools in one agent
- FastAPI loading plugins from a folder

Until then, **skills-only** gives you shareability with minimal moving parts.

*Related file: same folder, implementation follows Phase 1 checklist above.*

---

*Next step when approved: create `skills/_template/story-llama-rag/` and `Exercise_1b_RAG_Skill.md`.*
