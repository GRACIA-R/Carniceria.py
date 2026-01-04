import sqlite3
import os

DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "carniceria.db")

SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

@st.cache_resource
def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()


def get_connection():
    if not os.path.exists(DB_PATH):
        init_db()

    return sqlite3.connect(DB_PATH, check_same_thread=False)
