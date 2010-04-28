# Models for StudentApp Application
from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.api import users


# Create your models here.
class StudentInfo(BaseModel):
    userID = db.UserProperty()
    nflID = db.IntegerProperty()
    about = db.TextProperty()
    events = db.ListProperty(db.Key) # A list of events that the student does, keyed to busticket.models.SpeechEvents
    phone = db.StringProperty()

class StudentAvatar(BaseModel):
    student = db.ReferenceProperty(StudentInfo, collection_name='avatar')
    avatarImg = db.BlobProperty()

class StudentGoals(BaseModel):
    goal_types = ['Season', 'Tournament', 'Weekly', 'Personal']
    student = db.ReferenceProperty(StudentInfo, collection_name='goals')
    goalText = db.TextProperty()
    goalType = db.TextProperty(choices=goal_types)
    goalStartDate = db.DateProperty()
    goalEndDate = db.DateProperty()
    