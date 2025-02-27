import weaviate
from weaviate import Client

class SwiftQueryEngine:
    """
    An interface for Swift Query Engine.
    """

    client: Client = None

    def __init__(self, weaviate_url: str, weaviate_api_key: str, openai_key: str):
        SwiftQueryEngine.client = weaviate.Client(
            url=weaviate_url,
            auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),
            additional_headers={"X-OpenAI-Api-Key": openai_key},
        )

    def query_chunks(self, query_string: str) -> tuple:
        """Execute a query to a receive specific chunks from Weaviate
        @parameter query_string : str - Search query
        @returns tuple - (system message, iterable list of results)
        """
        raise NotImplementedError("query must be implemented by a subclass.")
    
    def change_generative_model(self, generative_model: str) -> dict:
        """Change schema to another generative module model"""
        raise NotImplementedError(
            "retrieve_document must be implemented by a subclass."
        )
    
    def retrieve_document(self, doc_id: str) -> None:
        """Return a document by it's ID (UUID format) from Weaviate
        @parameter doc_id : str - Document ID
        @returns dict - Document dict
        """
        raise NotImplementedError(
            "retrieve_document must be implemented by a subclass."
        )

    def get_client(self) -> Client:
        return SwiftQueryEngine.client
    