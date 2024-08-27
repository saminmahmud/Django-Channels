from django.contrib import admin
from .models import Group, Chat

class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'timestamp', 'group']

class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Group, GroupModelAdmin)
admin.site.register(Chat, ChatModelAdmin)
# Register your models here.
