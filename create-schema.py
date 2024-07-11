import weaviate
from weaviate.auth import AuthApiKey
from weaviate.collections import Collection
from weaviate.classes.config import Configure, Property, DataType
import os
from wasabi import msg
from dotenv import load_dotenv

load_dotenv() 

msg.divider("Starting schema creation")

# Create a client instance to connect to the Weaviate instance
client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WCD_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCD_API_KEY")),
        )

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

if client.collections.exists("BlogPost"):
    user_input = input(
        "BlogPost class already exists, do you want to delete it? (y/n): "
    )
    if user_input.strip().lower() == "y":
        client.collections.delete("BlogPost")
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
        msg.good("'BlogPost' schema created")
    else:
        msg.warn("Skipped deleting BlogPost, nothing changed")
else:
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
    msg.good("'BlogPost' schema created")

msg.info("Done")
