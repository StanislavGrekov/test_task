import psycopg2

DB_NAME='bank_db'
DB_USER = 'postgres'
DB_PASSWORD='masterkey'

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()

