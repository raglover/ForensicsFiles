# Models for CoachingApp Application
from appengine_django.models import BaseModel
from google.appengine.ext import db
# Create your models here.
class CoachInfo(BaseModel):
    name = db.UserProperty()
    events = db.ListProperty(db.Key) #Keyed off of Events
    