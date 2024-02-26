from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Userprofile)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(ConversationMessage)
admin.site.register(Notification)