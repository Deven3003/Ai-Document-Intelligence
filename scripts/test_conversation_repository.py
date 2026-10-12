from src.repositories.conversation_repository import create_conversation,save_message,get_message

comversation_id = create_conversation(
    user_id =1,
    title ="Employee handbook questions "
)

print("Conversation created successfully")
print("Conversation ID:",comversation_id)

save_id =save_message(
    conversation_id=comversation_id,
    role="user",
    content="what is the employee leave policy ?"
)

print("Message saved successfully..for role user")

save_id =save_message(
    conversation_id=comversation_id,
    role="Assistant",
    content="Employees are entitled to 5 days leave policy in year"
)

messages = get_message(comversation_id)

for message in messages:
    print(message)