from flask import Flask, render_template,url_for
from flask.ext.socketio import SocketIO,join_room, leave_room
from mongoengine import connect
import json
connect(
    db='website_ui',
    username='admin',
    password='admin123',
    host='mongodb://admin:admin123@ds131384.mlab.com:31384/website_ui'
)

from data_model import Device,User
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html',)

@app.route("/page2")
def page2():
    return render_template('page2.html',)

@app.route("/page1")
def page1():
    return render_template('page1.html',)

@app.route("/page3")
def page3():
    return render_template('page3.html',)

@app.route("/page4")
def page4():
    return render_template('page4.html',)

@app.route("/page5")
def page5():
    return render_template('page5.html',)

@socketio.on('send_message')
def handle_source(json_data):
    print(json_data)
    text = json_data['message'].encode('ascii', 'ignore')
    socketio.emit('echo', {'echo': 'Server Says: '+text.decode()},broadcast=True)

@socketio.on("add_device")
def add_device(data):
	device=Device.objects(device_id=data).first()

	if device:	
		socketio.emit('device_id',{'id':device.ref_id},broadcast=True)
		
	else:
		device=Device(device_id=data)
		device.save()
		device=Device.objects(device_id=data).first()
		socketio.emit('device_id',{'id' : device.ref_id },broadcast=True)
@socketio.on("add_user")
def add_user(data):
	print(data['username'])
	user=User.objects(username=data["username"]).first()
	if user:
		socketio.emit('redirect', {'url': url_for('page2')})	
	else:
		user=User(username=data["username"],device_id=data["device_id"])
		user.save()
		print("added user")
		socketio.emit('redirect', {'url': url_for('page2')},broadcast=True)	

@socketio.on("chno")
def change_channel(data):
	print(data)
	socketio.emit('redirect', {'url': url_for('page'+str(data))},broadcast=True)

	
if __name__ == "__main__":
    socketio.run(app,host='192.168.38.168',port=5000)

