from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q,Count
from django.urls import reverse
from .forms import *
from .models import Message, Chat,App_User,User

# Create your views here.
def handler(request):
    if request.user.is_authenticated:
        return messaging_service(request,'')
    else:
        return login_user(request)
    


def register_user(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()            
            return HttpResponseRedirect("/register")
    else:
        form = CustomUserCreationForm()
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
        return HttpResponseRedirect("/Chat")
    

"""
\messaging\

"""
def user_exists(username):
    try:
        User.objects.get(username=username)
        return True  # User with the provided username exists
    except User.DoesNotExist:
        return False


def messaging_service(request,username_link):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("/")
    if username_link:
        if not user_exists(username_link):
            return HttpResponseRedirect("/chat/")
    if request.method == "POST":
        if not username_link:
            form = general_sendmessage(data = request.POST)
        else:
            form = specific_sendmessage(data = request.POST)
        if form.is_valid():
            if not username_link:
                user_to = form.cleaned_data.get("user_to")
            else:
                user_to = username_link
            user_recep = App_User.objects.get(username = user_to)    
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
            appuser = App_User.objects.filter(user__username = username).first()
            form_add_friend = add_friend()
            new_friends_choices = User.objects.exclude(user_friends = appuser).exclude(username = appuser.user.username).values_list('username','username')
            form_add_friend.fields['user_to'].choices = new_friends_choices
            form = general_sendmessage()
            new_choices = appuser.friends.exclude(username=username).values_list('username','username')
            form.fields['user_to'].choices = new_choices
            usernames = appuser.friends.exclude(username=username).values_list('username', flat=True)
            return render(request, 'login/chat.html',{'username': username,'messageform': form,'users': usernames,'form_add_friend':form_add_friend})
        else:
            messages = Message.objects.filter(chat__in=Chat.objects.filter(participants__username=username).filter(participants__username=username_link))
            form = specific_sendmessage()
            return render(request, 'login/chat.html',{'username': username,'messageform': form, 'messages':messages})

def friends_service(request):
    user_sending = request.user
    user_to = request.POST.get()