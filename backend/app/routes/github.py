import httpx
import base64
from fastapi import APIRouter, HTTPException
from app.services.repository_service import collect_source_files
from app.services.repository_service import fetch_source_contents

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

@router.get("/files")
async def get_repo_files(url:str):
    parts=url.rstrip("/").split("/")
    
    if len(parts)<2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )
        
    owner=parts[-2]
    repo=parts[-1].removesuffix(".git")
    
    async with httpx.AsyncClient() as client:
        
        #get repository default branch
        repo_response=await client.get(
            f"https://api.github.com/repos/{owner}/{repo}"
        )
        
        if repo_response.status_code==404:
            raise HTTPException(
                status_code=404,
                detail="Repository not found"
            )
        if repo_response.status_code!=200:
            raise HTTPException(
                status_code=502,
                detail="GitHub API request failed"
            )
        default_branch=repo_response.json()[
            "default_branch"
        ]
        
        
        #fetch complete file tree
        tree_response=await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}",
            params={"recursive":"1"}
        )
        
        if tree_response.status_code!=200:
            raise HTTPException(
                status_code=502,
                detail="Unable to fetch the repository files"
            )
        tree_data=tree_response.json()
        files=[
            {
                "path": item["path"],
                "type": item["type"]
            }
            for item in tree_data.get("tree",[])
        ]
        return {
        "repository": f"{owner}/{repo}",
        "default_branch": default_branch,
        "total_items": len(files),
        "truncated": tree_data.get("truncated", False),
        "files": files
    }

@router.get("/fileContent")
async def get_file_content(url:str,path:str):
    parts=url.rstrip("/").split("/")
    if len(parts)<2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )
    owner=parts[-2]
    repo=parts[-1].removesuffix(".git")
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    try:
        async with httpx.AsyncClient() as client:
            response=await client.get(api_url)
            
        if response.status_code==404:
            raise HTTPException(404,"File not found")
        if response.status_code!=200:
            raise HTTPException(502,"GitHub API request failed")
        data=response.json()
        
        if data.get("type")!="file":
            raise HTTPException(400,"Path does not point to a file")
        if data.get("size",0) >1_000_000:
            raise HTTPException(413,"File size exceeds 1MB")
        content=base64.b64decode(data["content"]).decode("utf-8")
        
        return {
            "repository":f"{owner}/{repo}",
            "file_path":data["path"],
            "size":data["size"],
            "content":content
            
        }
    except httpx.RequestError:
        raise HTTPException(502,"unable to connect the github")
    except UnicodeDecodeError:
        raise HTTPException(405,"File is not valid UTF-8 text")

@router.get("/sourceFiles")
async def get_source_files(url:str):
    parts=url.rstrip("/").split("/")
    if len(parts)<2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )
    owner=parts[-2]
    repo=parts[-1].removesuffix(".git")
    try:
        result = await collect_source_files(owner, repo)
        return result

    except httpx.HTTPStatusError as e:
        print("GitHub status:", e.response.status_code)
        print("GitHub response:", e.response.text)
        
        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {e.response.status_code}"
        )
    except httpx.RequestError as e:
        print("Connection error:", str(e))

        raise HTTPException(
            status_code=502,
            detail="Unable to connect to GitHub"
        )
        
@router.get("/source-code")
async def get_source_code(url: str):

    parts = url.rstrip("/").split("/")

    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )

    owner = parts[-2]
    repo = parts[-1].removesuffix(".git")

    try:
        return await fetch_source_contents(owner, repo)

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {e.response.status_code}"
        )

    except (httpx.RequestError, UnicodeDecodeError, KeyError):
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve source files from GitHub"
        )