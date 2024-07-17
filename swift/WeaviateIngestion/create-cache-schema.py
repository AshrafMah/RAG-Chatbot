import os
from wasabi import msg  # type: ignore[import]
from weaviate.classes.config import Configure, Property, DataType

from util import setup_client

from dotenv import load_dotenv

load_dotenv()

msg.divider("Starting cache collection creation")


client = setup_client(
    openai_key=os.environ.get("OPENAI_API_KEY", ""),
    weaviate_url=os.environ.get("WCD_URL", ""),
    weaviate_key=os.environ.get("WCD_API_KEY", ""),
)

if client.collections.exists("Cache"):
    user_input = input(
        "Cache class already exists, do you want to overwrite it? (y/n): "
    )
    if user_input.strip().lower() == "y":
        client.collections.delete("Cache")
        client.collections.create(
            "Cache",
            description="Cache of Documentations and their queries",
            vectorizer_config=Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(name="query", data_type=DataType.TEXT, description="Query"),
                Property(name="system", data_type=DataType.TEXT, description="System message", skip_vectorization=True, vectorize_property_name=False),
                Property(name="results", data_type=DataType.TEXT, description="List of results", skip_vectorization=True, vectorize_property_name=False),
            ],
        )
        msg.good("'Cache' collection created")
    else:
        msg.warn("Skipped deleting Cachecollection, nothing changed")
else:
    client.collections.create(
        "Cache",
        description="Cache of Documentations and their queries",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(),
        properties=[
            Property(name="query", data_type=DataType.TEXT, description="Query"),
            Property(name="system", data_type=DataType.TEXT, description="System message", skip_vectorization=True, vectorize_property_name=False),
            Property(name="results", data_type=DataType.TEXT, description="List of results", skip_vectorization=True, vectorize_property_name=False),
        ],
    )
    msg.good("'Cache' collections created")

msg.info("Done")