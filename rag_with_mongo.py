from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

 #load variables from.env



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































# for doc in document:
#     item = {
#         "text": doc.page_content,
#         "embeddings": get_embeddings(doc.page_content)
#     }
#     docs_to_insert.append(item)
# print(docs_to_insert[0])

# print(data[0].page_content,'\n===========\n',data[1].page_content)







# print(HuggingFaceEndpointEmbeddings.model_fields)


# from langchain_huggingface import HuggingFaceEndpointEmbeddings

# print(HuggingFaceEndpointEmbeddings.__mro__)



# from pydantic import BaseModel
# class Student(BaseModel):
#     age: float

# s = Student(age="abc")
# print(s.age)
# print(type(s.age))


# class Parent:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
        
# class Child(Parent):
#     def details(self):
#         return f"Name is {self.name} and age is {self.age}"
    
# child = Child("Vishwa",25)

# print(child.details())














































