from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import users

# Create your models here.

class PersonInfo(polymodel.PolyModel):
    phoneNumber = db.PhoneNumberProperty(required=True)
    phoneType = db.StringProperty(required=True, choices=['cell', 'home', 'work'])
    address = db.PostalAddressProperty(required=True)
    email = db.EmailProperty(required=True)