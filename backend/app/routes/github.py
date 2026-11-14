import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/github", tags=["GitHub"])

@router.get("/repository")
async def get_repository(url: str):
    try:
        parts = url.rstrip("/").split("/")

        if len(parts) < 2:
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub repository URL"
            )

        owner = parts[-2]
        repo = parts[-1].removesuffix(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository not found"
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="GitHub API request failed"
            )

        data = response.json()

        return {
            "name": data["name"],
            "full_name": data["full_name"],
            "description": data["description"],
            "language": data["language"],
            "stars": data["stargazers_count"],
            "url": data["html_url"]
        }

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to GitHub"
        )