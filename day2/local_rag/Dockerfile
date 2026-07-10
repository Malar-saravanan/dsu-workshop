FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag_agent.py app.py ./

# Non-secret defaults (same as .env.example). Override at runtime via --env-file.
ENV PINECONE_INDEX=story-llama \
    PINECONE_NAMESPACE=default \
    PINECONE_TEXT_FIELD=chunk_text \
    LLM_PROVIDER=google \
    GOOGLE_MODEL=gemini-2.0-flash \
    OPENAI_MODEL=gpt-4o-mini \
    RETRIEVAL_TOP_K=4

EXPOSE 7860

CMD ["python", "app.py"]
