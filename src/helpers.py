from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain.schema import Document

# Extract data from PDF files
def load_pdf_file(data):
    loader = DirectoryLoader(data,
                            glob = "*.pdf",
                            loader_cls=PyPDFLoader
                            )
    documents = loader.load()
    return documents

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    
    """Filters documents to only include page content and metadata."""
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src} 
            )
        )
    return minimal_docs

def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    text_chunck = text_splitter.split_documents(minimal_docs)
    return text_chunck

def download_embeddings():
    """ 
    Download and return the HuggingFace embeddings mode
    """

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name = model_name
    )
    return embeddings

embedding = download_embeddings()