from langchain_community.document_loaders import PyPDFLoader
from embedding_logic import Embedding
from DB_insertion import DBConnection
from model_calling import calling
from fastapi import FastAPI
from pydantic import BaseModel

class Validation(BaseModel):
    path : str
    question : str
class Validation1(BaseModel):
    question : str

app = FastAPI()
embedding = Embedding()

@app.post('/embedding/insertion')
def emb_and_insertion(file_path:Validation):
    loader = PyPDFLoader(file_path.path)
    data = loader.load()
    
    results = embedding.get_embeddings(data)
    # for result in results:
    #     print(result['text'],"\n===================================================\n",result['embeddings'],"\n===================================================\n",)
    insertion = DBConnection()
    db_inesrtion = insertion.db_insertion(results)
    # print(type(db_inesrtion))
    indexing = insertion.vector_indexing()
    insertion.connection_close()
    return {
        'status':'success',
        'inserted_count':len(db_inesrtion.inserted_ids),
        'indexing':indexing
    }

@app.post('/query')    
def user_question(question: Validation1):
    query_vector = embedding.query_embedding(question.question)
    
    db = DBConnection()
    results = db.vector_search(query_vector)
    texts = []
    for doc in results:
        texts.append(doc['text'])
    context = "\n\n".join(texts)
    
    ai_reply = calling(question.question, context)
        
    db.connection_close()

    return {
        'status': 200,
        'answer': ai_reply
    }
    


def main():
    # input_file_path = input("Enter File path :").strip('"')
    # file_path = rf"{input_file_path}"
    # emb_and_insertion(file_path)
    # user_query = input("Enter user query : ")
    # embedded_user_query = user_question(user_query)
    # print(embedded_user_query[0][:10])
    pass
    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",              
        host='localhost',
        port=9000
        # reload=True             
    )
    # main()    


