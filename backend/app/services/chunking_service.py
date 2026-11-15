from app.services.repository_service import fetch_source_contents
def split_into_chunks(
    content:str,
    chunk_size:int=80,
    overlap:int=10
    
):
    if chunk_size <=0:
        raise ValueError("chunk_size must be positive")
    if overlap <0 or overlap >=chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")
    lines=content.splitlines()
    
    chunks=[]
    start=0
    chunk_index=0
    while start<len(lines):
        end=min(start + chunk_size,len(lines))
        
        chunk_content="\n".join(lines[start:end])
        chunks.append({
            "chunk_index":chunk_index,
            "start_line":start +1,
            "end_line":end,
            "content":chunk_content
        })
        
        chunk_index+=1
        if end==len(lines):
            break
        
        start=end -overlap
    return chunks
async def chunk_repo(owner:str,repo:str):
    result=await fetch_source_contents(owner,repo)
    chunked_files=[]
    
    for file in result["files"]:
        chunks=split_into_chunks(file["content"])
        
        chunked_files.append({
            "path":file["path"],
            "total_chunks":len(chunks),
            "chunks":chunks
        })
        
    return {
        "repository":result["repository"],
        "branch":result["branch"],
        "total_files":len(chunked_files),
        "total_chunks":sum(file["total_chunks"] for file in chunked_files),
        "files":chunked_files
    }
    
    
    
    