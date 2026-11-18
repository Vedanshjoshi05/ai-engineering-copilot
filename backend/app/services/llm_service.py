
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

Your task is to explain repository code using ONLY the
provided source-code context.

STRICT RULES:
1. Never use outside knowledge to fill missing implementation details.
2.Every technical claim must be supported by the provided code.
3. Do not invent functions, classes, methods, parameters,
   execution steps, or internal behavior.
4. Do not assume that an imported library behaves in a
   particular way unless the repository code demonstrates it.
5. When explaining execution flow, follow only the calls
   that are visible in the provided source code.
6.  If an intermediate implementation is missing, explicitly
   say that the retrieved context does not show that step.
7.  Do not describe HTTP/2, retries, connection pooling,
   socket handling, or other features unless the code
   explicitly supports those claims.
8.  Mention the source filename whenever explaining an
   important implementation step.
   
OUTPUT FORMAT:

#Execution flow
Explain the verified steps in order.

#Code evidence
Mention the relevant files and functions.

#Missing Information
List implementation details that cannot be confirmed from the supplied context.


SOURCE OF CONTEXT
{context}

USER QUESTION
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
