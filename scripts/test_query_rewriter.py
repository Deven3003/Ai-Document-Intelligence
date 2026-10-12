from src.api.app import ConversationMessage
from src.generation.query_rewritter import rewrite_question

history =[
    ConversationMessage(
        role="user",
        content="What is the vacation policy ?"
    ),
    ConversationMessage(
        role="assistant",
        content="Employee recive vaction based on their years of experince."
    )
]

question ="what about after 5 years ?"

rewritten_question=rewrite_question(
    question,
    history
) 

print("\nOriginal question:")
print(question)
print("\nRewritten Question:")
print(rewritten_question)