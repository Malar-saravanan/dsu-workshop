# Agentic Design Patterns — The Complete List of 21

**Source:** *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems*
Antonio Gulli — Senior Director & Distinguished Engineer, Google (Office of the CTO)
Free guide (424 pages) · Published by Springer · Author royalties donated to Save the Children

---

## Part 1 — Core Patterns

| # | Pattern | What It Does |
|---|---------|---------------|
| 1 | **Prompt Chaining** | Breaks one large task into a sequence of smaller, ordered LLM calls — each step's output feeds the next |
| 2 | **Routing** | Dynamically selects which path, tool, or agent should handle a given request |
| 3 | **Parallelization** | Runs independent sub-tasks concurrently instead of sequentially, for speed |
| 4 | **Reflection** | The agent critiques and improves its own output before finalizing it |
| 5 | **Tool Use** | Lets the model call external functions, APIs, or data sources to act beyond text generation |
| 6 | **Planning** | Decomposes a goal into an ordered strategy of steps before acting |
| 7 | **Multi-Agent Collaboration** | Multiple specialized agents work together, each owning a narrow role |

## Part 2 — Advanced Patterns

| # | Pattern | What It Does |
|---|---------|---------------|
| 8 | **Memory Management** | Persists state and context across steps or sessions |
| 9 | **Learning and Adaptation** | The agent improves its behavior dynamically over time |
| 10 | **Model Context Protocol (MCP)** | A standardized interface for connecting models to tools and data |
| 11 | **Goal Setting and Monitoring** | Tracks objectives and progress throughout a task's lifecycle |

## Part 3 — Production Patterns

| # | Pattern | What It Does |
|---|---------|---------------|
| 12 | **Exception Handling and Recovery** | Detects failures and recovers gracefully instead of crashing the pipeline |
| 13 | **Human-in-the-Loop** | Routes high-stakes or ambiguous decisions to a human for approval |
| 14 | **Knowledge Retrieval (RAG)** | Retrieval-Augmented Generation — grounds answers in external documents/data |

## Part 4 — Enterprise Patterns

| # | Pattern | What It Does |
|---|---------|---------------|
| 15 | **Inter-Agent Communication (A2A)** | Standardizes how independent agents exchange messages and data |
| 16 | **Resource-Aware Optimization** | Manages compute, cost, and latency budgets across agent operations |
| 17 | **Reasoning Techniques** | Advanced decision-making strategies (e.g. chain-of-thought, tree-of-thought) |
| 18 | **Guardrails / Safety Patterns** | Constrains agent behavior to mitigate risk and prevent harmful actions |
| 19 | **Evaluation and Monitoring** | Batch-tests and tracks agent performance before and after deployment |
| 20 | **Prioritization** | Decides task order when multiple objectives compete for attention |
| 21 | **Exploration and Discovery** | Enables agents to autonomously explore and learn about unfamiliar problem spaces |

---

## Appendices (bonus material, not counted in the 21)

- **A** — Advanced Prompting Techniques
- **B** — AI Agentic: From GUI to Real-World Environment
- **C** — Quick Overview of Agentic Frameworks
- **D** — Building an Agent with AgentSpace
- **E** — AI Agents on the CLI
- **F** — Under the Hood: Reasoning Engines
- **G** — Coding Agents

---

## Where to Get the Full Book

- **Free PDF + code notebooks:** github.com/nevzat/Agentic-Design-Patterns-by-AntonioGulli
- **Print/Kindle:** Amazon — *Agentic Design Patterns* (Gulli, Springer, 2025)
- **Publisher page:** link.springer.com/book/10.1007/978-3-032-01402-3
