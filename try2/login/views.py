from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q,Count
from django.urls import reverse
from .forms import sendmessage
from .models import Message, Chat,User

# Create your views here.
def handler(request):
    if request.user.is_authenticated:
        return messaging_service(request,'')
    else:
        return login_user(request)
def register_user(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request,"login/index.html", {"formregister": form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                error_message = "Successfully logged in"
                return render(request, 'login/index.html', { 'error_message': error_message})

        return render(request, 'login/index.html', {'formlogin': form})
    else:
        form = AuthenticationForm()
        if request.user.is_authenticated:
            username = request.user.get_username()
            return render(request, 'login/index.html', {'formlogin': form, 'error_message': username})
        else:
            return render(request,"login/index.html", {"formlogin":  form})
        
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        form = AuthenticationForm()
        error_message = "Successfully logged out"
        return render(request, 'login/index.html', {'form': form, 'error_message': error_message})
    else:
        return HttpResponseRedirect("/")
    

"""
\messaging\

"""

def messaging_service(request,username_link):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = sendmessage(data = request.POST)
        if form.is_valid():
            user_to = form.cleaned_data.get("user_to")
            user_recep = User.objects.get(username = user_to)
            text = form.cleaned_data.get("text")
            chatrec  = Chat.objects.annotate(participant_count=Count('participants')).filter(participants=request.user).filter(participants=user_recep).filter(participant_count=2)
            if chatrec.exists():
                chat_to = chatrec.get()
                message_to_send = Message(text = text, user = request.user, chat = chat_to)
                message_to_send.save()
            else:
                chat_to = Chat.objects.create()
                chat_to.participants.add(user_recep)
                chat_to.participants.add(request.user)
                chat_to.save()
                message_to_send = Message(text = text, user = request.user, chat = chat_to)
                message_to_send.save()
                print("hello")
        final_url = reverse('login:handler_user_included',args=[user_to])
        return HttpResponseRedirect(final_url)
    else:
        username = request.user.get_username()
        if not username_link:
            form = sendmessage()
            new_choices = [(value, label) for value, label in form.fields['user_to'].choices if value != username]
            form.fields['user_to'].choices = new_choices
            usernames = User.objects.exclude(username=username).values_list('username', flat=True)
            return render(request, 'login/chat.html',{'username': username,'messageform': form,'users': usernames})
        else:
            messages = Message.objects.filter(
            chat__in=Chat.objects.filter(participants__username=username).filter(participants__username=username_link))
            form = sendmessage()
            return render(request, 'login/chat.html',{'username': username,'messageform': form, 'messages':messages})

