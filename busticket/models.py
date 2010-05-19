# Models for BusTicket Application
from google.appengine.ext import db
import datetime
from studentapp.models import StudentInfo
from coachapp.models import CoachInfo

class Tournaments(db.Model):
    name = db.StringProperty(required=True)
    location = db.StringProperty(required=True)
    entryDeadline = db.DateProperty(required=True)
    startDate = db.DateProperty(required=True)
    endDate = db.DateProperty(required=True)
    events = db.ListProperty(db.Key) #This is a list of the Events to be offered at any given tournament, keyed to Events
    individualDebateEntryLimit = db.IntegerProperty(required=True, default=1)
    individualIeEntryLimit = db.IntegerProperty(required=True, default=2)
    individualCongressEntryLimit = db.IntegerProperty(required=True, default=1)
    debateEntryMax = db.IntegerProperty(required=True, default=6)
    ieEntryMax = db.IntegerProperty(required=True, default=6)
    congressEntryMax = db.IntegerProperty(required=True, default=6)
    gcalEditLink = db.TextProperty()
    gcalEventLink = db.TextProperty()
    gcalEventXml = db.TextProperty()
    #pseudo-element: requirements is a foreign key to TicketRequirements

class Events(db.Model):
    name = db.StringProperty(required=True)
    desc = db.TextProperty(required=True)
    eventType = db.StringProperty(required=True)
    hasPartner = db.BooleanProperty()
    #pseudo-element: requirements is a foreign key to TicketRequirements

class TicketRequirements(db.Model):
    reqType = db.ReferenceProperty(Events, collection_name='requirements')
    tournament = db.ReferenceProperty(Tournaments, collection_name='requirements')
    dueDate = db.DateProperty(required=True)
    requirement = db.TextProperty(required=True)
    attachments = db.ListProperty(basestring)

class CompletedReqs(db.Model):
    ticketID = db.ReferenceProperty(TicketRequirements, collection_name='completed')
    studentID = db.ReferenceProperty(StudentInfo, collection_name='completedReqs')
    completed_date = db.DateProperty(required=True)
    coachID = db.ReferenceProperty(CoachInfo, collection_name='signedOff')

class Entries(db.Model):
    student = db.ReferenceProperty(StudentInfo, collection_name='entries')
    event = db.ReferenceProperty(Events, collection_name='entries')
    tournament = db.ReferenceProperty(Tournaments, collection_name='entries')
    partner = db.ReferenceProperty(StudentInfo, collection_name='partner')
    otherInfo = db.TextProperty()