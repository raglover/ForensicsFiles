from google.appengine.ext import db
import datetime

class Tournament(db.Model):
    name = db.StringProperty(required=True)
    location = db.StringProperty(required=True)
    startDate = db.DateProperty(required=True)
    endDate = db.DateProperty(required=True)
    
class TicketRequirement(db.Model):
    reqType = db.StringProperty(required=True)
    tournament = db.ReferenceProperty(Tournament)
    dueDate = db.DateProperty(required=True)
    requirement = db.TextProperty(required=True)
    attachments = db.ListProperty()
    completedBy = db.ListProperty()