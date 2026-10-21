# import os
# from pypdf import PdfReader
# import chromadb
 
# DATA_DIR = "data"
# DB_DIR = "chroma_db"
# COLLECTION = "unibot"
 
# # STEP 4: read every PDF, page by page
# def load_pdfs(folder):
#     pages = []
#     for filename in sorted(os.listdir(folder)):
#         if not filename.lower().endswith(".pdf"):
#             continue
#         reader = PdfReader(os.path.join(folder, filename))
#         for num, page in enumerate(reader.pages, start=1):
#             text = page.extract_text() or ""
#             if text.strip():
#                 pages.append({"text": text, "source": filename, "page": num})
#     return pages

# # STEP 5: split text into overlapping chunks of words
# def chunk_text(text, chunk_size=150, overlap=30):
#     words = text.split()
#     chunks = []
#     step = chunk_size - overlap
#     for start in range(0, len(words), step):
#         chunks.append(" ".join(words[start:start + chunk_size]))
#         if start + chunk_size >= len(words):
#             break
#     return chunks

# # STEP 6: store all chunks in Chroma
# def build_index():
#     pages = load_pdfs(DATA_DIR)
 
#     ids, documents, metadatas = [], [], []
#     for p in pages:
#         for i, chunk in enumerate(chunk_text(p["text"])):
#             ids.append(f"{p['source']}-p{p['page']}-c{i}")
#             documents.append(chunk)
#             metadatas.append({"source": p["source"], "page": p["page"]})
 
#     client = chromadb.PersistentClient(path=DB_DIR)
#     # start fresh each time we run ingest
#     if COLLECTION in [c.name for c in client.list_collections()]:
#         client.delete_collection(COLLECTION)
#     collection = client.create_collection(COLLECTION)
 
#     collection.add(ids=ids, documents=documents, metadatas=metadatas)
#     print(f"Read {len(pages)} pages -> stored {len(documents)} chunks.")
 
# if __name__ == "__main__":
#     build_index()



from pathlib import Path
from pypdf import PdfReader
import chromadb

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"
COLLECTION = "unibot"


def load_pdfs(folder):
    if not folder.exists():
        raise FileNotFoundError(
            f"PDF folder not found: {folder}"
        )

    pages = []

    for file_path in sorted(folder.iterdir()):
        if file_path.suffix.lower() != ".pdf":
            continue

        reader = PdfReader(str(file_path))

        for num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                pages.append({
                    "text": text,
                    "source": file_path.name,
                    "page": num,
                })

    if not pages:
        raise ValueError(
            "No readable PDF pages found in the data folder."
        )

    return pages


def chunk_text(text, chunk_size=150, overlap=30):
    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size])

        if chunk.strip():
            chunks.append(chunk)

        if start + chunk_size >= len(words):
            break

    return chunks


def build_index():
    pages = load_pdfs(DATA_DIR)

    ids, documents, metadatas = [], [], []

    for page in pages:
        for i, chunk in enumerate(chunk_text(page["text"])):
            ids.append(
                f"{page['source']}-p{page['page']}-c{i}"
            )
            documents.append(chunk)
            metadatas.append({
                "source": page["source"],
                "page": page["page"],
            })

    if not documents:
        raise ValueError("No text chunks were generated from PDFs.")

    client = chromadb.PersistentClient(path=str(DB_DIR))

    existing = client.list_collections()
    names = [
        c if isinstance(c, str) else c.name
        for c in existing
    ]

    if COLLECTION in names:
        client.delete_collection(COLLECTION)

    collection = client.create_collection(COLLECTION)

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    print(
        f"Read {len(pages)} pages -> "
        f"stored {len(documents)} chunks."
    )

    return len(documents)


if __name__ == "__main__":
    build_index()
