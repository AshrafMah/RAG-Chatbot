import os
import weaviate 

from wasabi import msg 

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv

from SimpleSwiftEngine import SimpleSwiftQueryEngine

load_dotenv()

# Initialize the SimpleSwiftQueryEngine with API keys and Weaviate URL from environment variables
swift_engine = SimpleSwiftQueryEngine(
    os.environ.get("WEAVIATE_URL", ""),
    os.environ.get("WEAVIATE_API_KEY", ""),
    os.environ.get("OPENAI_API_KEY", ""),
)


msg.good("Connected to Weaviate Client")

# FastAPI App
app = FastAPI()

origins = ["http://localhost:3000"]

# Add middleware for handling Cross Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for query payload
class QueryPayload(BaseModel):
    query: str

# Define a Pydantic model for get document payload
class GetDocumentPayload(BaseModel):
    document_id: str

# Define health check endpoint
@app.get("/health")
async def root():
    try:
        # Check if the Weaviate client is ready
        if swift_engine.get_client().is_ready():
            return JSONResponse(
                content={
                    "message": "Alive!",
                }
            )
        else:
            return JSONResponse(
                content={
                    "message": "Database not ready!",
                },
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
    except Exception as e:
        msg.fail(f"Healthcheck failed with {str(e)}")
        return JSONResponse(
            content={
                "message": f"Healthcheck failed with {str(e)}",
            },
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

# Query endpoint
@app.post("/query")
async def query(payload: QueryPayload):
    try:
        # Use the query engine to process the query
        results = swift_engine.query(payload.query)
        msg.good(f"Succesfully processed query: {payload.query}")

        system_msg = results[0]["_additional"]["generate"]["groupedResult"]

        return JSONResponse(
            content={
                "system": system_msg,
                "documents": results,
            }
        )
    except Exception as e:
        msg.fail(f"Query failed: {str(e)}")
        return JSONResponse(
            content={
                "system": f"Something went wrong! {str(e)}",
                "documents": [],
            }
        )

# Get document by ID endpoint    
@app.post("/get_document")
async def get_document(payload: GetDocumentPayload):
    msg.info(f"Document ID received: {payload.document_id}")

    try:
        # Use the query engine to retrieve the document by ID
        document = swift_engine.retrieve_document(payload.document_id)
        msg.good(f"Succesfully retrieved document: {payload.document_id}")
        return JSONResponse(
            content={
                "document": document,
            }
        )
    except Exception as e:
        msg.fail(f"Query failed: {str(e)}")
        return JSONResponse(
            content={
                "document": {},
            }
        )