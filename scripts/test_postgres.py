import psycopg

connection =psycopg.connect(
    host="localhost",
    port=5432,
    dbname="ai_document_intelligence",
    user="postgres",
    password="Devpingale@123"
)

print("PostGraceSQL connection successfull !!")

connection.close()