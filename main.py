from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from flask_socket-io import SocketIO,
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(msg):
    print(msg)
    send(msg, broadcast=True)

@app.route("/")
def index():
   return render_template('index.html')


if __name__ == "__main__":
    socketio.run(host='0.0.0.0', debug=True)
