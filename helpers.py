import sqlite3
import os
from flask import current_app


def init_db():
    try:
        conn = sqlite3.connect(current_app.config['DATABASE'])
        sql_path = os.path.join(current_app.config['APP_ROOT'], 'db_init.sql')
        with open(sql_path, 'r') as f:
            cmd = f.read()
        crsr = conn.cursor()
        crsr.execute(cmd)
        conn.commit()
        conn.close()
    except IOError:
        print("Couldn't initialize the database, exiting...")
        raise
    except sqlite3.OperationalError:
        print("Couldn't execute the SQL, exiting...")
        raise


def _add_message(message, sender):
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        c = conn.cursor()
        q = "INSERT INTO messages VALUES (NULL, datetime('now'),?,?)"
        c.execute(q, (message, sender))
        conn.commit()
        return c.lastrowid


def _get_message(msg_id=None):

    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        c = conn.cursor()

        if msg_id:
            msg_id = int(msg_id)  # Ensure that we have a valid id value to query
            q = "SELECT * FROM messages WHERE id=? ORDER BY dt DESC"
            rows = c.execute(q, (msg_id,))

        else:
            q = "SELECT * FROM messages ORDER BY dt"
            rows = c.execute(q)

        return [{'id': r[0], 'dt': r[1], 'message': r[2], 'sender': r[3]} for r in rows]