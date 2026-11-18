
import asyncio
from app.services.llm_service import generate_answer

async def main():
    answer = await generate_answer(
        question="What is an HTTP GET request?",
        context="GET requests retrieve data from a server."
    )

    print(answer)

asyncio.run(main())
