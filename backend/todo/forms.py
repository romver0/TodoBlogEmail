from django.forms import ModelForm
from .models import *


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'is_important']


class InfoForm(ModelForm):
    class Meta:
        model = InfoUser
        fields = ['сity', 'social_network', 'phonenumber',]
