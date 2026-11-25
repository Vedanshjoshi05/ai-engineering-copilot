import asyncio
import re
from urllib.parse import urlsplit

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.review_service import review_repository

router = APIRouter(prefix="/github", tags=["Code Review"])


class ReviewRequest(BaseModel):
    url: str = Field(max_length=500)


@router.post("/review")
async def review_github_repository(request: ReviewRequest):
    try:
        url = urlsplit(request.url.strip())
    except ValueError:
        raise HTTPException(400, "Enter a public GitHub repository URL.") from None

    path = re.fullmatch(r"/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)/?", url.path)
    if (
        url.scheme != "https"
        or url.netloc.lower() not in {"github.com", "www.github.com"}
        or not path
        or url.query
        or url.fragment
        or path[2].removesuffix(".git") in {"", ".", ".."}
    ):
        raise HTTPException(400, "Enter a public GitHub repository URL.")

    try:
        return await asyncio.wait_for(
            review_repository(path[1], path[2].removesuffix(".git")),
            timeout=180,
        )
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            raise HTTPException(404, "Repository or source file not found.") from error
        raise HTTPException(502, "GitHub could not provide the repository source.") from error
    except (httpx.RequestError, UnicodeDecodeError) as error:
        raise HTTPException(502, "Could not read the repository source.") from error
    except TimeoutError as error:
        raise HTTPException(504, "The code review timed out. Please retry.") from error
