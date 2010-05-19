# forms for studentapp application
from google.appengine.ext.db import djangoforms
from django import forms
from busticket.formfields import ListPropertyChoice
import busticket.models
import models


class StudentForm(djangoforms.ModelForm):
    event_options = [(e.key(), e.name) for e in busticket.models.Events.all()]
    events = ListPropertyChoice(
        widget=forms.CheckboxSelectMultiple(), 
        choices=event_options
        )
    class Meta:
        model = models.StudentInfo
        exclude = ['userID','class']

class AvatarForm(djangoforms.ModelForm):
    class Meta:
        model = models.StudentAvatar
        exclude = ['student']
        
class ParentForm(djangoforms.ModelForm):
    volunteerOps = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(), 
        )
    class Meta:
        model = models.StudentInfo
        exclude = ['student','class']