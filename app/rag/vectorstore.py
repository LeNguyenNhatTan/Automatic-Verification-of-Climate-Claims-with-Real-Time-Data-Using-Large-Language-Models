import os
import requests

from typing import List
from langchain.schema import Document
from datetime import datetime, timedelta
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from core.config import NEWSAPI_KEY

def fetch_news_articles(source: str, query: str, days_back: int = 30) -> List[Document]:
    
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    url = f"https://newsapi.org/v2/everything?q={query}&from={from_date}&apiKey={NEWSAPI_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        documents = []
        for article in articles:
            content = article.get("content") or article.get("description") or ""
            if content:
                metadata = {
                    "source": article.get("url", "Unknown"),
                    "title": article.get("title", "No title"),
                    "publishedAt": article.get("publishedAt", "Unknown")
                }
                documents.append(Document(page_content=content, metadata=metadata))
        
        return documents
    except requests.RequestException as e:
        print(f"Error fetching articles from {source}: {e}")
        return []
    
def load_vectorstore(persist_dir: str, source: str, query: str) -> Chroma:

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(persist_dir):
        print(f"Loading existing vectorstore from: {persist_dir}")
        return Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

    print(f"Creating new vectorstore at: {persist_dir}")
    os.makedirs(persist_dir, exist_ok=True)

    documents = fetch_news_articles(source, query)
    if not documents:
        print(f"No articles found for {source}. Using empty vectorstore.")
        return Chroma(embedding_function=embedding_model, persist_directory=persist_dir)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(chunks, embedding=embedding_model, persist_directory=persist_dir)
    vectorstore.persist()

    print(f"Vectorstore created and saved at: {persist_dir}")
    return vectorstore
