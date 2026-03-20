from sentence_transformers import SentenceTransformer
import faiss
import pickle
import ollama

model = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.read_index("vector.index")

with open("docs.pkl", "rb") as f:
    documents, doc_names = pickle.load(f)

def retrieve(query, k=2):
    query_vec = model.encode([query])
    D, I = index.search(query_vec, k)
    
    results = []
    for i in I[0]:
        results.append((documents[i], doc_names[i]))
    
    return results

def generate_answer(query, context_docs):
    context = "\n\n".join([doc for doc, _ in context_docs])

    prompt = f"""
Answer ONLY using the context below.

Context:
{context}

Question:
{query}
"""

    response = ollama.chat(
        model='mistral',
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']
