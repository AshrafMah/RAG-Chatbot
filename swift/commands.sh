# Create Document and Chunk Schema, deletes existing schemas
python WeaviateIngestion/create-schema.py

# Create Cache, delete existing cache
python WeaviateIngestion/create-cache-schema.py

# Create Suggestions, delete existing cache
python WeaviateIngestion/create-suggestion-schema.py

# Load and chunk data to import into Weaviate (Using Haystrack processing)
python WeaviateIngestion/import_weaviate.py