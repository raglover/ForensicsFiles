from django.forms.fields import MultipleChoiceField
from appengine_django.models import BaseModel

class ListPropertyChoice(MultipleChoiceField):

    def clean(self, value):
        """ extending the clean method to work with GAE keys """
        new_value = super(ListPropertyChoice, self).clean(value)
        key_list = []
        for k in new_value:
            key_list.append(BaseModel.get(k).key())
        return key_list
