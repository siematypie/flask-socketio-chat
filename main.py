from flask import Flask, render_template, request, url_for, redirect, flash, session, abort, jsonify
from flask_socketio import SocketIO, send, emit, join_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['DEBUG'] = True
socketio = SocketIO(app)
ids = []
test = [1,2,3,4,5]

@socketio.on('join')
def on_join():
    ids.append(request.sid)
    room = "hehe"
    join_room(room)
    # print(request.sid);
    emit('userLoggedIn',ids[-1], room=room)


@socketio.on('connect', namespace='/')
def test_connect():
    ids.append(request.sid)
    print("connectiooon" + request.sid)
    emit('connectedUserChange', {"data": ids}, broadcast=True)
    # emit('message', "User is connected")

@socketio.on('disconnect')
def test_disconnect():
    ids.remove(request.sid)
    emit('connectedUserChange', {"data": ids}, broadcast=True)
    print("DISCONNECTED " + request.sid)


@app.route("/")
def index():
   return render_template("bla.html")


@socketio.on('message', namespace="/")
def handle_message(msg, user="User"):
    msg = "<dt>{}</dt><dl>{}<dl>".format(user, msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
