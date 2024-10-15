import sqlite3

"""
YGO PRO API NOTE:
Rate Limiting on the API is enabled. 
The rate limit is 20 requests per 1 second. 
If you exceed this, you are blocked from accessing the API for 1 hour. 
We will monitor this rate limit for now and adjust accordingly.
"""

def connect_db():
    con = sqlite3.connect("cards.db")
    cursor = con.cursor()
    create_query = """create table IF NOT exists "Cards"(
                    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "NAME" TEXT,
                    "TYPE" TEXT,
                    "TCG_DATE" TEXT,
                    "OCG_DATE" TEXT
                    );"""
    cursor.execute(create_query)