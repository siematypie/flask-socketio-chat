from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['DEBUG'] = True
socketio = SocketIO(app)


@app.route("/")
def index():
   return render_template("bla.html")


@socketio.on('message')
def handle_message(msg, user="User"):
    msg = "<dt>{}</dt><dl>{}<dl>".format(user, msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
