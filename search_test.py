import chromadb
 
db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_collection("unibot")
 
question = "What is the minimum attendance to sit for exams?"
results = collection.query(query_texts=[question], n_results=4)
 
for text, meta, dist in zip(results["documents"][0],
                            results["metadatas"][0],
                            results["distances"][0]):
    print(f"{dist:.2f} | {meta['source']} p{meta['page']} | {text[:80]}...")
