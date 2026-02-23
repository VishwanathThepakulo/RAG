from langchain_community.document_loaders import PyPDFLoader
from embedding_logic import Embedding
from DB_insertion import DBConnection
from fastapi import FastAPI
from pydantic import BaseModel

class Validation(BaseModel):
    path : str

app = FastAPI()

@app.post('/embedding/insertion')
def emb_and_insertion(file_path:Validation):
    loader = PyPDFLoader(file_path.path)
    data = loader.load()
    embedding = Embedding()
    results = embedding.get_embeddings(data)
    # for result in results:
    #     print(result['text'],"\n===================================================\n",result['embeddings'],"\n===================================================\n",)
    insertion = DBConnection()
    db_inesrtion = insertion.db_insertion(results)
    # print(type(db_inesrtion))
    return {
        'status':'success',
        'inserted_count':len(db_inesrtion.inserted_ids)
    }



def main():
    input_file_path = input("Enter File path :").strip('"')
    file_path = rf"{input_file_path}"
    emb_and_insertion(file_path)
    
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",              # ← important: "filename:app"
        host='localhost',
        port=9000
        # reload=True              # auto-reload during dev
    )
    
