from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import time

import os
from dotenv import load_dotenv

class DBConnection:
    def __init__(self):
        load_dotenv()
        db_credentials = os.getenv('DB_CREDENTIALS')
        if not db_credentials:
            raise ValueError("API key not found")
        self.mongo_client = MongoClient(db_credentials)
        self.collection = self.mongo_client['ragDB']['serachable_docs']
        # self.db
        

    
    def db_insertion(self, ingestion_data):
        # collection = self.mongo_client['ragDB']['serachable_docs']
        results = self.collection.insert_many(ingestion_data)   
        return results 
      
    def vector_indexing(self):
      for idx in self.collection.list_search_indexes():
        if idx['name'] == "vector_index":
          print("Index already exists")
          return {
            'status':200,
            'Index':'existed'
          }
      search_index_model = SearchIndexModel(
        definition={
            "fields": [
              {
                "type": "vector",
                "path": "embeddings",
                "numDimensions": 384,
                "similarity": "cosine"
              }
            ]
          },
          name="vector_index",
          type="vectorSearch"
      )
      result = self.collection.create_search_index(model=search_index_model)
      print("New search index named " + result + " is building.")

      # Wait for initial sync to complete
      print("Polling to check if the index is ready. This may take up to a minute.")
      predicate=None
      if predicate is None:
        predicate = lambda index: index.get("queryable") is True

      while True:
        indices = list(self.collection.list_search_indexes(result))
        if len(indices) and predicate(indices[0]):
          break
        time.sleep(5)
      print(result + " is ready for querying.")
      return {
        'status':200,
        'Index':'created'
      }

    def vector_search(self, query_vector, limit=5):
      pipeline = [
        {
          '$vectorSearch':{
            'index':'vector_index',
            'path':'embeddings',
            'queryVector':query_vector,
            'numCandidates':100,
            'limit':limit
          }
        },{
          '$project':{
            '_id':0,
            'text':1,
            "score": {"$meta": "vectorSearchScore"}
          }
        }
      ]
      results = list(self.collection.aggregate(pipeline))
      return results


    def connection_close(self):
      self.mongo_client.close()
      

    
    
    