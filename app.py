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

urls=["https://www.youtube.com/embed/LXFxoS9ZJGg?autoplay=1"
]
@app.route("/")
def index():
    return render_template('index.html',)

@app.route("/page/<int:channel_no>")
def page(channel_no):
    return render_template('page.html',url=urls[channel_no-1])


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
	print(data['device_id'])
	user=Device.objects(ref_id=data["device_id"]).first()
	if user:
		socketio.emit('redirect',{'url':'https://tv-shows-01.herokuapp.com/page/1'})	
	else:
		socketio.emit('error', {"ref_id":data['device_id'],"message":"device id not registered"},broadcast=True)	

@socketio.on("chno")
def change_channel(data):
	print(data)
	socketio.emit('redirect', {'url': 'https://tv-shows-01.herokuapp.com/page/'+str(data)},broadcast=True)

	
if __name__ == "__main__":
    socketio.run(app)

