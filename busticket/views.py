# Views for BusTicket Application
from google.appengine.ext.db import djangoforms
from google.appengine.api import users
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import models
from studentapp.models import StudentInfo
import datetime


class TournamentForm(djangoforms.ModelForm):
    class Meta:
        model = models.Tournaments

class EventForm(djangoforms.ModelForm):
    class Meta:
        model = models.Events

class TicketForm(djangoforms.ModelForm):
    class Meta:
        model = models.TicketRequirements

def home(request):
    tournaments = getTournamentSchedule()
    openTickets = getOpenTickets()
    completedTickets = getCompletedTickets()
    return render_to_response(
        'base.html',
        { 'tournaments' : tournaments, 'open' : openTickets, 'closed' : completedTickets }
    )
    
def student(request):
    return render_to_response(
        'base.html',
        { 'text' : 'This is a Student page'}
    )
    
def getCompletedTickets():
    curUser = users.get_current_user()
    ticket = models.CompletedReqs.all().filter('studentID =', curUser.user_id())
    if not ticket.get() :
        ticket = "No Completed Requirements! Get to work."
    return ticket

def getTournamentSchedule():
    tournaments = models.Tournaments.all()
    if not tournaments.get() :
        tournaments = 'No Tournaments Yet!'
    return tournaments

def getOpenTickets():
    reqList = []
    today = datetime.date.today()
    curUser = users.get_current_user()
    curTourn = models.Tournaments.all().filter('startDate > ', today)
    if curTourn.get():
        student = StudentInfo.all().filter('userID = ', curUser.user_id())
        if student.get():
            tournID = curTourn.get()
            events = models.Events.all().filter('__key__ IN ', student.events()).filter('tournament = ', curTourn.key())
            for event in events.fetch(limit=5, offset=0):
                reqList = reqList.append(event.requirements())
        else:
            reqList = "Student Not Found."
    else:
        reqList = "No Active Tournaments"
    return reqList
