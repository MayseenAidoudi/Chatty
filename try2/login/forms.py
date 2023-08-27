from django import forms
from .models import User,App_User
from django.contrib.auth.forms import UserCreationForm
class general_sendmessage(forms.Form):
    choices = User.objects.all().values_list('username','username')
    message_to_send = forms.CharField(label="message",max_length="500",widget=forms.TextInput(attrs={'id':'message_to_send'}))
    user_to = forms.ChoiceField(choices=choices)

class specific_sendmessage(forms.Form):
    message_to_send = forms.CharField(label="message",max_length="500" ,widget=forms.TextInput(attrs={'id':'message_to_send'}))

class CustomUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        app_user = App_User(user=user)
        app_user.save()
        return user

class add_friend(forms.Form):
    choices = User.objects.all().values_list('username','username')
    user_to = forms.ChoiceField(label="Select a person to add as a friend",choices=choices)

class FriendRequestForm(forms.Form):
    f_request_user = forms.CharField(widget=forms.HiddenInput)
    decision = forms.CharField(widget=forms.HiddenInput)