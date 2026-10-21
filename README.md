# UniBot — AI University Chatbot

UniBot is an AI-powered university document chatbot that answers student queries using information retrieved from university PDF documents. Built with **Python, Retrieval-Augmented Generation (RAG), ChromaDB, and the Groq API**, it combines semantic search with a large language model (LLM) to generate context-based answers with source document and page references.

## Features

- **PDF Processing:** Extracts text from university documents using PyPDF.
- **Text Chunking:** Splits extracted text into overlapping chunks for retrieval.
- **Semantic Search:** Uses ChromaDB to retrieve relevant document chunks through embeddings.
- **AI-Powered Responses:** Integrates the Groq API with an LLM to generate context-grounded answers.
- **Source References:** Displays source filenames and page numbers for retrieved content.
- **Interactive Chat Interface:** Provides a Streamlit chat interface with session-based chat history.
- **Fallback Responses:** Instructs the model to indicate when information cannot be found in the provided context.
- **Local Vector Storage:** Stores document embeddings and metadata in a persistent ChromaDB collection.

## Tech Stack

- **Language:** Python
- **RAG Framework:** Custom RAG pipeline
- **Vector Database:** ChromaDB
- **Embeddings:** ChromaDB Default Embedding Function
- **LLM Integration:** Groq API
- **LLM Model:** `openai/gpt-oss-20b`
- **Frontend:** Streamlit
- **PDF Extraction:** pypdf
- **Environment Configuration:** python-dotenv

## How It Works

UniBot follows a Retrieval-Augmented Generation (RAG) workflow:

1. **Document Ingestion:** Reads university PDF files and extracts text page by page.
2. **Text Chunking:** Splits extracted text into chunks of 150 words with a 30-word overlap.
3. **Embedding and Indexing:** ChromaDB generates embeddings and stores the chunks with source filenames and page numbers.
4. **Semantic Retrieval:** Retrieves the four most relevant chunks for a user's question.
5. **Context Augmentation:** Combines the retrieved document content with the user's question.
6. **Answer Generation:** Sends the context to the Groq-hosted LLM to generate a response.
7. **Source Display:** Displays retrieved sources and page references alongside the answer.

## Project Structure

```text
UniBot/
├── chroma_db/          # Local ChromaDB vector storage
├── data/               # University PDF documents
├── app.py              # Streamlit chat interface
├── rag.py              # Retrieval and answer generation
├── ingest.py           # PDF extraction, chunking, and indexing
├── search_test.py      # Retrieval testing
├── hello_groq.py       # Groq API connectivity test
├── requirements.txt    # Python dependencies
├── .env                # API key configuration (not committed)
└── .gitignore          # Git exclusions
```

The `chroma_db/` directory is generated local storage and can be rebuilt from the PDFs. The `.env` file contains secrets and must never be committed to GitHub.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version
- A Groq API key
- University PDF documents to index

### 1. Clone the Repository

```bash
git clone https://github.com/vikastyagi2004/UniBot.git
cd UniBot
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get an API key from the [Groq Console](https://console.groq.com/).

**Security:** Never upload your `.env` file or expose your API key in source code, screenshots, or public repositories.

### 5. Add University Documents

Place your PDF files inside the `data/` directory.

Example:

```text
data/
└── student_handbook.pdf
```

UniBot processes PDFs that contain extractable text. Scanned documents may require OCR.

### 6. Build the Vector Index

Run the ingestion script:

```bash
python ingest.py
```

The script extracts PDF text, creates overlapping chunks, and stores them in the local ChromaDB collection.

Example output:

```text
Read 11 pages -> stored 22 chunks.
```

The number of pages and chunks depends on your PDF documents.

### 7. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

You can now ask questions based on the indexed university documents.

## Testing and Debugging

UniBot includes utility scripts for testing individual components:

- **`hello_groq.py`** — Checks Groq API connectivity.
- **`search_test.py`** — Tests document retrieval and helps inspect relevant chunks.
- **`ingest.py`** — Rebuilds the vector index from the available PDFs.

Run a script with:

```bash
python search_test.py
```

Use the questions whose answers are present in your documents to evaluate retrieval relevance and response accuracy.

## Deployment

UniBot can be deployed using [Streamlit Community Cloud](https://share.streamlit.io/).

### Deployment Steps

1. Push the application code and required PDF documents to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Create an app and select your repository, branch, and `app.py` entry point.
4. Add `GROQ_API_KEY` in the app's Streamlit Secrets settings:

   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   ```

5. Deploy the application and check the logs for errors.

### Deployment Notes

- Include the required PDFs in the repository if the app builds its index from local files.
- Configure the application to initialize the ChromaDB collection before retrieval.
- The local ChromaDB index is not guaranteed to persist across cloud environment rebuilds.
- For production use, consider a persistent or externally hosted vector database.
- Never commit API keys or `.env` files.

## Current Limitations

- Answer quality depends on the relevance and quality of the indexed documents.
- Scanned PDFs without extractable text are not supported without OCR.
- Vague questions may retrieve less relevant chunks.
- Information split across different chunks may be missed.
- Chat history is displayed within the Streamlit session, but previous messages are not currently passed into the RAG pipeline for contextual follow-up questions.
- The model is instructed to answer from retrieved context, but this does not guarantee that every response is hallucination-free.
- Local vector storage is suitable for experimentation, not reliable long-term production persistence on temporary cloud storage.

## Future Improvements

- Add contextual query rewriting for follow-up questions.
- Introduce similarity thresholds to reduce irrelevant retrieval.
- Evaluate retrieval quality using metrics such as Recall@K.
- Explore hybrid search combining semantic and keyword retrieval.
- Add OCR support for scanned PDF documents.
- Improve error handling, logging, and response-time monitoring.
- Use persistent vector storage for reliable cloud deployment.
- Add automated tests for retrieval accuracy and hallucination resistance.

## Author

**Vikas Tyagi**

- GitHub: [vikastyagi2004](https://github.com/vikastyagi2004)

## License

This project is intended for learning and demonstration. Add a `LICENSE` file if you want to distribute it under a specific open-source license.

---

*UniBot demonstrates a custom Retrieval-Augmented Generation pipeline using PDF ingestion, semantic search, vector storage, and LLM integration for university document question answering.*
