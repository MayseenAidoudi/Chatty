from django.contrib import admin
from .models import Chat,Message,App_User,Friend_Request

# Register your models here.
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(App_User)
admin.site.register(Friend_Request)
