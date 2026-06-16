## Demo Video
https://github.com/user-attachments/assets/6696cd56-62b4-4e90-a8a2-716d041c280f







# AI Knowledge Assistant

An AI-powered Knowledge Assistant that enables users to upload documents and ask questions in natural language. The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate accurate answers based on document content.

## Features

✅ Upload multiple document formats
- PDF
- DOCX
- TXT
- CSV

✅ Intelligent Question Answering

✅ Semantic Search using Vector Embeddings

✅ Source Citation Display

✅ Retrieval-Augmented Generation (RAG)

✅ User-Friendly Streamlit Interface

## How It Works

1. User uploads documents.
2. Documents are processed and split into chunks.
3. Chunks are converted into vector embeddings.
4. Embeddings are stored in ChromaDB.
5. User asks a question.
6. Relevant chunks are retrieved.
7. Gemini generates an answer using retrieved context.
8. Sources used for the answer are displayed.

## Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini API
- HuggingFace Embeddings
- ChromaDB
- RAG Architecture

## Project Structure

AI-Knowledge-Assistant/
│

├──app.py

├── requirements.txt

├── chroma_db/

├── README.md


## Installation

pip install -r requirements.txt

## Run

streamlit run app.py

## Future Enhancements

- Conversation Memory
- Multi-Document Comparison
- Voice Input
- Document Summarization
- Hybrid Search
- Authentication System

## Screenshots
<img width="1917" height="901" alt="ai knowledge assisstant" src="https://github.com/user-attachments/assets/69b8bc39-079a-4e9c-8c79-90f7d1d8641a" />

