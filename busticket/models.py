# Models for BusTicket Application
from appengine_django.models import BaseModel
from google.appengine.ext import db
import datetime
from studentapp.models import StudentInfo

class Tournaments(BaseModel):
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

class TicketRequirements(BaseModel):
    reqType = db.ReferenceProperty(Events, collection_name='requirements')
    tournament = db.ReferenceProperty(Tournaments, collection_name='requirements')
    dueDate = db.DateProperty(required=True)
    requirement = db.TextProperty(required=True)
    attachments = db.ListProperty(basestring)

class CompletedReqs(BaseModel):
    ticketID = db.ReferenceProperty(TicketRequirements, collection_name='completed')
    studentID = db.ReferenceProperty(StudentInfo, collection_name='completedReqs')
    completed_date = db.DateProperty(required=True)
    
    """
    def valid_date():
        q = TicketRequirements.filter('__key__ =', ticketID)
        dueDate = q.dueDate.get()
        if completed_date =< dueDate
    """      