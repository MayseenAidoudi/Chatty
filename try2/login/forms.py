from django import forms
from .models import User

class sendmessage(forms.Form):
    choices = User.objects.all().values_list('username','username')
    text = forms.CharField(label="message",max_length="500")
    user_to = forms.ChoiceField(choices=choices)
    