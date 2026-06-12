# AI-Powered E-commerce RAG Chatbot

An intelligent customer support chatbot that answers product-related queries using a **Retrieval-Augmented Generation (RAG)** pipeline. The chatbot scrapes product data from an e-commerce website, stores it in a vector database, retrieves relevant information, and generates grounded responses using an LLM.

## Features

* Scrapes product data (name, description, price, category, ratings, availability).
* Stores data in JSON format.
* Builds embeddings using HuggingFace models.
* Uses **ChromaDB** as the vector database.
* Implements **RAG** using LangChain.
* Generates responses using **Groq (Llama 3.1)**.
* Provides a **FastAPI backend** and a **Bootstrap frontend**.

## Tech Stack

* Python
* FastAPI
* LangChain
* ChromaDB
* HuggingFace Embeddings
* Groq (Llama 3.1)
* HTML, CSS, JavaScript, Bootstrap

## Setup

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_api_key
```

Run scraper:

```bash
python app/scraper.py
```

Build vector database:

```bash
python app/build_index.py
```

Start backend:

```bash
uvicorn app.api:app --reload
```

Start frontend:

```bash
cd frontend
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

## Example Queries

* What is the price of Product X?
* Tell me about Product X.
* Compare Product A and Product B.
* Recommend similar products.
* Which products belong to category X?


