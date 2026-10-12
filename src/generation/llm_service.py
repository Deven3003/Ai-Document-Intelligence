from groq import Groq
from src.config import settings
from src.services.logger import get_logger

logger =get_logger(__name__)
print("API KEY LOADED::",bool(settings.GROQ_API_KEY))
client =Groq(api_key=settings.GROQ_API_KEY)
print("Client Added Successfully....!")

def generate_answer(prompt):
    try:
        response =client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        answer =response.choices[0].message.content

        logger.info("LLM Answer generated successfully")

        return answer
    except Exception:
        logger.exception("LLM generation failed")
        raise