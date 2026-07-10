# Exercise 7 — Deploy to Hugging Face Spaces (Gradio, free)

**Day 2 · Slot 3 · Hands-on (~75 min)**

> Push **`local_rag1/`** to a public URL. Same code as local — no separate deploy folder.

**Why Gradio, not Docker?** Docker Spaces require HF PRO. Gradio SDK is **free**.

---

## What gets pushed

Copy these four files from `local_rag1/` into your HF Space git repo:

| File | Purpose |
|------|---------|
| `app.py` | Gradio chat UI |
| `rag_agent.py` | Agent logic |
| `requirements.txt` | Same file as local/Docker |
| `README.md` | HF Space config (`sdk: gradio`) |

**Stay local (do not push):** `.env`, `Dockerfile`, `run_docker.sh`, `upload_docs.py`, `.dockerignore`

---

## Step 1 — Account and token

1. https://huggingface.co/join
2. **Settings → Access Tokens → New token** — role **Write**
3. Save token (`hf_...`) — git password when pushing

---

## Step 2 — Create the Space

1. https://huggingface.co/new-space
2. **SDK:** Gradio → Blank
3. **Space name:** e.g. `my-rag-app`
4. **Visibility:** Public
5. **Hardware:** free option (ZeroGPU OK — `app.py` has `@spaces.GPU`)
6. Create

Public URL: `https://<username>-<space-name>.hf.space`

---

## Step 3 — Push code

```bash
git clone https://huggingface.co/spaces/<username>/my-rag-app
cd my-rag-app

cp ../local_rag1/app.py .
cp ../local_rag1/rag_agent.py .
cp ../local_rag1/requirements.txt .
cp ../local_rag1/README.md .

echo ".env" >> .gitignore

git add app.py rag_agent.py requirements.txt README.md .gitignore
git commit -m "Deploy RAG agent (Gradio)"
git push
```

Password = **write token**, not account password.

---

## Step 4 — Copy `.env` to HF secrets

**Never commit `.env`.** Add each variable as a Space secret:

**Settings → Variables and secrets → New secret**

| Secret name | Required? | Example |
|-------------|-----------|---------|
| `PINECONE_API_KEY` | Yes | from `.env` |
| `PINECONE_INDEX` | Yes | `story-llama` |
| `LLM_PROVIDER` | Yes | `google` |
| `GOOGLE_API_KEY` | Yes (if google) | from `.env` |
| `GOOGLE_MODEL` | Optional | `gemini-2.0-flash` |
| `PINECONE_NAMESPACE` | Optional | `default` |
| `OPENAI_API_KEY` | Yes (if openai) | from `.env` |

**Restart Space** after adding secrets.

---

## Step 5 — Verify

1. **Logs** → Building → **Running** (green)
2. Open `https://<username>-<space-name>.hf.space`
3. Ask: *"What is the story about?"*

Share the public URL with anyone — no HF account needed for Public Spaces.

---

## Update after local changes

```bash
cd my-rag-app
cp ../local_rag1/app.py ../local_rag1/rag_agent.py ../local_rag1/requirements.txt .
git add . && git commit -m "Update app" && git push
```

---

## Checklist

- [ ] Space **Running** (green)
- [ ] Chat UI loads
- [ ] Grounded answers work
- [ ] Secrets set — `.env` not in git
- [ ] Eval harness passes locally

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| **ZeroGPU runtime error** | Re-push latest `app.py` (has `@spaces.GPU`). Or switch to **CPU** hardware |
| `PINECONE_API_KEY is not set` | Add HF secrets, restart |
| `429` quota from Google | Wait and retry; check `GOOGLE_MODEL` |
| Build fails (`HfFolder`, `starlette`) | Ensure `requirements.txt` includes `huggingface_hub` and `starlette` pins |
| Runtime error on App tab | Check Logs traceback; usually missing secrets |
| Empty answers | Wrong `PINECONE_INDEX` secret |
| Push rejected | Use write token as password |

---

**Done:** Eval → Gradio (local) → Docker (optional) → HF Space (free).
