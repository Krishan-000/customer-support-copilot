

from langchain_community.document_loaders import ( TextLoader , PyPDFLoader )
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from pathlib import Path



documents = []

data_path = Path("data")

for txt_file in data_path.glob("*.txt"):

    loader = TextLoader(
        str(txt_file),
        encoding="utf-8"
    )

    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = txt_file.name

    documents.extend(docs)

for pdf_file in data_path.glob("*.pdf"):

    loader = PyPDFLoader(
        str(pdf_file)
    )

    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = pdf_file.name

    documents.extend(docs)

print(f"Loaded {len(documents)} documents")    

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")

docs = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(
    docs,
    embeddings
)

db.save_local("vectordb")

print("Database Created Successfully!")