import os
import json
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

load_dotenv()

DB_DIR = "data/chroma_db"
DATA_FILE = "data/products.json"

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

client = Groq(api_key=groq_api_key)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embedding_model
)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    products = json.load(f)

SYSTEM_PROMPT = """
You are a customer support chatbot for an e-commerce website.

Answer only using the provided product context.
If the answer is not available in the context, say:
"I could not find that information in the scraped product data."

Do not invent prices, ratings, availability, or specifications.
Keep answers clear and helpful.
"""

def clean_price(price):
    return str(price).replace("Â£", "£")

def find_exact_products(question):
    question_lower = question.lower()
    matched = []

    for product in products:
        name = product.get("name", "")
        if name.lower() in question_lower:
            matched.append(product)

    return matched

def product_to_context(product):
    specs = product.get("specifications", {})
    specs_text = "\n".join([f"{k}: {v}" for k, v in specs.items()])

    return f"""
Product Name: {product.get("name")}
Category: {product.get("category")}
Price: {clean_price(product.get("price"))}
Rating: {product.get("rating")}
Availability: {product.get("availability")}
Description: {product.get("description")}
Specifications:
{specs_text}
URL: {product.get("url")}
"""

def ask_bot(question: str):
    exact_products = find_exact_products(question)

    if exact_products:
        context = "\n\n".join(product_to_context(product) for product in exact_products)

        sources = [
            {
                "name": product.get("name"),
                "category": product.get("category"),
                "price": clean_price(product.get("price")),
                "url": product.get("url")
            }
            for product in exact_products
        ]

    else:
        docs = db.similarity_search(question, k=3)
        context = "\n\n".join(doc.page_content for doc in docs)

        seen = set()
        sources = []

        for doc in docs:
            url = doc.metadata.get("url")
            if url not in seen:
                seen.add(url)
                sources.append({
                    "name": doc.metadata.get("name"),
                    "category": doc.metadata.get("category"),
                    "price": clean_price(doc.metadata.get("price")),
                    "url": url
                })

    prompt = f"""
Product Context:
{context}

Customer Question:
{question}

Answer using only the product context.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content
    answer = answer.replace("Â£", "£")

    return {
        "answer": answer,
        "sources": sources
    }