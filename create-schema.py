import weaviate
from weaviate.auth import AuthApiKey
from weaviate.collections import Collection
from weaviate.classes.config import Configure, Property, DataType
import os
from dotenv import load_dotenv
load_dotenv() 

# Create a client instance to connect to the Weaviate instance
client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WCD_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCD_API_KEY")),
        )

# Delete all existing schema definitions
client.collections.delete_all()

# Create the collection based on the defined configuration
client.collections.create(
    "BlogPost",
    properties=[
        Property(name="Content", data_type=DataType.TEXT, description="Content from the blog post")
    ],
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    generative_config=Configure.Generative.openai(
        model="gpt-3.5-turbo",
    ),
    description="Blog post from the Weaviate website."
)

# Print a message indicating that the collection has been created
print("Collection configuration created")
