def build_prompt(question, retrieved_chunks):
    context =""

    for result in retrieved_chunks:
        context += result["text"] + "\n\n"

        prompt =f"""
you are the corporate knowladge assistant.

Answer the user question using only the provided context.
if the answer could not find in the context , say :
"I Could not able to Find answer in the provided Document."

Context:
--------------------------
{context}
--------------------------

Question:
---------------------------
{question}
---------------------------

Answer:
"""
        return prompt