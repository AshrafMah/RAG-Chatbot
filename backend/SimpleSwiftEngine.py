from SwiftEngine.interface import SwiftQueryEngine

class SimpleSwiftQueryEngine(SwiftQueryEngine):
    def query(self, query_string: str) -> tuple:
        """Execute a query to a receive specific chunks from Weaviate
        @parameter query_string : str - Search query
        @returns tuple - (system message, iterable list of results)
        """
        query_results = (
            SwiftQueryEngine.client.query.get(
                class_name="Chunk",
                properties=["text", "doc_name", "chunk_id", "doc_uuid"],
            )
            .with_near_text(content={"concepts": [query_string]})
            .with_generate(
                grouped_task=f"Answer the query {query_string} with the given snippets of documentation in 2-3 sentences or if needed give code examples. If the data is not sufficient say that you need more data."
            )
            .with_limit(6)
            .do()
        )

        if "data" not in query_results:
            raise Exception(query_results)

        results = query_results["data"]["Get"]["Chunk"]

        if results[0]["_additional"]["generate"]["error"]:
            system_msg = results[0]["_additional"]["generate"]["error"]
        else:
            system_msg = results[0]["_additional"]["generate"]["groupedResult"]

        return (system_msg, results)

    def retrieve_document(self, doc_id: str) -> dict:
        """Return a document by it's ID (UUID format) from Weaviate
        @parameter doc_id : str - Document ID
        @returns dict - Document dict
        """
        document = SwiftQueryEngine.client.data_object.get_by_id(
            doc_id,
            class_name="Document",
        )

        return document