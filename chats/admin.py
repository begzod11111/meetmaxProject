from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Message)
admin.site.register(PrivateChat)
admin.site.register(GroupChat)

