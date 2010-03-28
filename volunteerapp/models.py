# Models for VolunteerApp Application
from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
class VolunteerInfo(BaseModel):
    name = db.StringProperty(required=True)
    email = db.Email
    phone = db.StringProperty()
    events = db.ListProperty(db.Key) #Which Events Can be Judged
    availability = db.ListProperty(db.Key) #For which Tournaments is the judge available?
    relStudent = db.ReferenceProperty(StudentInfo, collection_name='judges')
    notes = db.TextProperty()