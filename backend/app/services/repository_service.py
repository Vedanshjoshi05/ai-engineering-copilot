import httpx
SUPPORTED_EXTENSIONS={
    ".py",".json",".txt",".md",".html",".css",".js",".php",".rb",".go",".rs",".rb",".rbx"
}
IGNORED_DIRECTORIES={
    "node_modules","venv","__pycache__",".venv","dist","build",".git","vendor"
}
async def collect_source_files(owner:str,repo:str):
    async with httpx.AsyncClient(timeout=30) as client:
        #get repository 
        repo_response=await client.get(
            f"https://api.github/com/repos/{owner}/{repo}"
        )
        repo_response.raise_for_status()
        branch=repo_response.json()["default_branch"]
        
        #get repository file tree
        tree_response=await client.get(
            f"https://appi.github/com/repos/{owner}/{repo}/git/trees/{branch}",
            params={"recursive":"1"}
        )
        
        tree_response.raise_for_status()
        tree=tree_response.json()["tree"]
        source_files=[]
        
        for item in tree:
            if item["type"]!="blob":
                continue
            path=item["path"]
            parts=path.split("/")
            if any(part in IGNORED_DIRECTORIES for part in parts):
                continue
            if not any(path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                continue
            if item.get("size",0) >1_000_000:
                continue
            source_files.append({
                "path":path,
                "size":item["size"]
            })
            if len(source_files) >=20:
                break
        return{
            "repository":f"{owner}/{repo}",
            "branch":branch,
            "files":source_files,
            "total_files":len(source_files)
            
        }
        
