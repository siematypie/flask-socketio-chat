from flask import Flask, render_template, request, url_for, redirect, flash, session, abort, jsonify
from flask_socketio import SocketIO, send, emit, join_room, disconnect
import os
import jinja2
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['DEBUG'] = True
socketio = SocketIO(app)
sessions_ids = {"hehe":3}
users = {}


# @socketio.on('addSessionAndJoin')
# def on_join(name):
#     print("I'm working")
#
#
#     session['name'] = name
#     users[name] = [request.sid]
#     emit('connectedUserChange', {"data": list(users)}, broadcast=True)
#     print(session['id'])
#     print(session['name'] )
#
#     # if name in sessions_ids:
#     #     if 'name' in session and id in session:
#     #         if all_sessions[name]
#     # session['name'] = name
#     #
#     # if name in users:
#     #     users[name].append(request.sid)
#     # else:
#     #     users[name] = [request.sid]
#     # emit('message', "{} has connected!".format(name), broadcast=True)
#     # emit('connectedUserChange', {'data':list(users)})


@socketio.on('connect')
def test_connect():
    if 'name' in session:
        print(sessions_ids)
        print(users)
        print(session['name'])
        session_name = session['name']
        session_id = session['id']

        if session_name in sessions_ids and session_id != sessions_ids[session_name]:
            msg = "ERROR! Name '{}' you used before is alerady in use by someone else! Please choose different one!".format(session_name)
            emit('loginNeeded', msg , room=request.sid)
            return
        elif session_name not in sessions_ids:
            sessions_ids[session_name] = session_id

        join_room('general')
        if session_name in users:
            users[session_name].append(request.sid)
        else:
            users[session_name] = [request.sid]
        emit('connectedUserChange', {"data": list(users)}, broadcast=True)
        emit('joinSuccessful')
    else:
        print('hehe')
        emit('loginNeeded', room=request.sid)

    @socketio.on('disconnect')
    def test_disconnect():
        print('DISCOOOOO')
        if 'name' in session:
            session_name = session['name']
            if session_name in users:
                sid_list = users[session_name]
                if sid_list:
                    if request.sid in sid_list:
                        if len(sid_list) == 1:
                            del users[session_name]
                            del sessions_ids[session_name]
                        else:
                            sid_list.remove(request.sid)


            emit('connectedUserChange', {"data": list(users)}, broadcast=True)


def append_sid_to_users(name):
    pass
# @socketio.on('connect', namespace='/')
# def test_connect():
#     session['sid'] = request.sid
#     ids.append(request.sid)
#     print("connectiooon" + request.sid)
#     emit('connectedUserChange', {"data": ids}, broadcast=True)
#     # emit('message', "User is connected")


# @socketio.on('disconnectMe')
# def disconnect_user():
#     emit('connectedUserChange', {"data": list(users.values())}, broadcast=True)
#     emit('message', 'HEHEHE!', broadcast=True)


@socketio.on('checkSessionName')
def check_session_name():
    if 'name' in session:
        return session['name']


@app.route("/")
def index():
    return render_template("bla.html")

@app.route("/session/<name>")
def set_session(name):
    session['name'] = name
    session['id'] = uuid.uuid4()
    name = str(jinja2.escape(name))
    return redirect(url_for('index'))


@socketio.on('message', namespace="/")
def handle_message(msg):

    msg = str(jinja2.escape(msg))
    msg = "<dt>{}</dt><dd>{}<dd>".format(session['name'], msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
