import chromadb
from app.services.chunking_service import chunk_repo


#create persistent chromadb storage
client=chromadb.PersistentClient(
    path="./chromadb_db"
)

#create or retreive the collection 
collection=client.get_or_create_collection(
    name="repository_code"
)
async def index_repository(owner:str,repo:str):
    
    #get the repo chunks
    result=await chunk_repo(owner,repo)
    
    ids=[]
    documents=[]
    metadata=[]
    
    for file in result["files"]:
        file_path=file["path"]
        
        for chunk in file["chunks"]:
            chunk_id=(
                f"{owner}_{repo}_"
                f"{file_path}_{chunk['chunk_index']}"
                
            )
            ids.append(chunk_id)
            documents.append(chunk["content"])
            metadata.append({
                "repository":result["repository"],
                "file_path":file_path,
                "chunk_index":chunk["chunk_index"],
                "start_line":chunk["start_line"],
                "end_line":chunk["end_line"],
            })
    if not documents:
        return {
            "message":"No code chunks found",
            "total_chunks":0
        }
        
    #generate emdeddings and store chunks
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadata
    )
    
    return {
        "repository":result["repository"],
        "total_files":result["total_files"],
        "total_chunks":len(documents),
        "message":"Repository indexed successfully"
    }
