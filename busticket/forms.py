# Forms for busticket app
from django import forms
from google.appengine.api import users
from google.appengine.ext.db import djangoforms
from google.appengine.ext import db
from formfields import ListPropertyChoice
import models
import datetime
from studentapp.models import StudentInfo

"""
    Define Helper Methods for Populating Dynamic Form Data
"""
def check_entries(tournament):
    available_events = [] # This is the list we'll be building to return to the calling method
    #Initialize Counters
    debate_counter = 0
    ie_counter = 0
    congress_counter = 0
    #Initialize Iterators
    events = db.get(tournament.events)
    entries = db.get(tournament.entries)
    for event in events: # We are doing this per tournament event
        for entry in entries: # Run through the entries and increment the relevant counter
            if event.name == entry.event.name:
                if event.eventType == 'debate':
                    debate_counter = debate_counter + 1
                elif event.eventType == 'ie' || event.eventType == 'duo':
                    ie_counter = ie_counter + 1
                elif event.eventType == 'congress':
                    congress_counter = congress_counter + 1
        if event.eventType == 'debate':
            if debate_counter =< tournaments.debateEntryMax:
                available_events.append(event)
        elif event.eventType == 'ie' || event.eventType == 'duo':
            if ie_counter =< tournaments.ieEntryMax:
                available_events.append(event)
        elif event.eventType == 'congress':
            if ie_counter =< tournaments.congressEntryMax:
                available_events.append(event)
    return available_events

def get_event_choices(tournament_id, entry_check=False):
    tournament = models.Tournaments.get_by_id(int(tournament_id))
    if !entry_check:
        listed_events = tournament.events
        choices = [(m.key(), m.name) for m in db.get(listed_events)]
    else:
        available_events = check_entries(tournament)
        choices = [(m.key(), m.name) for m in available_events]
    return choices

def get_partner_choices(tournament_id):
    choices = []
    students = []
    tournament = models.Tournaments.get_by_id(int(tournament_id))
    entries = tournament.entries
    partners = [entry.partner.userID for entry in entries]
    user = users.get_current_user()
    if user in partners:
        for partner in partners:
            if user == partner:
                students.append(partner)
        choices = [(p.key(), p.nickname) for p in students]
    else:
        students = StudentInfo.all()
        choices = [(p.key(), p.userID.nickname) for p in students]
    return choices

"""
    Define Actual Forms
"""

class TournamentForm(djangoforms.ModelForm):
    events = ListPropertyChoice(
        widget=forms.CheckboxSelectMultiple(), 
        choices=[(m.key(), m.name) for m in models.Events.all()]
        )
    class Meta:
        model = models.Tournaments
        exclude = ['gcalEditLink', 'gcalEventLink', 'gcalEventXml']

class EventForm(djangoforms.ModelForm):
    eventType = forms.ChoiceField(
        choices=[('debate', 'Debate Event'), ('duo', 'Duo Event'), ('ie', 'Individual Event'), ('congress', 'Student Congress')]
    )
    class Meta:
        model = models.Events

class TicketForm(djangoforms.ModelForm):
    
    reqType = forms.ChoiceField()
    
    class Meta:
        model = models.TicketRequirements
        exclude = ['tournament', 'attachments'] #TODO: Need to add ability to create attachments on this form, as a URL list(GData?)

    def __init__(self, tournament_id, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.tournament_id = tournament_id
        self.fields = self.base_fields
        self.fields['reqType'].choices = get_event_choices(self.tournament_id)
        
class EntryForm(djangoforms.ModelForm):
    event = forms.ChoiceField()
    isTeamEvent = forms.ChoiceField(
        widget = forms.CheckboxSelect(),
        label = 'Team Event?',
    )
    partner = forms.ChoiceField()
    class Meta:
        model = models.Entries
        exclude = ['student']
        
    def __init__(self, tournament_id, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.tournament_id = tournament_id
        self.fields = self.base_fields
        self.fields['events'].choices = get_event_choices(self.tournament_id)
        self.fields['partner'].choices = get_partner_choices(self.tournament_id)
    
    def clean_events(self):
        data = self.cleaned_data
        debate_count = 0
        ie_count = 0
        congress_count = 0
        tournament = db.get(data['tournament'])
        cur_event = db.get(data['event'])
        student = StudentInfo.all().filter('userID =', users.get_current_user())
        entries = models.Entries.all().filter('tournament =', tournament.key()).filter('student =', student.key())
        
        # count some entries. Whee.
        for entry in entries:
            if entry.event.eventType == 'debate':
                debate_count = debate_count + 1
            elif entry.event.eventType == 'ie' || entry.event.eventType == 'duo':
                ie_count = ie_count + 1
            elif entry.event.eventType == 'congress':
                congress_count = congress_count + 1
        
        # You can't add more events than are allowed. 
        if cur_event.eventType == 'debate' && debate_count >= tournament.individualDebateEntryLimit:
            raise forms.ValidationError("You are already registered for the maximum number of debate events.")
        elif cur_event.eventType == 'ie' && ie_count >= tournament.individualIeEntryLimit:
            raise forms.ValidationError("You are already registered for the maximum number of individual and duo events.")
        elif cur_event.eventType == 'duo' && ie_count >= tournament.individualIeEntryLimit:
            raise forms.ValidationError("You are already registered for the maximum number of individual and duo events.")
        elif cur_event.eventType == 'congress' && congress_count >= tournament.individualCongressEntryLimit:
            raise forms.ValidationError("You are already registered for the maximum number of congress events.")
        
        return data
    
    def clean_partner(self):
        data = self.cleaned_data
        ie_count = 0
        current_event = db.get(data['event'])
        partner_choice = db.get(data['partner'])
        partner_debate_events = []
        partner_duo_events = []
        partner_entries = models.Entries.all().filter('tournament =', tournament.key()).filter('student =', partner_choice.key())

        # Check to see that individual didn't choose her/himself for a partner. 
        if partner_choice.userID == users.get_current_user():
            raise forms.ValidationError("You cannot choose yourself as a partner!")
        
        # Cycle through partner entries
        for entry in partner_entries:
            if entry.event.eventType == 'debate':
                partner_debate_events.append(entry.event.name)
                # If the selected partner already has somebody else selected as their debate partner, throw an error.
                if entry.event.name == current_event.name && if entry.hasPartner && if entry.partner != users.get_current_user():
                    raise forms.ValidationError("This student already has a partner in this event.")
            if entry.event.eventType == 'ie':
                ie_count = ie_count + 1
            if entry.event.eventType == 'duo':
                ie_count = ie_count + 1
                partner_duo_events.append(entry.event.name)
                # If the selected partner already has somebody as their duo partner, throw an error.
                if entry.event.name == current_event.name && if entry.partner != users.get_current_user():
                    raise forms.ValidationError("This student already has a partner in this event.")
        
        # If the partner already has a full debate quota, and this event isn't among them, throw an error.
        if current_event.eventType == 'debate' && 
        partner_debate_events.count() >= tournament.individualDebateEntryLimit && 
        if current_event.name not in partner_debate_events:
            raise forms.ValidationError("This partner can't have any additional debate events.")
        
        # If the partner already has a full IE quota, and this duo isn't already there, throw an error. 
        if current_event.eventType == 'duo' && 
        ie_count >= tournament.individualDebateEntryLimit &&
        current_event.name not in partner_duo_events:
            raise forms.ValidationError("This partner can't have any additional duo events.")
        
        return data
    
    def clean(self):
        data = self.cleaned_data
        req_partner = data['hasPartner']
        partner = data['partner']
        if req_partner && !partner:
            raise forms.ValidationError("You must select a partner for this event.")
        if !req_partner && partner:
            raise forms.ValidationError("You cannot select a partner for this event.")
        return data