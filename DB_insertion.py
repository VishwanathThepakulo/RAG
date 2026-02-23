from pymongo import MongoClient
# from embedding_logic import Embedding
import os
from dotenv import load_dotenv

class DBConnection:
    def __init__(self):
        load_dotenv()
        db_credentials = os.getenv('DB_CREDENTIALS')
        if not db_credentials:
            raise ValueError("API key not found")
        self.mongo_client = MongoClient(db_credentials)
        

    
    def db_insertion(self, ingestion_data):
        collection = self.mongo_client['ragDB']['serachable_docs']
        results = collection.insert_many(ingestion_data)   
        return results 