from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit


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

@socketio.on('client1')
def test_message(message):                    
    emit('client2', {'data': 'testdata'})
@socketio.on('my event')
def my_event(message):
	print(message)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1',port=5000)