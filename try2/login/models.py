from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
class App_User(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='user_friends')

@receiver(m2m_changed, sender=App_User.friends.through)
def prevent_self_friendship(sender, instance, action, pk_set, **kwargs):
    if action == "pre_add":
        if instance.user_id in pk_set:
            raise ValueError("Cannot add yourself as a friend.")
# Create your models here.
class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='messages')
    created= models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)



