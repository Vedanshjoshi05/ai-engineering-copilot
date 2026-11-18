
import os
from dotenv import load_dotenv
from ollama import AsyncClient

load_dotenv()

client = AsyncClient(
    host="http://localhost:11434"
)

MODEL = os.getenv("LLM_MODEL", "qwen2.5-coder:3b")


async def generate_answer(question: str, context: str):
    prompt = f"""
You are an AI Software Engineering Assistant.

Answer the user's question using the provided repository code.

Rules:
1. Use the supplied code as your primary source.
2. Do not invent functions or implementation details.
3. If the context is insufficient, clearly say so.
4. Explain technical concepts in simple language.

Repository Context:
{context}

User Question:
{question}
"""

    response = await client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


async def ask_repository(
    owner: str,
    repo: str,
    question: str
):
    from app.services.vector_service import search_repository

    search_results = search_repository(
        owner=owner,
        repo=repo,
        query=question,
        limit=5
    )

    if not search_results["results"]:
        return {
            "answer": "No relevant code found in this repository.",
            "sources": []
        }

    context_parts = []
    sources = []

    for result in search_results["results"]:
        metadata = result["metadata"]

        context_parts.append(
            f"""
File: {metadata['file_path']}
Lines: {metadata['start_line']}-{metadata['end_line']}

Code:
{result['content']}
"""
        )

        sources.append({
            "file_path": metadata["file_path"],
            "start_line": metadata["start_line"],
            "end_line": metadata["end_line"]
        })

    context = "\n\n".join(context_parts)

    answer = await generate_answer(
        question=question,
        context=context
    )

    return {
        "repository": f"{owner}/{repo}",
        "question": question,
        "answer": answer,
        "sources": sources
    }
