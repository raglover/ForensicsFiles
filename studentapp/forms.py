# forms for studentapp application
from google.appengine.ext.db import djangoforms
from django import forms
from busticket.formfields import ListPropertyChoice
from busticket.models import Events
import models


class StudentForm(djangoforms.ModelForm):
    events = ListPropertyChoice(
        widget=forms.CheckboxSelectMultiple(), 
        choices=[(m.key(), m.name) for m in Events.all()]
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