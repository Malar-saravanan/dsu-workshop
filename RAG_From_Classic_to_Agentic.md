# RAG: From Classic to Agentic


**Workshop mapping:**

| Concept | Hands-on |
|---------|----------|
| Classic / Naive RAG | Exercise 1 |
| Agentic RAG (tool decides when to retrieve) | Exercise 2 |
| Agentic RAG (multi-agent + verification) | Exercise 3 |

---

## The progression (one slide to anchor the talk)

```
Classic RAG          Variants (smarter retrieval)       Agentic RAG (smarter control)
───────────          ──────────────────────────       ───────────────────────────
Always retrieve  →   Rewrite · Rerank · Correct  →   Agent decides if / when / how
Fixed pipeline       Better chunks in, better out      Loops, tools, teams
Exercise 1           Concepts below                    Exercises 2 & 3
```

---

# PART 1 — CLASSIC RAG (Naive RAG)

## SLIDE — What is RAG?

**Retrieval-Augmented Generation**

- **Problem:** LLMs hallucinate and don't know your private documents
- **Idea:** Before the LLM answers, **retrieve** relevant passages from your corpus and **inject** them into the prompt
- **Promise:** Answers grounded in **your** data, not the model's training memory

```
User question
    → retrieve relevant chunks from vector DB
    → stuff chunks into prompt as "context"
    → LLM generates answer from context
```

**This workshop's Exercise 1 is classic RAG** — retrieval runs on **every** question.

---

## SLIDE — Classic RAG: the two phases

| Phase | What happens |
|-------|----------------|
| **Indexing (offline)** | Ingest documents once — load, chunk, embed, store |
| **Query (online)** | Per question — embed query, search, augment prompt, generate |

```
INDEXING (batch, once)                QUERY (per request)
──────────────────────                ────────────────────
PDF / docs                            User question
  → load text                           → embed question
  → chunk                               → similarity search (top-k)
  → embed chunks                        → build prompt + context
  → upsert to vector DB                 → LLM answer
```

---

## SLIDE — Internal technique 1: Document loading

**Goal:** Get clean text into the pipeline.

| Approach | When to use |
|----------|-------------|
| Page-level load (PDF) | Simple docs, workshops, papers |
| Structured load (HTML, JSON, DB) | Wikis, tickets, APIs |
| OCR / vision load | Scanned PDFs, slides |

**Workshop (Ex 1):** `PyPDFLoader` — one LangChain document per PDF page.

**Watch for:** headers, footers, and tables polluting chunks; encoding issues in scanned docs.

---

## SLIDE — Internal technique 2: Chunking

**Goal:** Split long documents into pieces small enough to retrieve precisely, large enough to carry meaning.

| Strategy | How it works | Trade-off |
|----------|--------------|-----------|
| **Fixed-size** | N characters/tokens per chunk | Simple; may cut mid-sentence |
| **Recursive** | Split on `\n\n`, then `\n`, then space | **Workshop default** — respects structure |
| **Semantic** | Split when embedding similarity drops | Better boundaries; more compute |
| **Parent–child** | Small chunks for search, large parent for context | Better precision + richer context |

**Key knobs:**
- `chunk_size` — bigger = more context per hit, less precise retrieval
- `chunk_overlap` — overlap preserves continuity across chunk borders

**Workshop (Ex 1):** `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`.

---

## SLIDE — Internal technique 3: Embeddings

**Goal:** Map text → dense vectors so **similar meaning** = **close vectors**.

```
"Who is the hero?"  ≈  "main character of the story"
         ↓                        ↓
    vector A                  vector B     (close in space)
```

| Choice | Notes |
|--------|-------|
| Hosted API embeddings | OpenAI `text-embedding-3-small`, etc. |
| Integrated index embeddings | **Workshop:** Pinecone `llama-text-embed-v2` embeds at upsert/search time |
| Open models | BGE, E5, Nomic — self-hosted option |

**Rule:** Query and documents must use the **same embedding model** (same vector space).

---

## SLIDE — Internal technique 4: Vector store & indexing

**Goal:** Persist chunks + vectors for fast similarity search.

```
chunk_id → { vector, text, metadata }
```

| Metadata examples | Why it matters |
|-------------------|----------------|
| `source`, `page` | Citations in answers |
| `section`, `date` | Filtered retrieval later |
| `doc_type` | Route queries to the right corpus |

**Workshop (Ex 1):** Pinecone index `story-llama`, namespace `default`, field `chunk_text`.

**Similarity metric:** cosine (most common for text embeddings).

---

## SLIDE — Vector stores: FAISS vs Chroma vs Pinecone

**All three power the same RAG step** — store embedding vectors, run similarity search. They differ in **where they run** and **who operates them**.

| | **FAISS** | **Chroma** | **Pinecone** |
|---|---|---|---|
| **What** | Search **library** (Facebook AI) | **Self-hosted** vector DB | **Managed cloud** vector DB |
| **Runs where** | In your Python process / local disk | Local, Docker, your server | Pinecone cloud (API) |
| **Setup** | `pip install faiss-cpu` + index code | `pip install chromadb` + collections | API key + create index |
| **Stores text?** | No — vectors + IDs only; you map text yourself | Yes — docs + metadata + vectors | Yes — records with metadata |
| **Persistence** | You save/load index files | Built-in (e.g. SQLite) | Managed |
| **Production API** | You build it | You operate it | Built-in HTTP API |
| **Cost** | Free (your compute) | Free locally; you host | Free tier → usage-based |

**One-liners:**
- **FAISS** — fast math engine in your notebook
- **Chroma** — SQLite-for-vectors on your laptop
- **Pinecone** — hosted search service (API key, no DB ops)

---

## SLIDE — When to use FAISS, Chroma, or Pinecone

```
Solo notebook / tiny corpus / offline?
    → FAISS or Chroma

Need persistence + metadata, still local?
    → Chroma

Workshop, team, or cloud-deployed app (Colab → FastAPI → HF)?
    → Pinecone
```

| Scenario | Pick |
|----------|------|
| Learning, one PDF, no API keys | **Chroma** or **FAISS** |
| **This workshop** (shared index, Colab + deploy) | **Pinecone** ✓ |
| FastAPI / HF Space — index already in cloud | **Pinecone** |
| Data must stay on-prem / no external API | **Chroma** or self-hosted Qdrant / pgvector |
| Custom index research, max control | **FAISS** |
| Large scale, multi-user, don't want to run vector infra | **Pinecone** (or managed Qdrant / Weaviate) |

**LangChain integration (same RAG pattern, different store):**

| Store | Typical usage |
|-------|----------------|
| FAISS | `FAISS.from_documents(docs, embeddings)` |
| Chroma | `Chroma.from_documents(docs, embeddings, persist_directory=...)` |
| Pinecone | `PineconeVectorStore` or Pinecone SDK (**workshop uses SDK** + integrated `llama-text-embed-v2`) |

**Workshop choice:** Pinecone so every student searches the same `story-llama` index from Colab, and Day 2 FastAPI/HF can call the same index without shipping a local DB.

---

## SLIDE — Internal technique 5: Retrieval

**Goal:** Given a question, return the top-k most relevant chunks.

| Method | Idea |
|--------|------|
| **Dense retrieval** | Embed query → nearest neighbors in vector DB (**classic default**) |
| **Sparse retrieval** | BM25 / keyword match — strong on exact terms |
| **Hybrid** | Combine dense + sparse (variant — see Part 2) |
| **MMR** | Maximal Marginal Relevance — diverse results, less redundancy |

**Knobs:**
- `top_k` — more chunks = more context, but noise and token cost rise
- **Score threshold** — return nothing if best match is too weak ("I don't know")

**Workshop (Ex 1):** Pinecone integrated search, `top_k=4`.

---

## SLIDE — Internal technique 6: Augmentation (prompt)

**Goal:** Tell the LLM to answer **only** from retrieved context.

**Typical template:**
```
System: Answer using the context below. If the answer is not in the context, say you don't know.

Context:
{retrieved chunks}

Chat history:
{optional memory}

User: {question}
```

| Technique | Purpose |
|-----------|---------|
| Context stuffing | Concatenate top-k chunks into `{context}` |
| Citation prompt | Ask model to quote source numbers |
| Strict grounding rule | Reduces hallucination when doc doesn't contain answer |

**Workshop (Ex 1):** system prompt + `MessagesPlaceholder` for chat history (last 4 turns).

---

## SLIDE — Internal technique 7: Generation

**Goal:** LLM produces the final natural-language answer.

- Temperature ~0–0.3 for factual Q&A
- Output parser for plain text (or structured JSON if needed)
- **Grounding check** is *not* built into naive RAG — that's why variants and agentic RAG add verification

**Workshop (Ex 1):** Gemini `gemini-2.0-flash` via LCEL chain: `prompt | llm | StrOutputParser`.

---

## SLIDE — Classic RAG: strengths & limits

**Strengths**
- Simple to build and debug
- Fast path to grounded Q&A on private docs
- Predictable: same pipeline every time

**Limits**
| Limit | Symptom |
|-------|---------|
| Always retrieves | Wastes tokens on "Hello" or general knowledge questions |
| Single retrieval pass | Misses info spread across many chunks |
| Chunk quality = ceiling | Bad splits → bad answers, no recovery |
| No self-correction | Model may still hallucinate despite context |
| Static pipeline | Can't adapt strategy per question type |

**Bridge line:** *"Variants fix retrieval. Agentic RAG fixes control."*

---

# PART 2 — RAG VARIANTS (2–3 stepping stones)

Three widely used evolutions beyond naive RAG. You don't need all three in production — teach them as **design options**.

---

## SLIDE — Variant 1: Advanced RAG

**Idea:** Keep the fixed pipeline, but make **each stage smarter**.

```
Question
  → [Query transformation]   rewrite / expand / decompose
  → [Retrieval]              dense · hybrid · filtered
  → [Post-retrieval]         rerank · compress · dedupe
  → [Generation]
```

| Technique | What it fixes |
|-----------|---------------|
| **Query rewriting** | Vague user question → better search query |
| **Multi-query** | Generate 3 paraphrases → union of results |
| **HyDE** | LLM drafts a hypothetical answer → embed *that* for search |
| **Hybrid search** | Dense + BM25 — exact terms + semantic meaning |
| **Reranking** | Cross-encoder scores (query, chunk) pairs; reorder top-k |
| **Context compression** | Summarize chunks before stuffing — fit more signal in token budget |

**When to pick it:** Same architecture as Ex 1, but accuracy plateaus — tune retrieval before adding agents.

---

## SLIDE — Variant 2: Corrective RAG (CRAG)

**Idea:** After retrieval, **grade** whether the chunks are actually relevant. If not, **correct** (re-search or web fallback).

```
Retrieve top-k
    → relevance grader (LLM or classifier)
         ├─ RELEVANT     → generate answer
         ├─ AMBIGUOUS    → refine query + retrieve again
         └─ IRRELEVANT   → fallback (web, different corpus, or "can't answer")
```

| Stage | Role |
|-------|------|
| Retrieval | Initial candidate chunks |
| **Evaluation** | "Do these chunks answer the question?" |
| **Correction** | New query, different source, or abstain |

**When to pick it:** Noisy corpora, mixed-quality uploads, or when false retrieval hurts trust.

**Workshop link:** Exercise 3's **verifier_agent** is the same *spirit* — check before you ship the answer (online, per request).

---

## SLIDE — Variant 3: Self-RAG

**Idea:** The model **reflects** during generation — decide if it needs retrieval, if the draft is supported, if utility is high.

```
For each step the LLM can emit control tokens / decisions:
  [Retrieve?]  yes / no
  [Is passage relevant?]  relevant / irrelevant
  [Is generation supported?]  fully / partially / no
  [Utility score]  1–5
```

**Loop:** retrieve → generate partial answer → self-critique → maybe retrieve again → finalize.

| vs Advanced RAG | vs CRAG |
|-----------------|---------|
| Reflection is **inside** the generation loop | CRAG grades **retrieval**; Self-RAG grades **retrieval + generation** |
| More adaptive per token/step | More explicit retrieve-then-fix graph |

**When to pick it:** High-stakes answers where one-pass RAG isn't enough; research assistants, legal, medical (with human review).

---

## SLIDE — Variants at a glance

| | Naive RAG (Ex 1) | Advanced RAG | CRAG | Self-RAG |
|---|---|---|---|---|
| Pipeline shape | Fixed linear | Fixed, enriched stages | Retrieve → grade → correct | Reflective loops |
| Retrieval passes | 1 | 1 (smarter) | 1+ | 0–many (adaptive) |
| Failure handling | Hope context is enough | Rerank / compress | Explicit correction | Self-critique |
| Complexity | Low | Medium | Medium–high | High |
| **Workshop** | **Exercise 1** | Concept | Verifier idea → **Ex 3** | Agent loops → **Ex 2–3** |

---

# PART 3 — AGENTIC RAG (latest)

## SLIDE — What is Agentic RAG?

**Idea:** Don't hard-code "always retrieve." Give an **agent** (or team) **tools** and **control flow** to decide:

- **Whether** to retrieve
- **What** to search for
- **How many times** to retrieve
- **Whether** the answer is good enough

```
Classic:   question ──→ retrieve ──→ answer     (fixed)

Agentic:   question ──→ agent reasons ──→ [tool: search] ──→ observe ──→ maybe search again ──→ answer
```

**Agentic RAG = RAG + agent harness** (perceive → act → observe → repeat).

---

## SLIDE — Agentic RAG pattern A: Tool-calling RAG

**One agent, retrieval as an optional tool.**

| Component | Role |
|-----------|------|
| LLM | Reasons about the question |
| `@tool document_search` | Retrieves from vector DB when needed |
| Agent loop | `create_react_agent` — perceive / act / observe |

```
User: "What is the story about?"
  → Agent calls document_search("story plot summary")
  → Reads chunks
  → Answers grounded in sources

User: "What's the capital of France?"
  → Agent answers from general knowledge
  → Skips document_search
```

**Workshop:** **Exercise 2** — same `story-llama` index, agent **chooses** when to retrieve.

**Upgrade path from Ex 1:** Wrap `retrieve()` in `@tool`; swap chain for agent.

---

## SLIDE — Agentic RAG pattern B: Multi-step / iterative retrieval

**Agent retrieves multiple times with refined queries** (manual ReAct or graph loop).

```
Question → search("main characters") → partial answer
        → search("character relationships") → merge
        → search("ending") → finalize
```

| Use when | Example |
|----------|---------|
| Answer spans many sections | Long thesis, policy manuals |
| First retrieval is too narrow | Complex multi-part questions |
| Comparison questions | "Compare X and Y in the document" |

**Implementation options:** LangGraph loops, planner node, or supervisor instructions ("search again with …").

---

## SLIDE — Agentic RAG pattern C: Multi-agent RAG

**Separation of duties — specialists + coordinator.**

```
Supervisor (routes)
    ├─ research_agent   → calls document_search, drafts answer
    ├─ verifier_agent   → checks groundedness (APPROVED / NEEDS_REVISION)
    └─ FINISH           → final answer to user
```

| Role | Why separate |
|------|----------------|
| Researcher | Optimized for finding and synthesizing |
| Verifier | Optimized for catching unsupported claims |
| Supervisor | Workflow — no worker grades its own homework |

**Workshop:** **Exercise 3** — same `document_search` tool as Ex 2; adds **online verification** before FINISH.

**Link to CRAG / Self-RAG:** Verifier ≈ relevance + support grading, but routed through a **team** instead of a single reflective model.

---

## SLIDE — Agentic RAG pattern D: Adaptive routing (optional depth)

**Router picks the right RAG strategy per question** (common in production platforms).

```
                    ┌─→ no retrieval (chitchat / general knowledge)
User question ── Router ─┼─→ single-shot RAG (simple factual)
                    ├─→ multi-step agentic RAG (complex)
                    └─→ SQL / API tool (structured data, not vectors)
```

**Examples:** LangGraph routers, Flowise conditions, enterprise "question type" classifiers.

---

## SLIDE — Classic → Variants → Agentic (full map)

```
                    CLASSIC RAG (Ex 1)
                    ─────────────────
                    load → chunk → embed → store
                    query → retrieve → prompt → generate

                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
      ADVANCED RAG       CRAG           SELF-RAG
      smarter stages     grade + fix     reflect + loop
           │               │               │
           └───────────────┴───────────────┘
                           │
                           ▼
                    AGENTIC RAG
                    ───────────
                    Ex 2: tool decides WHEN
                    Ex 3: team verifies WHAT
                    + iterative / routing in production
```

---

## SLIDE — What we build in this workshop

| Day 1 exercise | RAG type | Key idea |
|----------------|----------|----------|
| **Exercise 1** | Classic / Naive RAG | Always retrieve; learn ingest + chain |
| **Exercise 2** | Agentic RAG (tool) | Agent decides **if** to retrieve |
| **Exercise 3** | Agentic RAG (multi-agent) | Team drafts + **verifies** before answer |
| **Exercise 4** (Day 2) | Eval gate | Offline batch check before deploy |

**One index (`story-llama`), one tool (`document_search`), escalating control.**

---

## SLIDE — Choosing the right RAG level

| Situation | Start with |
|-----------|------------|
| First prototype on one PDF | **Classic RAG** (Ex 1) |
| Users ask off-topic or general questions | **Agentic tool RAG** (Ex 2) |
| High stakes, need trust / citations | **+ Verifier or CRAG-style check** (Ex 3) |
| Retrieval quality is weak | **Advanced RAG** (rerank, hybrid, query rewrite) |
| Shipping to production | **Ex 2 agent + Day 2 eval harness** |

**Practical rule:** Master classic internals first → add one variant technique that fixes your worst failure mode → add agency only when the pipeline needs **decisions**, not just **better search**.

---

# APPENDIX — PPT slide order (suggested ~20 min concept block)

Use before Exercise 1 or split across the morning:

| # | Slide topic |
|---|-------------|
| 1 | What is RAG? |
| 2 | Classic RAG: two phases |
| 3 | Technique: chunking |
| 4 | Technique: embeddings + vector store |
| 4b | FAISS vs Chroma vs Pinecone — when to use what |
| 5 | Technique: retrieval + augmentation |
| 6 | Classic strengths & limits |
| 7 | Variant: Advanced RAG |
| 8 | Variant: CRAG |
| 9 | Variant: Self-RAG |
| 10 | Variants comparison table |
| 11 | What is Agentic RAG? |
| 12 | Pattern A: Tool-calling (→ Ex 2) |
| 13 | Pattern C: Multi-agent (→ Ex 3) |
| 14 | Full evolution map |
| 15 | Workshop build summary |

---

*Pairs with `Workshop_Presentation.md` (overall agenda) and Day 1 Colab notebooks.*
