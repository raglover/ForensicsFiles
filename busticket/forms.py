# Forms for busticket app
from django import forms
from google.appengine.ext.db import djangoforms
from google.appengine.ext import db
from formfields import ListPropertyChoice
import models



class TournamentForm(djangoforms.ModelForm):
    events = ListPropertyChoice(
        widget=forms.CheckboxSelectMultiple(), 
        choices=[(m.key(), m.name) for m in models.Events.all()]
        )
    class Meta:
        model = models.Tournaments
        exclude = ['gcalEditLink', 'gcalEventLink', 'gcalEventXml']

class EventForm(djangoforms.ModelForm):
    class Meta:
        model = models.Events

def get_choices(tournament_id):
    tournament = models.Tournaments.get_by_id(int(tournament_id))
    listed_events = tournament.events
    choices = [(m.key(), m.name) for m in db.get(listed_events)]
    return choices

class TicketForm(djangoforms.ModelForm):
    
    reqType = forms.ChoiceField()
    
    class Meta:
        model = models.TicketRequirements
        exclude = ['tournament', 'attachments'] #TODO: Need to add ability to create attachments on this form, as a URL list(GData?)

    def __init__(self, tournament_id, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.tournament_id = tournament_id
        self.fields = self.base_fields
        self.fields['reqType'].choices = get_choices(self.tournament_id)