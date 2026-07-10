"""
Exercise 2 — Tool-calling agent (local port of Exercise_2_ToolAgent_Colab.ipynb).

Shared by app.py (Gradio) and exercise4_eval_harness.py (eval).
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pinecone import Pinecone
from pydantic import BaseModel, Field

load_dotenv()

# ── Config (from .env or environment) ─────────────────────────
PINECONE_INDEX = os.environ.get("PINECONE_INDEX", "story-llama")
PINECONE_NAMESPACE = os.environ.get("PINECONE_NAMESPACE", "default")
PINECONE_TEXT_FIELD = os.environ.get("PINECONE_TEXT_FIELD", "chunk_text")
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "google").lower()
GOOGLE_MODEL = os.environ.get("GOOGLE_MODEL", "gemini-2.0-flash")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
LLM_MODEL = GOOGLE_MODEL if LLM_PROVIDER == "google" else OPENAI_MODEL
TOP_K = int(os.environ.get("RETRIEVAL_TOP_K", "4"))
AGENT_PROMPT = os.environ.get(
    "AGENT_PROMPT",
    (
        "You are an educational assistant answering questions about stories in uploaded documents.\n"
        "Rules:\n"
        "- Use ONLY facts from the retrieved sources. Never invent details.\n"
        "- Give a direct answer in 2-4 sentences. Do not repeat the question or show your reasoning.\n"
        "- If multiple stories appear, answer about the one most relevant to the question.\n"
        "- If the sources do not contain the answer, say you could not find it in the document."
    ),
)

_index: Any = None
_agent: Any = None


def _require_keys() -> None:
    if not os.environ.get("PINECONE_API_KEY"):
        raise RuntimeError("PINECONE_API_KEY is not set")
    if LLM_PROVIDER == "google" and not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is not set (LLM_PROVIDER=google)")
    if LLM_PROVIDER == "openai" and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set (LLM_PROVIDER=openai)")
    if LLM_PROVIDER not in ("google", "openai"):
        raise ValueError('LLM_PROVIDER must be "google" or "openai"')


def get_index():
    global _index
    if _index is None:
        _require_keys()
        _index = Pinecone(api_key=os.environ["PINECONE_API_KEY"]).Index(PINECONE_INDEX)
    return _index


def pinecone_search(query: str, top_k: int | None = None) -> list[str]:
    k = top_k or TOP_K
    hits = get_index().search(
        namespace=PINECONE_NAMESPACE,
        query={"inputs": {"text": query}, "top_k": k},
        fields=[PINECONE_TEXT_FIELD],
    )["result"]["hits"]
    return [h["fields"][PINECONE_TEXT_FIELD] for h in hits]


class DocumentSearchInput(BaseModel):
    query: str = Field(description="Search query for story content.")

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        schema = handler(core_schema)
        schema.pop("title", None)
        for prop in schema.get("properties", {}).values():
            prop.pop("title", None)
        return schema


@tool(args_schema=DocumentSearchInput)
def document_search(query: str) -> str:
    """Search uploaded documents for story text. Call this for any question about plot, characters, ending, or moral."""
    chunks = pinecone_search(query)
    return "\n\n".join(f"Source {i+1}:\n{t}" for i, t in enumerate(chunks))


def to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return content.get("text", str(content))
    if isinstance(content, list):
        return "".join(to_text(part) for part in content)
    return str(content)


def get_llm(temperature: float = 0.1):
    if LLM_PROVIDER == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=GOOGLE_MODEL, temperature=temperature)
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=OPENAI_MODEL, temperature=temperature)


def get_agent():
    global _agent
    if _agent is None:
        _require_keys()
        _agent = create_react_agent(
            model=get_llm(),
            tools=[document_search],
            state_modifier=AGENT_PROMPT,
        )
    return _agent


def history_to_messages(history: list[dict]) -> list:
    messages = []
    for msg in history[-8:]:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg.get("role") == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages


def chat(question: str, history: list[dict] | None = None) -> str:
    sources = document_search.invoke(question)
    augmented = (
        f"Question: {question}\n\n"
        f"Retrieved sources (answer using ONLY these):\n{sources}"
    )
    messages = history_to_messages(history or [])
    messages.append(HumanMessage(content=augmented))
    result = get_agent().invoke({"messages": messages})
    return to_text(result["messages"][-1].content)
