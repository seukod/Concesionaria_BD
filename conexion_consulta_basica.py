import psycopg2

conn = psycopg2.connect(
    host= "aws-0-sa-east-1.pooler.supabase.com",
    password= "0NzSHHo6Ee9Hl4BI",
    port = "5432",
    database = "postgres",
    user= "postgres.qdxsvygmfuqrrcaisqvw"
)

cursor = conn.cursor()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
print(cursor.fetchall())

conn.close()
