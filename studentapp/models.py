# Models for StudentApp Application
from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
class StudentInfo(BaseModel):
    userID = db.UserProperty()
    nflID = db.IntegerProperty()
    goals = db.ListProperty(basestring)
    about = db.TextProperty()
    events = db.ListProperty(db.Key)
    avatar = db.BlobProperty()
    phone = db.StringProperty()

