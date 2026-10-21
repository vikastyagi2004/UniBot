import os
from dotenv import load_dotenv
from groq import Groq
import chromadb
 
load_dotenv()
MODEL = "openai/gpt-oss-20b"
TOP_K = 4
 
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_collection("unibot")
 
SYSTEM_PROMPT = """You are UniBot, a helpful university assistant.
Answer ONLY using the context provided.
If the answer is not in the context, say:
"I couldn't find that in the university documents."
Keep answers short and mention the source file and page."""


# 1. RETRIEVE: find the top-k most similar chunks
def retrieve(question, k=TOP_K):
    results = collection.query(query_texts=[question], n_results=k)
    chunks = []
    for text, meta, dist in zip(results["documents"][0],
                                results["metadatas"][0],
                                results["distances"][0]):
        chunks.append({"text": text, "source": meta["source"],
                       "page": meta["page"], "distance": dist})
    return chunks
 
# 2. AUGMENT: put the chunks into the prompt
def build_prompt(question, chunks):
    context = "\n\n".join(
        f"[{c['source']}, page {c['page']}]\n{c['text']}" for c in chunks
    )
    return f"Context:\n{context}\n\nQuestion: {question}"


# 3. GENERATE: ask the LLM on Groq
def ask_llm(question, chunks):
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(question, chunks)},
        ],
        temperature=0.2,
        reasoning_effort="low",
        max_completion_tokens=1024,
    )
    return response.choices[0].message.content
 
def answer(question):
    chunks = retrieve(question)
    return ask_llm(question, chunks), chunks

if __name__ == "__main__":
    question = input("Ask UniBot: ")
    reply, chunks = answer(question)
    print("\n" + reply + "\n\nSources:")
    for c in chunks:
        print(f"- {c['source']} p{c['page']} (distance {c['distance']:.2f})")
