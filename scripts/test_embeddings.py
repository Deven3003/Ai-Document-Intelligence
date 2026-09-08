from src.embeddings.embeddings_service import create_embeddings

text ="what is the leave policy ?"

embedding = create_embeddings(text)

print(type(embedding))
print("diemension",len(embedding))
print("first 10 values ::",embedding[:10])