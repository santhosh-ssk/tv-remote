from mongoengine import *
class User(Document):
	username=StringField(required=True,unique=True)
	device_id=StringField(required=True,unique=True)
class Device(Document):
	device_id=StringField(unique=True)
	ref_id=SequenceField()