from uuid import uuid4
import fitz  # PyMuPDF
import re
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
# from langchain_community.vectorstores import FAISS
from langchain.vectorstores import FAISS
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from qdrant_client.http.models import CollectionStatus
from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import QdrantVectorStore
from qdrant_client.http.models import Distance, VectorParams


from langchain_community.chains import PebbloRetrievalQA
import fitz  # PyMuPDF
from fastapi import UploadFile
from langchain_openai import ChatOpenAI
# --- Configure Environment ---

from src.core.config import settings

# qdrant_client = QdrantClient(":memory:")

OPENAI_API_KEY = settings.OPENAI_API_KEY
# --- Qdrant Client ---
qdrant_client = QdrantClient(
    url=settings.QDRANT_HOST,
    # port=QDRANT_PORT
    api_key=settings.QDRANT_API_KEY
)

existing = qdrant_client.get_collections()

COLLECTION_NAME = "pdf_chunks"
# qdrant_client.create_collection(
#     collection_name=COLLECTION_NAME,
#     vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
# )

# --- Ensure Collection Exists ---
if COLLECTION_NAME not in [c.name for c in existing.collections]:
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )

def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        pdf_bytes = file.file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Failed to extract text: {str(e)}"

# def extract_text_from_pdf(file) -> str:
#     pdf_doc = fitz.open(stream=file.file.read(), filetype="pdf")
#     text = ""
#     for page in pdf_doc:
#         text += page.get_text()
#     return text

# def split_text(text: str, chunk_size=500, overlap=100) -> List[str]:
#     # Basic regex-based sentence splitter
#     sentences = re.split(r'(?<=[.!?]) +', text)
#     chunks = []
#     current_chunk = ""

#     for sentence in sentences:
#         if len(current_chunk) + len(sentence) <= chunk_size:
#             current_chunk += " " + sentence
#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = sentence

#     if current_chunk:
#         chunks.append(current_chunk.strip())

#     # Optional: add overlap
#     if overlap:
#         overlapped = []
#         for i in range(0, len(chunks)):
#             start = max(0, i - 1)
#             combined = " ".join(chunks[start:i+1])
#             overlapped.append(combined)
#         return overlapped

#     return chunks

def split_text(text: str) -> List[str]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    return text_splitter.create_documents([text])




# --- Load and Chunk PDF ---

# def load_and_split_pdf(file: UploadFile, pdf_id):
#     raw_text = extract_text_from_pdf(file)
#     chunks = split_text(raw_text, chunk_size=1000, overlap=150)
#     return [Document(page_content=chunk, metadata={"source": file.filename, "pdf_id": str(pdf_id)}) for chunk in chunks]

# def load_and_split_local_pdf(pdf_path: str):
#     loader = PyPDFLoader(pdf_path)
#     documents = loader.load()
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
#     return splitter.split_documents(documents)

# --- Index to Qdrant ---
def index_chunks_qdrant(chunks, pdf_id: int):
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
    # vectorstore  = Qdrant.from_documents(
    #     documents=chunks,
    #     embedding=embeddings,
    #     collection_name=COLLECTION_NAME,
    #     url=f"http://{QDRANT_HOST}:{QDRANT_PORT}"
    # )
    # Add proper metadata (pdf_id per chunk)
    uuids = [str(uuid4()) for _ in range(len(chunks))]

    vector_store.add_documents(documents=chunks, ids=uuids)


    for chunk in chunks:
        chunk.metadata["pdf_id"] = str(pdf_id)

    vector_store.add_documents(documents=chunks)
    # for deleting item from vector store
    # vector_store.delete(ids=[uuids[-1]])


    return vector_store

# --- For local development (optional FAISS index) ---
# def index_chunks_faiss(chunks):
#     embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
#     vector_store = FAISS.from_documents(chunks, embeddings)
#     return vector_store


# --- Create RetrievalQA chain from Qdrant ---
# def create_qa_chain(pdf_id: str):
#     embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
#     qdrant = Qdrant(
#         client=qdrant_client,
#         collection_name=COLLECTION_NAME,
#         embeddings=embeddings
#     )

#     retriever = qdrant.as_retriever(
#         search_kwargs={
#             "filter": {
#                 "must": [
#                     {"key": "pdf_id", "match": {"value": str(pdf_id)}}
#                 ]
#             }
#         }
#     )

#     llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.3)

#     qa_chain = PebbloRetrievalQA.from_chain_type(
#         app_name="my_pdf_chat_app",
#         description="PDF QA chain for document search",
#         owner="sandeep",
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True
#     )
#     return qa_chain

def create_qa_chain_simple(pdf_id: str):
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    qdrant = QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
        retrieval_mode=RetrievalMode.DENSE
    )

    retriever = qdrant.as_retriever(
        search_kwargs={
            "filter": {
                "must": [
                    {"key": "pdf_id", "match": {"value": str(pdf_id)}}
                ]
            }
        }
    )
    retriever = qdrant.as_retriever()
    # FAISS().+
    # retriever = vector_store.as_retriever()
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.3)

    # return RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=retriever,
    #     return_source_documents=True
    # )
    # return qdrant
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=qdrant.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,  # Optionally return the source chunks used
    )
    return qa_chain


def query_pdf_chunks(pdf_id: str, question: str):
    # chain = create_qa_chain(pdf_id)
    vector_store = create_qa_chain_simple(pdf_id=pdf_id)
    # result = chain({
    #     "query": question,
    #     # "semantic_context": {},  # or whatever your app expects
    #     # "auth_context": {},    
    # })
    result = vector_store.invoke({"query": question})
    # found_docs = vector_store.similarity_search(question)
    # print(found_docs, 'found docs...........................................')
    # found_docs['sources'] = []
    # return found_docs, "something else"
    return result["result"], result.get("source_documents", [])
import tempfile

def load_and_split_pdf(file: UploadFile, pdf_id: int):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")

    # Load and split using proper LangChain tools
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(documents)
    print("Creating FAISS vector store (in memory)...")
    # vector_store = FAISS.from_documents(split_docs, embeddings)
    print("Vector store created.")
    # Add pdf_id metadata to each chunk
    for doc in split_docs:
        doc.metadata["pdf_id"] = str(pdf_id)

    return split_docs


