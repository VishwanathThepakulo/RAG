from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os


class Embedding:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('api_key')
        if not api_key:
            raise ValueError("API key not found")
        self.embedding_model  = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=api_key,
        )
        
    def get_embeddings(self,data):
        docs_to_insert = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        documents = text_splitter.split_documents(data)
        # print("=================",type(documents),"=============\n",documents[0].metadata)
        texts = [doc.page_content for doc  in documents]
        # print(texts[0])
        embeddings = self.embedding_model.embed_documents(texts)
        for text, emb in zip(texts, embeddings):
            item = {"text":text,"embeddings":emb}
            docs_to_insert.append(item)
        # print(docs_to_insert[0])
        # print(len(docs_to_insert[0]['embeddings']))
        return docs_to_insert
    
    def query_embedding(self, query_text:str):
        result = self.embedding_model.embed_query(query_text)
        print(type(result))
        return result



















































