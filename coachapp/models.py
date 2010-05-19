# Models for CoachingApp Application
from google.appengine.ext import db
# Create your models here.
class CoachInfo(db.Model):
    name = db.UserProperty()
    events = db.ListProperty(db.Key) #Keyed off of Events
    