from src.rag_service import initialize_rag,ask_question

initialize_rag()

print("\n RAG service test successful!")

question =input("Ask Your Question::::  ")

answer = ask_question(
    question
)

print("\n======================================================-")
print("QUESTION::")
print(question)

print("\nANSWER::")
print(answer)
print("\n=======================================================")