"""
Gradio chat UI for the RAG tool agent.

Runs locally, in Docker, and on Hugging Face Spaces (same file).
Run locally: python app.py
HF Spaces: imports demo automatically.
"""

from dotenv import load_dotenv

load_dotenv()

import gradio as gr
import spaces

from rag_agent import LLM_MODEL, LLM_PROVIDER, PINECONE_INDEX, chat


@spaces.GPU(duration=60)
def respond(message: str, history: list) -> str:
    try:
        api_history: list[dict] = []
        for turn in history:
            if isinstance(turn, dict):
                role = turn.get("role")
                content = turn.get("content", "")
                if role in ("user", "assistant") and content:
                    api_history.append({"role": role, "content": content})
            elif isinstance(turn, (list, tuple)) and len(turn) >= 2:
                user_msg, bot_msg = turn[0], turn[1]
                if user_msg:
                    api_history.append({"role": "user", "content": user_msg})
                if bot_msg:
                    api_history.append({"role": "assistant", "content": bot_msg})
        return chat(message, api_history)
    except Exception as exc:
        return (
            f"**Error:** {exc}\n\n"
            "Check HF **Settings → Variables and secrets** (same names as `.env`), "
            "then **Restart Space**."
        )


demo = gr.ChatInterface(
    fn=respond,
    title="RAG Tool Agent",
    description=(
        f"Grounded answers from Pinecone **{PINECONE_INDEX}** · "
        f"LLM: **{LLM_PROVIDER}** · model: **{LLM_MODEL}**"
    ),
    examples=[
        "What is the story about?",
        "Who are the main characters?",
        "What happens at the end of the story?",
        "What is the moral of the story?",
    ],
    cache_examples=False,
    type="messages",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
