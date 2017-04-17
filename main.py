from flask import Flask, render_template, request, url_for, redirect, flash, session, abort, jsonify
from flask_socketio import SocketIO, send, emit, join_room, disconnect
import os
import eventlet
import jinja2

eventlet.monkey_patch
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
socketio = SocketIO(app)
users = {}

@socketio.on('join')
def on_join(name):
    users[request.sid] = name
    room = "hehe"
    join_room(room)
    print(users)
    emit('message', "{} has connected!".format(name), broadcast=True)
    emit('connectedUserChange', {'data':list(users.values())}, room=room)

    @socketio.on('disconnect')
    def test_disconnect():
        if request.sid in users:
            del users[request.sid]
            emit('connectedUserChange', {"data": list(users.values())}, broadcast=True)
        print("DISCONNECTED")

# @socketio.on('connect', namespace='/')
# def test_connect():
#     session['sid'] = request.sid
#     ids.append(request.sid)
#     print("connectiooon" + request.sid)
#     emit('connectedUserChange', {"data": ids}, broadcast=True)
#     # emit('message', "User is connected")


@socketio.on('disconnectMe')
def disconnect_user():
    emit('connectedUserChange', {"data": list(users.values())}, broadcast=True)
    emit('message', 'HEHEHE!', broadcast=True)


@socketio.on('checkSessionName')
def check_session_name():
    if 'name' in session:
        return session['name']


@app.route("/")
def index():
   return render_template("bla.html")


@socketio.on('message', namespace="/")
def handle_message(msg, user="User"):
    user = str(jinja2.escape(user))
    msg = str(jinja2.escape(msg))
    msg = "<dt>{}</dt><dd>{}<dd>".format(user, msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
