# Exercise 1b — Build & Share a RAG Plugin (Cursor Skill)

**Prerequisites:** Pinecone index already populated (`story-llama` from Exercise 1, or your own index).

**Time:** ~25 minutes  
**Artifact:** `plugins/story-llama-rag/` → installed at `.cursor/skills/story-llama-rag/`

---

## What you are building

A **shareable plugin folder** — not a new vector DB. It contains:

- `SKILL.md` — tells Cursor **when** and **how** to search
- `config.yaml` — index name, namespace, field (no secrets)
- `scripts/search.py` — one command to retrieve context

---

## Step 1 — Test the plugin

```bash
export PINECONE_API_KEY="your-key"
cd plugins/story-llama-rag
pip install pinecone pyyaml
python scripts/search.py "What is the story about?"
```

**Checkpoint:** You see `--- Source 1 ---` blocks with text from your index.

---

## Step 2 — Install into Cursor (showcase)

From `workshop_exercises/`:

```bash
chmod +x plugins/install-to-cursor.sh
./plugins/install-to-cursor.sh story-llama-rag
```

This copies the plugin to `.cursor/skills/story-llama-rag/` so Cursor Agent can use it in this project.

**Personal install (optional):** copy to `~/.cursor/skills/story-llama-rag/` for all projects.

---

## Step 3 — Use in Cursor Agent

1. Ensure `PINECONE_API_KEY` is in your shell environment (or Cursor env)
2. Open Agent chat in this project
3. Ask: *"Using the story RAG plugin, who are the main characters?"*
4. Agent should run `search.py` and answer from sources only

**Your turn:** Ask something **not** in the document — agent should not hallucinate plot details.

---

## Step 4 — Share the plugin

```bash
cd plugins
zip -r story-llama-rag.zip story-llama-rag/
```

Send the zip. Teammate:

1. Unzips to `~/.cursor/skills/story-llama-rag/`
2. Sets `PINECONE_API_KEY`
3. Uses the same index (shared team index) or edits `config.yaml`

---

## Step 5 — Create a second plugin (template)

```bash
cp -R plugins/_template/story-llama-rag plugins/my-corpus-rag
mkdir -p plugins/my-corpus-rag/scripts
cp plugins/story-llama-rag/scripts/search.py plugins/my-corpus-rag/scripts/
```

Edit `config.yaml` and `SKILL.md` for your index. Run `./plugins/install-to-cursor.sh my-corpus-rag`.

---

## How this relates to Exercise 2

| | Exercise 1b (plugin) | Exercise 2 (Colab) |
|---|---|---|
| Where | Cursor IDE | Google Colab |
| Retrieval | `search.py` script | `@tool document_search` |
| Agent | Cursor Agent | `create_react_agent` |
| Share | Zip plugin folder | Share notebook |

Same Pinecone index. Different harness — skill for IDE, tool for Colab.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `PINECONE_API_KEY is not set` | `export PINECONE_API_KEY=...` |
| No matches | Re-run Exercise 1 ingest or check `config.yaml` index/namespace |
| Skill not picked up | Re-run `install-to-cursor.sh`; reload Cursor window |
| `ModuleNotFoundError` | `pip install pinecone pyyaml` |
