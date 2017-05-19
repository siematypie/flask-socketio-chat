import time
from threading import Thread
from flask import Flask, render_template, request, url_for, redirect, flash, session, abort, jsonify, g
from flask_socketio import SocketIO, send, emit, join_room, disconnect
import os
import eventlet
import jinja2
import uuid
from flask_cors import CORS


eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['DEBUG'] = True
cors = CORS(app,resources={r"/*":{"origins":"*"}}, support_credentials=True)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
sessions_ids = {"beka":"123"}
users_conns = {}
sids = {}
#
# def test():

# thread = Thread(target=test)
# thread.daemon = True
# thread.start()

@socketio.on('connect', namespace="/")
def test_connect():
    id = request.args.get('id')
    name = str(jinja2.escape(request.args.get('username')))
    if name in sessions_ids:
        if id != sessions_ids[name]:
            msg = "ERROR! Name '{}' you used before is already in use by someone else! Please choose different one!".format(name)
            emit('loginNeeded', msg, room=request.sid)
            disconnect()
            return

        join_room('general')
        if name in users_conns:
            users_conns[name] += 1
        else:
            users_conns[name] = 1

        sids[request.sid] = name
        emit('connectedUserChange', {"data": list(users_conns)}, broadcast=True)
        print("WORKIN")
        emit('joinSuccessful')
    else:
        print("JEJE")
        emit('loginNeeded', room=request.sid)
        disconnect()


    @socketio.on('disconnect')
    def test_disconnect():
        sid = request.sid
        if sid in sids:
            name = sids[sid]
            del sids[sid]
            users_conns[name] -= 1
            if users_conns[name] < 1:
                del users_conns[name]
                del sessions_ids[name]
        # if 'name' in session:
            # session_name = session['name']
            # if session_name in users:
            #     sid_list = users[session_name]
            #     if sid_list:
            #         if request.sid in sid_list:
            #             if len(sid_list) == 1:
            #                 del users[session_name]
            #                 del sessions_ids[session_name]
            #             else:
            #                 sid_list.remove(request.sid)


            emit('connectedUserChange', {"data": list(users_conns)}, broadcast=True)

# @socketio.on('connect', namespace='/')
# def test_connect():
#     session['sid'] = request.sid
#     ids.append(request.sid)
#     print("connectiooon" + request.sid)
#     emit('connectedUserChange', {"data": ids}, broadcast=True)
#     # emit('message', "User is connected")


# @socketio.on('disconnectMe')
# def disconnect_user()

@socketio.on('checkSessionName')
def check_session_name():
    if 'name' in session:
        return session['name']


@socketio.on('sendFile', namespace='/')
def handle_file(file_size, file_name, file_type, array_buffer):
    file_sender = sids[request.sid]
    file_dict = {"fileSize":file_size, "fileName":file_name, "fileSender":file_sender, "fileType":file_type, "arrayBuffer":array_buffer}
    emit('fileBroadcast',file_dict, broadcast=True)

@app.route("/")
def index():
    return render_template("bla.html")

@app.route("/getsession", methods=['POST'])
def set_session():
    user_data = request.json
    name = user_data['username']
    parsed_name =  str(jinja2.escape(name))
    if name in users_conns:
        return jsonify({"Error":
                        "ERROR! Name '{}' is already in use by someone else! Please choose different one!".format(name)}), 406

    id = str(uuid.uuid4())
    sessions_ids[parsed_name] = id

    return jsonify(
        username = name,
        id = id
    )

@app.route("/validate", methods=['POST'])
def validate_data():
    user_data = request.json

    if any(k not in user_data for k in ("id", "username")):
        return jsonify({"validation": False})

    name = str(jinja2.escape(user_data['username']))
    if name in sessions_ids and user_data["id"] != sessions_ids[name]:
        msg = "ERROR! Name '{}' you used before is already in use by someone else! Please choose different one!".format(
            name)
        return jsonify({"validation": False, "error":msg})

    sessions_ids[name] = user_data['id']
    return jsonify({"validation": True})

@app.route("/file", methods=['POST'])
def send_file():
    print(type(request.files['file'].read()))
    return jsonify({"result": "OK"})

def disconnect_with_delay(sid):
    with app.test_request_context('/'):
        time.sleep(7)
        socketio.server.disconnect(sid,
                                   namespace="/")


@socketio.on('message', namespace="/")
def handle_message(msg):
    msg = str(jinja2.escape(msg))
    msg = "<dt>{}</dt><dd>{}<dd>".format(sids[request.sid], msg)
    send(msg, broadcast=True)




@socketio.on('sendImg', namespace='/')
def handle_image(img):
    emit('imgBroadcast', img, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
