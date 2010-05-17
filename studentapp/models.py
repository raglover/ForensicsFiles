# Models for StudentApp Application
from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.api import users
from core.models import PersonInfo


# Create your models here.
class StudentInfo(PersonInfo):
    userID = db.UserProperty(auto_current_user_add=True)
    studentID = db.IntegerProperty()
    about = db.TextProperty()
    events = db.ListProperty(db.Key) # A list of events that the student does, keyed to busticket.models.SpeechEvents

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
    
class ParentInfo(PersonInfo):
    help_options = ['Judging', 'Coaching', 'Fundraising', 'Team Care', 'Other']
    relationship_options = ['Mother', 'Father', 'Legal Guardian']
    student = db.ReferenceProperty(StudentInfo, collection_name="parents")
    relationship = db.StringProperty(choices=relationship_options)
    willHelp = db.BooleanProperty(verbose_name="Are You Willing to Volunteer?")
    volunteerOps = db.StringProperty(choices=help_options)
    