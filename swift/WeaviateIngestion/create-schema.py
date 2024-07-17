from util import setup_client
import weaviate
from weaviate.classes.config import Configure, Property, DataType

import os
from wasabi import msg
from dotenv import load_dotenv

load_dotenv() 

msg.divider("Starting schema creation")


# Create a client instance to connect to the Weaviate instance
client = setup_client(
    openai_key=os.environ.get("OPENAI_API_KEY", ""),
    weaviate_url=os.environ.get("WCD_URL", ""),
    weaviate_key=os.environ.get("WCD_API_KEY", ""),
)

if client.collections.exists("Document"):
    user_input = input(
        "Document class already exists, do you want to overwrite it? (y/n): "
    )
    if user_input.strip().lower() == "y":
        client.collections.delete("Document")
        client.collections.delete("Chunk")
        client.collections.create(
            "Document",
            description="Documentation",
            properties=[
                Property(name="text", data_type=DataType.TEXT, description="Content of the document"),
                Property(name="doc_name", data_type=DataType.TEXT, description="Document name"),
                Property(name="doc_type", data_type=DataType.TEXT, description="Document type"),
                Property(name="doc_link", data_type=DataType.TEXT, description="Link to document"),
            ],
        )
        client.collections.create(
            "Chunk",
            description="Chunks of Documentations",
            vectorizer_config=Configure.Vectorizer.text2vec_openai(),
            generative_config=Configure.Generative.openai(
                model="gpt-3.5-turbo",
            ),
            properties=[
                Property(name="text", data_type=DataType.TEXT, description="Content of the document"),
                Property(name="doc_name", data_type=DataType.TEXT, description="Document name"),
                Property(name="doc_uuid", data_type=DataType.TEXT, description="Document UUID", skip_vectorization=True, vectorize_property_name=True),
                Property(name="chunk_id", data_type=DataType.NUMBER, description="Document chunk from the whole document", skip_vectorization=True, vectorize_property_name=True),
            ],
        )
        msg.good("'Document' and 'Chunk' schemas created")
    else:
        msg.warn("Skipped deleting Document and Chunk schema, nothing changed")
else:
    client.collections.create(
    "Document",
    description="Documentation",
    properties=[
        Property(name="text", data_type=DataType.TEXT, description="Content of the document"),
        Property(name="doc_name", data_type=DataType.TEXT, description="Document name"),
        Property(name="doc_type", data_type=DataType.TEXT, description="Document type"),
        Property(name="doc_link", data_type=DataType.TEXT, description="Link to document"),
    ],
    )
    client.collections.create(
        "Chunk",
        description="Chunks of Documentations",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(),
        generative_config=Configure.Generative.openai(
            model="gpt-3.5-turbo",
        ),
        properties=[
            Property(name="text", data_type=DataType.TEXT, description="Content of the document"),
            Property(name="doc_name", data_type=DataType.TEXT, description="Document name"),
            Property(name="doc_type", data_type=DataType.TEXT, description="Document type"),
            Property(name="doc_uuid", data_type=DataType.TEXT, description="Document UUID", skip_vectorization=True, vectorize_property_name=True),
            Property(name="chunk_id", data_type=DataType.NUMBER, description="Document chunk from the whole document", skip_vectorization=True, vectorize_property_name=True),
        ],
    )
    msg.good("'Document' and 'Chunk' schemas created")

msg.info("Done")