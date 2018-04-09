from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit,send
from flask_socketio import join_room, leave_room



app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'secret!'
values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template('index.html', **values)

@socketio.on('join')
def on_join(data):
    print(data)
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('my event')
def my_event(message):
	print(message)

@socketio.on('device_registration')
def device_registration(data):
	print(data)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1',port=5001)