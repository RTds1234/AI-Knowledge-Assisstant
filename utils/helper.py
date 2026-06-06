import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

import streamlit as st 

# ===========================================
# Embeddings
# ===========================================
@st.cache_resource

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# ============================================
# Vector Database
# ============================================

@st.cache_resource

def get_db():
    embeddings=get_embeddings()
    
    db=Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return db

# ============================================
#Gemini Model
# ============================================

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )

# ============================================
#FIle LOader
# ============================================
def get_loader(file_path):
    ext=os.path.splitext(file_path)[1].lower()
    
    if ext==".pdf":
        return PyPDFLoader(file_path)
    elif ext==".txt":
        return TextLoader(file_path,encoding="utf-8")
    elif ext==".csv":
        return CSVLoader(file_path)
    elif ext==".docx":
        return Docx2txtLoader(file_path)
    elif ext==".md":
        return TextLoader(file_path,encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {ext}")



# ============================================
# PROCESS FILES
# ============================================

def process_files(uploaded_files):
    db=get_db()
    all_docs=[]
    
    for uploaded_file in uploaded_files:
        
        extension=os.path.splitext(
            uploaded_file.name)[1]
        
        with tempfile.NamedTemporaryFile(
            delete=False,suffix=extension) as temp_file:
            
            temp_file.write(
                uploaded_file.read())
            
            temp_path=temp_file.name
            
        loader=get_loader(temp_path)
        docs=loader.load()
        
        for doc in docs:
            doc.metadata[
                "source_file"]=uploaded_file.name
            
            doc.metadata[
                "file_type"
                
            ]=extension
            
        all_docs.extend(docs)
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1500,    
        chunk_overlap=200
    )
    
    chunks=splitter.split_documents(all_docs)
    db.add_documents(chunks)
    return len(chunks)


# ============================================
# REwrite question with chat history
# ============================================
def rewrite_question(question, history_text):

    llm = get_llm()

    rewrite_prompt = f"""
You are a query rewriting assistant.

Your job is to convert the user's latest
question into a standalone question.

Examples:

History:
user: What is Machine Learning?

Question:
Can you elaborate it?

Standalone Question:
Can you elaborate on Machine Learning?

------------------------

History:
{history_text}

Question:
{question}

Standalone Question:
"""

    response = llm.invoke(rewrite_prompt)

    return response.content.strip()
# ============================================
# Question answering
# ============================================

def ask_question(
    question,
    chat_history
):

    db = get_db()

    retriever = db.as_retriever(
        search_kwargs={"k": 5}
    )

    # ======================
    # Build chat history
    # ======================

    history_text = ""

    for msg in chat_history[-6:]:

        history_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    # ======================
    # Rewrite question
    # ======================

    standalone_question = rewrite_question(
        question,
        history_text
    )

    print("\n===== REWRITTEN QUESTION =====")
    print(standalone_question)

    # ======================
    # Retrieve documents
    # ======================

    docs = retriever.invoke(
        standalone_question
    )

    print("\n===== RETRIEVED DOCS =====")

    for i, doc in enumerate(docs):

        print(f"\n--- DOC {i+1} ---")

        print(doc.page_content[:500])

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # ======================
    # Final prompt
    # ======================

    prompt = f"""
You are a helpful AI Assistant.

Use ONLY the provided context.

If answer is unavailable say:

Information not found in uploaded documents.

Conversation:
{history_text}

Context:
{context}

Question:
{standalone_question}
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    # ======================
    # Sources
    # ======================

    sources = []

    for doc in docs:

        file_name = doc.metadata.get(
            "source_file",
            "Unknown"
        )

        file_type = doc.metadata.get(
            "file_type",
            ""
        )

        page = doc.metadata.get(
            "page",
            None
        )

        if page is not None:

            source = (
                f"{file_name}"
                f" ({file_type})"
                f" | Page {page+1}"
            )

        else:

            source = (
                f"{file_name}"
                f" ({file_type})"
            )

        if source not in sources:

            sources.append(source)

    return (
        response.content,
        sources
    )