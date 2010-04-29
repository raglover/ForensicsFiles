# Views for BusTicket Application
from google.appengine.api import users
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import models
import forms
from studentapp.models import StudentInfo
import datetime
import atom
import gdata.service
import gdata.auth
import gdata.alt.appengine
import gdata.calendar
import gdata.calendar.service


def home(request):
    tournaments = _getTournamentSchedule()
    upcoming = _getCurrentTournament()
    completedTickets = _getCompletedReqs()
    return render_to_response(
        'base.html',
        { 'tournaments' : tournaments, 'upcoming' : upcoming, 'closed' : completedTickets }
    )

def tournament_form(request, tournament_id=None):
    if request.method == 'POST':
        if tournament_id:
            # This pulls up the current tournament for editing
            tournament = models.Tournaments.get_by_id(int(tournament_id))
            tournament_form = forms.TournamentForm(request.POST, instance=tournament)
        else:
            tournament_form = forms.TournamentForm(request.POST)
        if tournament_form.is_valid():
            tournament = tournament_form.save(commit=False)
            #TODO: Add ability to use this data to update GCal as the tournaments are created.
            tournament.put()
            return HttpResponseRedirect('/tournaments/')
    else:
        if tournament_id:
            tournament = models.Tournaments.get_by_id(int(tournament_id))
            tournament_form = forms.TournamentForm(instance=tournament)
        else:
            tournament_form = forms.TournamentForm()
    return render_to_response('busticket/tournamentform.html', {
        'tournament_id' : tournament_id,
        'tournament_form' : tournament_form
    })

def event_form(request, event_id=None):
    if request.method == 'POST':
        if event_id:
            # This pulls up the current tournament for editing
            event = models.Events.get_by_id(int(event_id))
            event_form = forms.EventForm(request.POST, instance=event)
        else:
            event_form = forms.EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.put()
            return HttpResponseRedirect('/events/')
    else:
        if event_id:
            event = models.Events.get_by_id(int(event_id))
            event_form = forms.EventForm(instance=event)
        else:
            event_form = forms.EventForm()
    return render_to_response('busticket/eventform.html', {
        'event_id' : event_id,
        'event_form' : event_form
    })    

def add_requirement_form(request, tournament_id=None):
    if request.method == 'POST':
        tournament = models.Tournaments.get_by_id(int(tournament_id))
        ticket_form = forms.TicketForm(tournament_id, request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.tournament = tournament.key()
            ticket.put()
            response = '/requirements/%s' % tournament_id
            return HttpResponseRedirect(response)
    else:
        tournament = models.Tournaments.get_by_id(int(tournament_id))
        ticket_form = forms.TicketForm(tournament_id)
    return render_to_response('busticket/requirementform.html', {
        'tournament' : tournament,
        'req_form' : ticket_form
    })
    
def requirements(request, tournament_id=None):
    tournament = models.Tournaments.get_by_id(int(tournament_id))
    tickets = tournament.requirements
    return render_to_response('busticket/requirements.html',
        { 'tournament' : tournament, 'tickets' : tickets }
    )

def tournaments(request):
    tournaments = _getTournamentSchedule()
    return render_to_response(
        'busticket/tournaments.html', {
        'tournaments' : tournaments
        }
    )

def events(request):
    events = models.Events.all()
    return render_to_response(
        'busticket/events.html', {
        'events' : events
        }
    )


#These are private methods, used internally for retrieving data. 
def _getCompletedReqs():
    curUser = users.get_current_user()
    tickets = models.CompletedReqs.all().filter('studentID =', curUser.user_id())
    if not tickets.get():
        tickets = 'You haven\'t completed any requirements. Get to work, SLACKER!'
    return tickets

def _getTournamentSchedule():
    tournaments = models.Tournaments.all()
    if not tournaments.get() :
        tournaments = 'No Tournaments Yet!'
    return tournaments

def _getCurrentTournament():
    today = datetime.date.today()
    tournamentQuery = models.Tournaments.all().filter('startDate > ', today).order('startDate')
    tournament = tournamentQuery.get()
    return tournament
    
def _getStudentEvents():
    student = users.get_current_user()
    query = StudentInfo.all().filter("studentID = ", student.user_id())
    record = query.get()
    if record:
        events = record.events
    else:
        events = "No Events! Damn."
    return events
        
"""
NOTE: This will have to be updated and made to work,eventually. But not for now.
def add_gcal_event(request, event):
    calendar_client = gdata.calendar.service.CalendarService()
    gdata.alt.appengine.run_on_appengine(calendar_client)
    token_request_url = None
    auth_token = gdata.auth.extract_auth_sub_token_from_url(request.url)
    if auth_token:
        calendar_client.SetAuthSubToken(calendar_client.upgrade_to_session_token(auth_token))
    if not isinstance(calendar_client.token_store.find_token(
            'http://www.google.com/calendar/feeds/'),
            gdata.auth.AuthSubToken):
        token_request_url = gdata.auth.geenrate_auth_sub_url(request.uri, ('http://www.google.com/calendar/feeds/default',))
    if event.gcalEditLink and event.gcalEventXml:
        cal_event = gdata.calendar.CalendarEventEntryFromString(str(event.gcalEventXml))
        cal_event.title = atom.Title(text=event.name)
        cal_event.when = [gdata.calendar.When(start_time=event.startDate, end_time=event.endDate)]
        cal_event.where = [gdata.calendar.Where(value_string=event.location)]
        try:
            updated_entry = calendar_client.UpdateEvent(str(event.edit_link). cal_event)
            event.gcalEditLink = updated_entry.GetEditLink().href
            event.gcalEventXml = str(updated_entry)
            event.save(commit=False)
        except gdata.service.RequestError, request_exception:
            request_error = request_exception[0]
            if request_error['status'] == 409:
                updated_entry = gdata.calendar.CalendarEventEntryFromString(request_error['body'])
                event.gcalEditLink = updated_entry.GetEditLink().href
                event.gcalEventXml = request_error['body']
                event.save(commit=False)
            else:
                raise
    else:
        event_entry = gdata.calendar.CalendarEventEntry()
        event_entry.title = atom.Title(text=event.name)
        event_entry.when.append(gdata.calendar.When(start_time=event.startDate, end_time=event.endDate))
        event_entry.where.append(gdata.calendar.Where(value_string=event.location))
        try:
            cal_event = calendar_client.InsertEvent(event_entry, 'http://www.google.com/calendar/feeds/default/private/full')
            edit_link = cal_event.GetEditLink()
            if edit_link and edit_link.href:
                event.gcalEditLink = edit_link.href
            alternate_link = cal_event.GetHtmlLink()
            if alternate_link and alternate_link.href:
                event.gcalEventLink = alternate_link.href
                event.gcalEventXml = str(cal_event)
            event.save(commit=False)
        except gdata.service.RequestError, request_exception:
            request_error = request_exception[0]
            if request_error['status'] == 401 or request_error['status'] == 403:
                gdata.alt.appengine.save_auth_tokens({})
            else:
                raise
    return event
"""        