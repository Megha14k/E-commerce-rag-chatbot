import json
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

DATA_FILE = "data/products.json"
DB_DIR = "data/chroma_db"

def product_to_text(product):
    specs = "\n".join(
        f"{k}: {v}" for k, v in product.get("specifications", {}).items()
    )

    return f"""
Product Name: {product['name']}
Category: {product['category']}
Price: {product['price']}
Rating: {product['rating']}
Availability: {product['availability']}
Description: {product['description']}
Specifications:
{specs}
URL: {product['url']}
"""

def build_index():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    documents = [
        Document(
            page_content=product_to_text(product),
            metadata={
                "name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "url": product["url"]
            }
        )
        for product in products
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    # db.persist()
    print("Vector index created.")

if __name__ == "__main__":
    build_index()