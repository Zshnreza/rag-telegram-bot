from rag import retrieve, generate_answer

query = "What are working hours?"

docs = retrieve(query)
answer = generate_answer(query, docs)

print("\nAnswer:\n", answer)

print("\nSources:")
for _, name in docs:
    print("-", name)
