from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
import weaviate
from weaviate.auth import AuthApiKey
import os
from dotenv import load_dotenv

load_dotenv() 

# Create a client instance to connect to the Weaviate instance
client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WCD_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCD_API_KEY")),
        )

# load the blogs in using the reader
blogs = SimpleDirectoryReader('./data').load_data()

# chunk up the blog posts into nodes 
parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(blogs)