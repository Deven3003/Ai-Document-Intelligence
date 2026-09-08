from groq import Groq
from src.config import settings

print("API KEY LOADED::",bool(settings.GROQ_API_KEY))
client =Groq(api_key=settings.GROQ_API_KEY)
print("Client Added Successfully....!")

def generate_answer(prompt):
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

    return answer