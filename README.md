# RAG-Chatbot
Build a chatbot in production with RAG, Weaviate and LlamaIndex.

> Currently this repo only supports the data processing pipeline for Weaviate documentation, supporting custom data is WIP.

## 🎯 Overview

Our RAG-Chatbot provides an interface for importing and querying your data. You can ask questions about your documents and discuss different data points.
It leverages Weaviate together with Generative Search to retrieve relevant document pieces and uses LLM to power the answer to your query.

### 💥 Generative Search to answer your queries 

Swift uses Weaviate's `generate` module to look at the retrieved document pieces and form an answer to your query. 

### 🔥 Semantic Cache to speed up your process

We embed the generated results and queries to Weaviate, and use it as a `Semantic Cache`.
This method is advantageous as it enables Swift to return results from queries that are semantically equal to the new query. This method allows us to gain much more from generated results than traditional string matching would permit. It's a simple yet potent solution that enhances the efficiency of the search process.

## 🛠️ Project Structure

RAG-Chatbot is structured in three main components:

1. A Weaviate database (either cluster hosted on WCS or local).
2. A FastAPI endpoint facilitating communication between the LLM provider and database.
3. An interactive React frontend for displaying the information.

Make sure you have Python (`>=3.8.0`) and Node (`>=18.16.0`) installed.

## 📚 Getting Started

To kick-start with the Healthsearch Demo, please refer to the READMEs in the `Frontend` and `Backend` folders:

- [Frontend README](./frontend/README.md)
- [Backend README](./backend/README.md)

## 💡 Usage

Follow these steps to use Swift

1. Set up the Weaviate database, FastAPI backend, and the React frontend by following the instructions in their respective READMEs.
2. Launch the database, backend server, and the frontend application.
3. Use the Swift frontend to talk with you data
