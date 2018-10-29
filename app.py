from flask import Flask, render_template,url_for,request,jsonify
from flask_socketio import SocketIO,join_room, leave_room
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

channels=[['Puthiya Thalaimurai', 'https://www.youtube.com/embed/-VfoXmi02zY?autoplay=1', 'https://yt3.ggpht.com/-uUA9W2X7gTE/AAAAAAAAAAI/AAAAAAAAAAA/ZyBVWwzjNKU/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',1], 
['Sun News', 'https://www.youtube.com/embed/DAzVIhYSi-8?autoplay=1', 'https://yt3.ggpht.com/-0ryR0iBcQR4/AAAAAAAAAAI/AAAAAAAAAAA/AJyOAXbAeYQ/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',2],
 ['Polimer TV', 'https://www.youtube.com/embed/3eFyaBXp2Pw?autoplay=1', 'https://yt3.ggpht.com/-HTBuNlCaWRc/AAAAAAAAAAI/AAAAAAAAAAA/5xOa_wW6LOA/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',3], 
 ['News 7', 'https://www.youtube.com/embed/J5bjsXBMrqw?autoplay=1', 'https://yt3.ggpht.com/-2l7MfvM53NI/AAAAAAAAAAI/AAAAAAAAAAA/r3eUuFf6Dho/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',4],
  ['News 18 Tamil Nadu', 'https://www.youtube.com/embed/NXGAmztCV8M?autoplay=1', 'https://yt3.ggpht.com/-NIgQfHt1xyk/AAAAAAAAAAI/AAAAAAAAAAA/2avjb9d76Ws/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',5], 
 ['CNBC', 'https://www.youtube.com/embed/LMBog4botcs?autoplay=1', 'https://yt3.ggpht.com/-XtkKuWmuq2k/AAAAAAAAAAI/AAAAAAAAAAA/Dl-qiQ1qNoc/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',6],
  ['TV5 Money', 'https://www.youtube.com/embed/X7h1mkwFAA4?autoplay=1', 'https://yt3.ggpht.com/-PgdKP6ufLSY/AAAAAAAAAAI/AAAAAAAAAAA/WnJzA--bFnU/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',7], 
 ['India TV', 'https://www.youtube.com/embed/5TEOMngiZ0E?autoplay=1', 'https://yt3.ggpht.com/-VxmxG_1VK_g/AAAAAAAAAAI/AAAAAAAAAAA/CMhiRWPuOMk/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',8],
  ['India Today', 'https://www.youtube.com/embed/62rmi9KMvVE?autoplay=1', 'https://yt3.ggpht.com/-_D48Q-O_Q48/AAAAAAAAAAI/AAAAAAAAAAA/r31m_qnzd7k/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',9], 
 ['Sky News', 'https://www.youtube.com/embed/XOacA3RYrXk?autoplay=1', 'https://yt3.ggpht.com/-uYnyeu0wFpQ/AAAAAAAAAAI/AAAAAAAAAAA/VU2Ct3J_ZQw/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',10], 
 ['CNN', 'https://www.youtube.com/embed/MnR9AVs6Q_c?autoplay=1', 'https://yt3.ggpht.com/-K12xTWC-rMI/AAAAAAAAAAI/AAAAAAAAAAA/2N_u5pcKB3w/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',11],
  ['Euro News', 'https://www.youtube.com/embed/OpqyqVA0Qmk?autoplay=1', 'https://yt3.ggpht.com/-E6JZH-KyyCc/AAAAAAAAAAI/AAAAAAAAAAA/fqL-p-2Wk40/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',12], 
 ['Bloomberg TV', 'https://www.youtube.com/embed/Ga3maNZ0x0w?autoplay=1', 'https://yt3.ggpht.com/-VEB545Y1H1M/AAAAAAAAAAI/AAAAAAAAAAA/trwfqEkQLEU/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',13],
  ['News 18 India', 'https://www.youtube.com/embed/NXGAmztCV8M?autoplay=1', 'https://yt3.ggpht.com/-AKivlOOZbgM/AAAAAAAAAAI/AAAAAAAAAAA/wm-EP6wlh7k/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',14],
  ['NDTV ', 'https://www.youtube.com/embed/mZQpvMxLTo0?autoplay=1', 'https://yt3.ggpht.com/-L8AxmJwZuy8/AAAAAAAAAAI/AAAAAAAAAAA/eZRzS7tRVX0/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',15], 
 ['NASA Live Feed', 'https://www.youtube.com/embed/4993sBLAzGA?autoplay=1', 'http://www.nasa.gov/sites/default/files/images/nasaLogo-570x450.png',16],
  ['National Geographic', 'https://www.youtube.com/embed/9BIHrwXs3MM?autoplay=1', 'https://yt3.ggpht.com/-eQlUGFZbnNI/AAAAAAAAAAI/AAAAAAAAAAA/NTSzOWhVFnk/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',17],
  ['Explore', 'https://www.youtube.com/embed/2UIA8xOVcOs?autoplay=1', 'https://yt3.ggpht.com/-oKZbj0nPwNE/AAAAAAAAAAI/AAAAAAAAAAA/23qLWZXZrpw/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',18], 
 ['DD News', 'https://www.youtube.com/embed/i1037LtNzy0?autoplay=1', 'https://yt3.ggpht.com/-To2bJ5pE_qo/AAAAAAAAAAI/AAAAAAAAAAA/U5H5BPelJts/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',19],
  ['Zoo TV', 'https://www.youtube.com/embed/P8pJYU5GiaE?autoplay=1', 'https://yt3.ggpht.com/-mUW6Ne6rXTc/AAAAAAAAAAI/AAAAAAAAAAA/5a9KlN74xig/s176-c-k-no-mo-rj-c0xffffff/photo.jpg',20]]

@app.route("/")
def index():
    return render_template('index.html',flash_message=None)

@app.route("/page",methods=['POST'])
def page():
    channel_no=int(request.form.to_dict()['channel_no'])-1
    if(channel_no <len(channels)):
    	return render_template('page.html',url=channels[channel_no][1],channels=channels,current_channel=channel_no+1,device_ref_id=int(request.form.to_dict()['device_ref_id']))
    else:
    	channel_no=int(request.form.to_dict()['current_channel'])-1
    	return render_template('page.html',url=channels[channel_no][1],channels=channels,current_channel=channel_no+1,device_ref_id=int(request.form.to_dict()['device_ref_id']),flash_message=request.form.to_dict()['channel_no']+" Channel is Not Available")

@app.route("/join_device",methods=["POST"])
def join_device():
	data=request.form.to_dict()['device_id']
	device=Device.objects(ref_id=data).first()
	if device:
		return render_template('page.html',url=channels[0][1],device_ref_id=data,channels=channels,current_channel=1)
	else:	
		return render_template('index.html',flash_message="device is not registered")

@socketio.on("add_device")
def add_device(data):
	device=Device.objects(device_id=data).first()

	if device:	
		socketio.emit('device_id',{'id':device.ref_id,'device_id':data},broadcast=True)
		
	else:
		device=Device(device_id=data)
		device.save()
		device=Device.objects(device_id=data).first()
		socketio.emit('device_id',{'id' : device.ref_id },broadcast=True)


@socketio.on("chno")
def change_channel(data):
	data=data.split('&')
	print(data)
	socketio.emit('redirect', {'channel_no':str(data[0]),'device_id':int(data[1])},broadcast=True)

	
if __name__ == "__main__":
    socketio.run(app)

