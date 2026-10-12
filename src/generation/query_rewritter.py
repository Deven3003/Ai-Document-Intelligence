from src.services.logger import get_logger
from src.generation.llm_service import generate_answer

logger =get_logger(__name__)

def rewrite_question(question:str,conversation_history:str)->str:
    if not conversation_history:
        return question

    history_text=""

    for message in conversation_history:
        history_text +=(f"{message['role']}:{message['content']}\n")

    prompt =f"""
you are a question re-writting assistant.
your task is to answer users current question into a standalone question that would be understood without the conversation history

use the conversation history only when current question depends on previous messages.

Do not answer the question.
Do not provide explanations.
Return only the rewritten standalone question.

Conversation history:
---------------------
{history_text}
---------------------

current_question:
{question}

standalone question:
"""

    rewritten_question =generate_answer(prompt)

    return rewritten_question 