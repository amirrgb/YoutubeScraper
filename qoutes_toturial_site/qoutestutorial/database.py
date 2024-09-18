import sqlite3

conn = sqlite3.connect('myquotes.db')
curr = conn.cursor()

def create_table():
    curr.execute("""create table IF NOT EXISTS quotes_tb(
                title text,
                author text,
                tag text
                )""")
    conn.commit()
