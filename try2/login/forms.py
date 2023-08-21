from django import forms
from .models import User,App_User
from django.contrib.auth.forms import UserCreationForm
class general_sendmessage(forms.Form):
    choices = User.objects.all().values_list('username','username')
    text = forms.CharField(label="message",max_length="500")
    user_to = forms.ChoiceField(choices=choices)

class specific_sendmessage(forms.Form):
    text = forms.CharField(label="message",max_length="500")

class CustomUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        app_user = App_User(user=user)
        app_user.save()
        return user

class add_friend(forms.Form):
    choices = User.objects.all().values_list('username','username')
    user_to = forms.ChoiceField(label="Select a person to add as a friend",choices=choices)