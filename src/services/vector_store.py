from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from sqlalchemy.orm import Session
import uuid
import os

# Set via .env or directly
CONNECTION_STRING = os.getenv("PGVECTOR_CONNECTION_STRING")

embeddings = OpenAIEmbeddings()  # or HuggingFaceEmbeddings, etc.

def index_chunks_with_langchain(chunks: list[str], pdf_id: int, db: Session):
    # Wrap into Langchain Document objects
    docs = [Document(page_content=chunk, metadata={"pdf_id": pdf_id}) for chunk in chunks]

    # Split (again, optionally - to double-split large chunks)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    # Store to pgvector
    PGVector.from_documents(
        documents=split_docs,
        embedding=embeddings,
        collection_name=f"pdf-{pdf_id}",
        connection_string=CONNECTION_STRING
    )
