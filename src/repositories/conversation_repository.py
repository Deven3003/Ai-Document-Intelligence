from src.database.database import get_connection

def create_conversation(user_id: int,title:str | None = None) ->int:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """Insert into conversation (user_id,title)
                values(%s,%s)
                Returning id;
                """,
                (user_id,title)
            )

            conversation_id =cursor.fetchone()[0]

        connection.commit()

        return conversation_id

    finally:
        connection.close()


def save_message(
    conversation_id:int,
    role:str,
    content:str
)-> int:

    connection =get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO conversation_message
                (conversation_id,
                role,
                content)
                VALUES
                (%s,%s,%s)
                returning id;""",
                (conversation_id,role,content)
            )

            message_id =cursor.fetchone()[0]

        connection.commit()

        return message_id

    finally:
        connection.close()   


def get_message(conversation_id:int)->list[dict]:
    connection =get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """select role,content
                    from conversation_message
                    where conversation_id=%s
                    ORDER BY created_at asc;
                    """,(conversation_id,)
            )

            rows =cursor.fetchall()

            message =[]

            for role,content in rows:
                message.append({
                    "role":role,
                    "content":content
                })

            return message

    finally:
        connection.close
