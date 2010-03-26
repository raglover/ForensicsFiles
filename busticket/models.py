from appengine_django.models import BaseModel
from google.appengine.ext import db
import datetime

class Tournament(BaseModel):
    name = db.StringProperty(required=True)
    location = db.StringProperty(required=True)
    startDate = db.DateProperty(required=True)
    endDate = db.DateProperty(required=True)
    events = db.ListProperty(db.Key) #This is a list of the Events to be offered at any given tournament, keyed to Events
    #pseudo-element: requirements is a foreign key to TicketRequirements

class Events(BaseModel):
    name = db.StringProperty(required=True)
    desc = db.TextProperty(required=True)
    #pseudo-element: requirements is a foreign key to TicketRequirements

class TicketRequirement(BaseModel):
    reqType = db.ReferenceProperty(Events, collection_name='requirements')
    tournament = db.ReferenceProperty(Tournament, collection_name='requirements')
    dueDate = db.DateProperty(required=True)
    requirement = db.TextProperty(required=True)
    attachments = db.ListProperty(basestring)
    completedBy = db.ListProperty(db.Key) #This is a list of the users who have completed the requirement

class UserInfo(BaseModel):
    nflID = db.IntegerProperty()
    goals = db.ListProperty(basestring)
    about = db.TextProperty()
    events = db.ListProperty(db.Key) #This is a list of the events in which the student participates, or for which the coach is responsible, keyed to Events
    avatar = db.BlobProperty()
    phone = db.PhoneNumber()

class StudentInfo(UserInfo):
    student = db.UserProperty()

class coachInfo(UserInfo):
    coach = db.UserProperty()

class JudgeInfo(BaseModel):
    name = db.StringProperty(required=True)
    email = db.Email
    phone = db.PhoneNumber()
    events = db.ListProperty(db.key) #Which Events Can be Judged
    rating = db.UserRating()
    availability = db.ListProperty(db.Key) #For which Tournaments is the judge available?
    relStudent = db.ReferenceProperty(StudentInfo, collection_name='judges')
    notes = db.TextProperty()

