"""
Exercise 4 — Tiny Eval Harness
==============================================================
Offline batch testing for your RAG agent.

Uses the SAME agent module as local_rag1/app.py (rag_agent.py).

Usage:
    pip install -r local_rag1/requirements.txt
    cp local_rag1/.env.example local_rag1/.env   # fill keys
    python exercise4_eval_harness.py
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "local_rag1" / ".env")
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent / "local_rag1"))

from rag_agent import (  # noqa: E402
    LLM_MODEL,
    LLM_PROVIDER,
    PINECONE_INDEX,
    chat,
    document_search,
    get_llm,
    to_text,
)

try:
    from rag_agent import _require_keys  # noqa: E402
    _require_keys()
except RuntimeError as e:
    print(f"ERROR: {e}")
    print("Create a .env with PINECONE_API_KEY and keys for your LLM_PROVIDER")
    sys.exit(1)

# ── Fixed eval set (same questions as app.py examples) ───────
EVAL_SET = [
    "What is the story about?",
    "Who are the main characters?",
    "What does the villain do?",
    "What happens at the end of the story?",
    "What is the moral of the story?",
]

JUDGE_SYSTEM = """You are grading an AI assistant's answer to a question about a document.
You are given the QUESTION, the SOURCES the assistant could retrieve, and its ANSWER.

Grade PASS if ALL of these hold:
- The answer is relevant to the question.
- Every factual claim is supported by the SOURCES (grounded).
- If the sources do not contain the answer, the assistant honestly says so (that is also a PASS).

Grade FAIL if the answer is irrelevant, empty, or contains claims not supported by the sources
(hallucination).

Reply with ONLY valid JSON: {"verdict": "PASS" | "FAIL", "reason": "one short sentence"}"""

judge_llm = get_llm(temperature=0.0)


def judge(question: str, answer: str) -> dict:
    sources = document_search.invoke(question)
    task = (
        f"QUESTION:\n{question}\n\n"
        f"SOURCES:\n{sources}\n\n"
        f"ANSWER:\n{answer}"
    )
    raw = to_text(
        judge_llm.invoke(
            [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": task}]
        ).content
    ).strip()

    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"verdict": "FAIL", "reason": f"Could not parse judge output: {raw[:80]}"}


def main():
    print("=" * 70)
    print(f"EVAL HARNESS — index '{PINECONE_INDEX}' — {LLM_PROVIDER} / {LLM_MODEL}")
    print(f"{len(EVAL_SET)} questions")
    print("=" * 70)

    results = []
    for i, q in enumerate(EVAL_SET, 1):
        print(f"\n[{i}/{len(EVAL_SET)}] {q}")
        try:
            answer = chat(q)
        except Exception as e:  # noqa: BLE001
            results.append((q, "ERROR", str(e)[:100]))
            print(f"   -> ERROR: {e}")
            continue

        verdict = judge(q, answer)
        results.append((q, verdict["verdict"], verdict["reason"]))
        print(f"   answer: {answer[:120].strip()}...")
        print(f"   -> {verdict['verdict']}: {verdict['reason']}")

    passed = sum(1 for _, v, _ in results if v == "PASS")
    total = len(results)
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    for q, v, reason in results:
        mark = "✅" if v == "PASS" else "❌"
        print(f"{mark} [{v:5}] {q}")
        if v != "PASS":
            print(f"         reason: {reason}")
    print("-" * 70)
    print(f"PASS RATE: {passed}/{total} ({100 * passed // total if total else 0}%)")

    if passed < total:
        print("\nSome checks FAILED — do not deploy until these are fixed.")
        sys.exit(1)
    print("\nAll checks passed ✓")


if __name__ == "__main__":
    main()
