import weaviate
from weaviate.auth import AuthApiKey
import os
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from dotenv import load_dotenv

load_dotenv() 

# Create a client instance to connect to the Weaviate instance
client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WCD_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCD_API_KEY")),
        )

# construct vector store
vector_store = WeaviateVectorStore(weaviate_client = client, index_name="BlogPost", text_key="content")

# setting up the storage for the embeddings
storage_context = StorageContext.from_defaults(vector_store = vector_store)

from upload import nodes

# set up the index
index = VectorStoreIndex(nodes, storage_context = storage_context)

# and now query 🚀
query_engine = index.as_query_engine()

query = input("Please enter your query: ")

response = query_engine.query(query)
print(response)

