
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
You are Nexora, an AI Software Engineering Copilot.

Answer the user's question using ONLY the repository
code provided below.

STRICT RULES:
1. Do not use outside knowledge to describe repository
   implementation.
2. Do not invent functions, classes, parameters, or features.
3. Every implementation claim must be supported by
   the supplied code.
4. If the code does not contain enough information,
   explicitly say what is missing.
5. Distinguish between what the code demonstrates
   and what cannot be verified.
6. Explain the implementation clearly with file names
   wherever relevant.
7. Do not claim a feature exists unless the context
   proves it.

Repository Context:
{context}

User Question:
{question}

Provide a clear, structured answer.
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
        limit=10
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
