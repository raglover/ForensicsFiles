from django.forms.fields import MultipleChoiceField
from google.appengine.ext import db

class ListPropertyChoice(MultipleChoiceField):

    def clean(self, value):
        """ extending the clean method to work with GAE keys """
        new_value = super(ListPropertyChoice, self).clean(value)
        key_list = []
        for k in new_value:
            key_list.append(db.Model.get(k).key())
        return key_list
