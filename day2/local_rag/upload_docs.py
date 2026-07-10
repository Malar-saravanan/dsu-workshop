"""
Upload a document to Pinecone (Exercise 1 ingest — local port).

Uses Pinecone integrated embeddings (llama-text-embed-v2) — same as Colab Exercise 1.

Usage:
    python upload_docs.py --file your_document.pdf
"""

import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX", "story-llama")
PINECONE_NAMESPACE = os.environ.get("PINECONE_NAMESPACE", "default")


def main() -> None:
    if not PINECONE_API_KEY:
        print("ERROR: PINECONE_API_KEY missing in .env")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Upload a document to Pinecone")
    parser.add_argument("--file", required=True, help="PDF, TXT, or DOCX path")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--chunk-overlap", type=int, default=50)
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)

    try:
        from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from pinecone import Pinecone
    except ImportError as e:
        print(f"ERROR: {e}\nRun: pip install -r requirements.txt")
        sys.exit(1)

    ext = args.file.lower().rsplit(".", 1)[-1]
    if ext == "pdf":
        loader = PyPDFLoader(args.file)
    elif ext == "txt":
        loader = TextLoader(args.file, encoding="utf-8")
    elif ext == "docx":
        loader = Docx2txtLoader(args.file)
    else:
        print(f"ERROR: Unsupported .{ext} — use pdf, txt, or docx")
        sys.exit(1)

    docs = loader.load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap
    ).split_documents(docs)
    print(f"Loaded {len(docs)} pages · {len(chunks)} chunks")

    pc = Pinecone(api_key=PINECONE_API_KEY)
    if not pc.has_index(PINECONE_INDEX):
        print(f"Creating index {PINECONE_INDEX} …")
        pc.create_index_for_model(
            name=PINECONE_INDEX,
            cloud="aws",
            region="us-east-1",
            embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}},
        )

    index = pc.Index(PINECONE_INDEX)
    index.upsert_records(
        namespace=PINECONE_NAMESPACE,
        records=[
            {"id": f"chunk-{i}", "chunk_text": c.page_content}
            for i, c in enumerate(chunks)
        ],
    )
    print(f"Done! {len(chunks)} chunks upserted to {PINECONE_INDEX}/{PINECONE_NAMESPACE}")


if __name__ == "__main__":
    main()
