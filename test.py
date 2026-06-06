from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

docs = db.similarity_search(
    "What is machine learning?",
    k=3
)

print("Docs found:", len(docs))

for i, doc in enumerate(docs):
    print(f"\n===== DOC {i+1} =====")
    print(doc.page_content[:500])