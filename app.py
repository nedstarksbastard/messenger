from flask import Flask, jsonify, make_response, redirect, render_template, request, session, url_for
import os
import settings
from flask_socketio import SocketIO, emit
from helpers import _add_message, _get_message, init_db

app = Flask(__name__)
app.config.from_object(settings)
socketio = SocketIO(app)

if not os.path.exists(app.config['DATABASE']):
    with app.app_context():
        init_db()


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        add_message(request.form['message'], session['username'])
        redirect(url_for('home'))

    return render_template('index.html', messages=_get_message(), user=session['username'])


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


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = _get_message()
    if not messages:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return jsonify({'messages': messages})


@socketio.on('socket_init')
def socket_init(message):
    print('received message: ' + message['data'])


@socketio.on('disconnect')
def disconnect_user():
    print('Socket disconnect')
    session.clear()


# @socketio.on('logout')
# def logout_user():
#     print('Logout user')
#     session.clear()
#     emit('redirect', '/login')
#     return redirect(url_for('home'))


def add_message(message, sender):
    msg_id = _add_message(message, sender)
    if msg_id:
        emit('new_msg', _get_message(msg_id)[0], namespace='/', broadcast=True)
    return make_response(jsonify({'success': True}), 200)


if __name__ == '__main__':
    socketio.run(app)
