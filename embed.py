from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

print("🔄 Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

documents = []
doc_names = []

print("📄 Reading files...")

for file in os.listdir("data"):
    with open(f"data/{file}", "r") as f:
        text = f.read()
        documents.append(text)
        doc_names.append(file)

print("🧠 Creating embeddings...")
embeddings = model.encode(documents)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

faiss.write_index(index, "vector.index")

with open("docs.pkl", "wb") as f:
    pickle.dump((documents, doc_names), f)

print("✅ Embeddings created successfully!")

