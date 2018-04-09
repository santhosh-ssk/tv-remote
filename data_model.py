from mongoengine import *
class User(Document):
	name=StringField(required=True)
	profile_image=FileField()
	profile_image_name=StringField()
	profile_image_type=StringField()
	username=StringField(required=True,unique=True)
	password=StringField(required=True)
	email=StringField(required=True)
	phone_no=StringField(required=True)
	address=StringField(required=True)
	dob=StringField(required=True)
class User_token(Document):
	  username=StringField(required=True,unique=True)
	  token=StringField(required=True)