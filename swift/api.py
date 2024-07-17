import os

from wasabi import msg 

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv

from SwiftEngine.SimpleSwiftEngine import SimpleSwiftQueryEngine

load_dotenv()

# Initialize the SimpleSwiftQueryEngine with API keys and Weaviate URL from environment variables
swift_engine = SimpleSwiftQueryEngine(
    os.environ.get("WCD_URL", ""),
    os.environ.get("WCD_API_KEY", ""),
    os.environ.get("OPENAI_API_KEY", ""),
)

msg.good("Connected to Weaviate Client")

# FastAPI App
app = FastAPI()

origins = ["http://localhost:3000", os.environ.get("VERBA_FRONTEND", "")]

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
        system_msg,results = swift_engine.query(payload.query)
        msg.good(f"Succesfully processed query: {payload.query}")

        # if results[0]["_additional"]["generate"]["error"]:
        #     system_msg = results[0]["_additional"]["generate"]["error"]
        # else:
        #     system_msg = results[0]["_additional"]["generate"]["groupedResult"]

        # if system_msg == None:
        #     msg.warn(results[0])

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
    
    
@app.post("/suggestions")
async def suggestions(payload: QueryPayload):
    try:
        suggestions = swift_engine.get_suggestions(payload.query)

        return JSONResponse(
            content={
                "suggestions": suggestions,
            }
        )
    except Exception as e:
        return JSONResponse(
            content={
                "suggestions": [],
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
        msg.fail(f"All Document retrieval failed: {str(e)}")
        return JSONResponse(
            content={
                "document": {},
            }
        )

@app.get("/get_all_documents")
async def get_all_documents():
    msg.info(f"Get all documents request received")

    try:
        documents = swift_engine.retrieve_all_documents()
        msg.good(f"Succesfully retrieved document: {len(documents)} documents")
        return JSONResponse(
            content={
                "documents": documents,
            }
        )
    except Exception as e:
        msg.fail(f"Document retrieval failed: {str(e)}")
        return JSONResponse(
            content={
                "documents": [],
            }
        )