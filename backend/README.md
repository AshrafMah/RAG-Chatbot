# 🔧 Swift - Backend 🔧

Welcome to the backend documentation for  Swift, designed to guide you through setting up, managing dependencies, and running this project.

## 🗂️ Dataset

We use Weaviate's documentation to power the Live demo.

## 📦 Setup & Requirements

### ⚙️ Manual Installation

The following steps guide you through setting up the backend manually

1. **Set up your Weaviate cluster:**
- **OPTION 1** Create a cluster in WCS (for more details, refer to the [Weaviate Cluster Setup Guide](https://weaviate.io/developers/wcs/guides/create-instance))
- **OPTION 2** Use Docker-Compose to setup a cluster locally [Weaviate Docker Guide](https://weaviate.io/developers/weaviate/installation/docker-compose)

2. **Set environment variables:**
- The following environment variables need to be set in a `.env` file
- ```export WEAVIATE_URL="http://your-weaviate-server:8080"```
- ```export WEAVIATE_API_KEY="your-weaviate-database-key"```
- ```export OPENAI_API_KEY="your-openai-api-key"```
> You can use `.env` files (https://github.com/theskumar/python-dotenv) or set the variables to your system
3. **Create a new Python virtual environment:**
- Make sure you have python `>=3.8.0` installed
- ```python3 -m venv env```
- ```source env/bin/activate```

4. **Install dependencies:**
- The `requirements.txt` file lists the Python dependencies needed. Install these with the following command:
- ```pip install -r requirements.txt```

5. **Start the FastAPI app:**
- ```uvicorn api:app --reload --host 0.0.0.0 --port 8000```


## Importing Data (WIP)

Currently, there is no interface to upload data. For now it's done through multiple scripts:

**Import dataset:**
- Use the `python create-schema.py` script to create the two schemas
    - Document (whole documents, not vectorized, contain meta data)
    - Chunks (document chunks, vectorized, contain uuid of original document)

- We offer multiple approaches on loading, cleaning, chunking the data:

- Make sure to add your github token to the `.env` file
- ```export GITHUB_TOKEN="your-token"```

- Haystack: `python import-data-haystack.py` (Downloads Weaviate data and uses Haystack to ingest them to Weaviate)

## Swift Engine

The FastAPI communicates with the SwiftEngine, which is an interface for handling queries and returning results. It acts as a wrapper to enable Swift to use different approaches on querying and information retrieval:

- `SimpleSwiftEngine`
    - Uses Weaviate-only, to retrieve documents and the generate module to construct the system answers
