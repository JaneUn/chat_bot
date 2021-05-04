import sqlite3

con = sqlite3.connect('chatbot.db')


def init_db():
    with con:
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, start_datetime timestamp, end_datetime timestamp)")
        cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, time timestamp, session_id INTEGER, text CHAR[400], client_id INTEGER)")

def write_message(time, text, session, client):
    with con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO messages (time, session_id, text, client_id) VALUES(?, ?, ?, ?)", (time, text, session, client))


def write_session(start_time):
    start_time = str(start_time)
    with con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO sessions (start_datetime) VALUES(?)", (start_time,))


def close_session(session_id, end_time):
    end_time = str(end_time)
    with con:
        cursor = con.cursor()
        cursor.execute("UPDATE sessions SET end_datetime=? WHERE id=?", (end_time, session_id))
        con.commit()


def get_current_session():
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT id FROM sessions ORDER BY id DESC")
        return cursor.fetchone()[0]
