
import httpx
import base64
from urllib.parse import quote

SUPPORTED_EXTENSIONS = {
    ".py", ".json", ".txt", ".md", ".html", ".css",
    ".js", ".jsx", ".ts", ".tsx", ".php", ".rb",
    ".go", ".rs", ".java", ".cpp", ".c", ".h", ".hpp"
}

IGNORED_DIRECTORIES = {
    "node_modules", "venv", "__pycache__", ".venv",
    "dist", "build", ".git", "vendor",
    ".github", "docs"
}
CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".cpp", ".c", ".h", ".hpp",
    ".go", ".rs", ".php", ".rb"
}


async def collect_source_files(owner: str, repo: str):

    async with httpx.AsyncClient(timeout=30) as client:

        repo_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}"
        )
        repo_response.raise_for_status()

        branch = repo_response.json()["default_branch"]

        tree_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}",
            params={"recursive": "1"}
        )
        tree_response.raise_for_status()

        tree = tree_response.json()["tree"]

        source_files = []

        for item in tree:

            if item["type"] != "blob":
                continue

            path = item["path"]
            parts = path.split("/")

            if any(part in IGNORED_DIRECTORIES for part in parts):
                continue

            if not any(path.lower().endswith(ext) for ext in CODE_EXTENSIONS):
                continue

            if item.get("size", 0) > 1_000_000:
                continue

            source_files.append({
                "path": path,
                "size": item.get("size", 0)
            })

            if len(source_files) >= 20:
                break

        return {
            "repository": f"{owner}/{repo}",
            "branch": branch,
            "files": source_files,
            "total_files": len(source_files)
        }


async def fetch_source_contents(owner: str, repo: str):

    result = await collect_source_files(owner, repo)

    branch = result["branch"]
    files = result["files"][:5]

    source_contents = []

    async with httpx.AsyncClient(timeout=30) as client:

        for file in files:

            path = file["path"]

            api_url = (
                f"https://api.github.com/repos/{owner}/{repo}/contents/"
                f"{quote(path, safe='/')}"
            )

            response = await client.get(
                api_url,
                params={"ref": branch}
            )
            response.raise_for_status()

            data = response.json()

            if data.get("type") != "file":
                continue

            if data.get("encoding") != "base64":
                continue

            content = base64.b64decode(
                data["content"]
            ).decode("utf-8")

            source_contents.append({
                "path": path,
                "size": file["size"],
                "content": content
            })

    return {
        "repository": result["repository"],
        "branch": branch,
        "total_files": len(source_contents),
        "files": source_contents
    }
