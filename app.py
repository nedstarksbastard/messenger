from flask import Flask, jsonify, make_response, redirect, render_template, request, session, url_for
import os
import sqlite3
import settings
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config.from_object(settings)
socketio = SocketIO(app)

if not os.path.exists(app.config['DATABASE']):
    try:
        conn = sqlite3.connect(app.config['DATABASE'])

        # Absolute path needed for testing environment
        sql_path = os.path.join(app.config['APP_ROOT'], 'db_init.sql')
        cmd = open(sql_path, 'r').read()
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
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        q = "INSERT INTO messages VALUES (NULL, datetime('now'),?,?)"
        c.execute(q, (message, sender))
        conn.commit()
        return c.lastrowid


# Helper functions
def _get_message(id=None):
    """Return a list of message objects (as dicts)"""
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()

        if id:
            id = int(id)  # Ensure that we have a valid id value to query
            q = "SELECT * FROM messages WHERE id=? ORDER BY dt DESC"
            rows = c.execute(q, (id,))

        else:
            q = "SELECT * FROM messages ORDER BY dt DESC"
            rows = c.execute(q)

        return [{'id': r[0], 'dt': r[1], 'message': r[2], 'sender': r[3]} for r in rows]

@socketio.on('socket_init')
def socket_init(message):
    print('received message: ' + message['data'])


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        add_message(request.form['message'], session['username'])
        redirect(url_for('home'))

    return render_template('index.html', messages=_get_message(), user=session['username'])



def add_message(message, sender):
    # message = request.args['message']
    # sender = request.args['sender']  # if key doesn't exist, returns a 400, bad request error
    # website = request.args.get('website') if key doesn't exist, returns None

    id = _add_message(message, sender)
    if id:
        emit('new_msg', _get_message(id)[0], namespace='/', broadcast=True)
    return make_response(jsonify({'success': True}), 200)


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = _get_message()
    if not messages:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return jsonify({'messages': messages})





@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    socketio.run(app)
