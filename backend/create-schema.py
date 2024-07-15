import weaviate
from weaviate.classes.config import Configure, Property, DataType
import openai
import os
from wasabi import msg
from dotenv import load_dotenv

load_dotenv() 

msg.divider("Starting schema creation")

# # Print environment variables to debug
# wcd_url = os.getenv("WCD_URL")
# wcd_api_key = os.getenv("WCD_API_KEY")
# openai_api_key = os.getenv("OPENAI_API_KEY")

# print(f"WCD_URL: {wcd_url}")
# print(f"WCD_API_KEY: {wcd_api_key}")
# print(f"OPENAI_API_KEY: {openai_api_key}")

# # Ensure the environment variables are not None
# if not wcd_url or not wcd_api_key or not openai_api_key:
#     raise ValueError("One or more environment variables are missing. Please check your .env file.")

# Create a client instance to connect to the Weaviate instance
client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WCD_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(api_key=os.getenv("WCD_API_KEY")),
        headers = {"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
        )

# # Create the collection
# client.collections.create(
#     "Chunk",
#     description="Chunks of Documentations",
#     vectorizer_config=Configure.Vectorizer.text2vec_openai(),
#     generative_config=Configure.Generative.openai(
#         model="gpt-3.5-turbo",
#     ),
#     properties=[
#         Property(name="text", data_type=DataType.TEXT, description="Content of the document"),
#         Property(name="doc_name", data_type=DataType.TEXT, description="Document name"),
#         Property(name="doc_uuid", data_type=DataType.TEXT, description="Document UUID", skip_vectorization=True, vectorize_property_name=True),
#         Property(name="chunk_id", data_type=DataType.NUMBER, description="Document chunk from the whole document", skip_vectorization=True, vectorize_property_name=True),
#     ],
# )

# client.collections.create(
#     "Document",
#     description="Documentation",
#     properties=[
#         Property(name="text", data_type=DataType.TEXT, description="Content of the document"),
#         Property(name="doc_name", data_type=DataType.TEXT, description="Document name"),
#         Property(name="doc_type", data_type=DataType.TEXT, description="Document type"),
#         Property(name="doc_link", data_type=DataType.TEXT, description="Link to document"),
#     ],
# )

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
            Property(name="doc_uuid", data_type=DataType.TEXT, description="Document UUID", skip_vectorization=True, vectorize_property_name=True),
            Property(name="chunk_id", data_type=DataType.NUMBER, description="Document chunk from the whole document", skip_vectorization=True, vectorize_property_name=True),
        ],
    )
    msg.good("'Document' and 'Chunk' schemas created")

msg.info("Done")