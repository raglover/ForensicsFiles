from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import users

# Create your models here.

class PersonInfo(polymodel.PolyModel):
    phoneNumber = db.PhoneNumberProperty()
    phoneType = db.StringProperty(choices=['cell', 'home', 'work'])
    address = db.PostalAddressProperty()
    email = db.EmailProperty()