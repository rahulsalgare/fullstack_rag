from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

from qdrant_client import QdrantClient, models
# from .openai_utils import get_embedding
# from decouple import config
from dotenv import load_dotenv

load_dotenv()

collection_name = "Websites"
client = QdrantClient(url="http://localhost:6333")

vector_store = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=OpenAIEmbeddings()
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)

def create_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
    )
    print(f"Collection {collection_name} created successfully")


def upload_website_to_collection(url: str):
    if not client.collection_exists(collection_name=collection_name):
        create_collection(collection_name)

    loader = WebBaseLoader(url)
    docs = loader.load_and_split(text_splitter)
    for doc in docs:
        doc.metadata = {"source_url": url}

    vector_store.add_documents(docs)
    return f"Successfully uploaded {len(docs)} documents to collection {collection_name} from {url}"


if __name__ == '__main__':
    url = "https://medium.com/@saikikeshi/you-are-not-everyones-cup-of-tea-and-that-s-okay-93ac9d0309ef"
    upload_website_to_collection(url)